import win32gui
import win32ui
import win32con
import win32api
import ctypes
import numpy as np
from PIL import Image
import logging
import threading

logger = logging.getLogger(__name__)

ctypes.windll.shcore.SetProcessDpiAwareness(2)


class WindowCapture:
    def __init__(self, window_title, target_width=800, target_height=600):
        self.window_title = window_title
        self.hwnd = None
        self.target_width = target_width
        self.target_height = target_height
        self.find_window()
        self.resize_window()
    
    def find_window(self):
        self.hwnd = win32gui.FindWindow(None, self.window_title)
        if not self.hwnd:
            raise Exception(f"Window '{self.window_title}' not found!")
        logger.info(f"Window found: {self.window_title} (HWND: {self.hwnd})")
    
    def resize_window(self):
        if not self.hwnd:
            return
        
        rect = win32gui.GetWindowRect(self.hwnd)
        x, y = rect[0], rect[1]
        
        SWP_NOZORDER = 0x0004
        SWP_SHOWWINDOW = 0x0040
        ctypes.windll.user32.SetWindowPos(
            self.hwnd, 0, int(x), int(y), 
            int(self.target_width), int(self.target_height), 
            SWP_NOZORDER | SWP_SHOWWINDOW
        )
        logger.info(f"Window resized to {self.target_width}x{self.target_height}")
    
    def get_window_rect(self):
        if not self.hwnd:
            self.find_window()
        
        rect = win32gui.GetClientRect(self.hwnd)
        x, y = win32gui.ClientToScreen(self.hwnd, (rect[0], rect[1]))
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return x, y, width, height
    
    def capture(self, max_y=None):
        if not self.hwnd:
            self.find_window()
        
        x, y, width, height = self.get_window_rect()
        
        if max_y:
            height = min(height, max_y)
        
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        
        result = ctypes.windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 3)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (height, width, 4)
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        
        img = img[:, :, :3]
        img = np.ascontiguousarray(img)
        
        return img
    
    def is_window_active(self):
        return win32gui.IsWindow(self.hwnd) if self.hwnd else False


class ForbiddenAreaOverlay:
    def __init__(self, target_hwnd, forbidden_zones):
        self.target_hwnd = target_hwnd
        self.forbidden_zones = forbidden_zones
        self.overlay_hwnd = None
        self.running = False
        self.thread = None
        
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._create_overlay, daemon=True)
            self.thread.start()
            logger.info("Forbidden area overlay started")
    
    def stop(self):
        self.running = False
        if self.overlay_hwnd:
            try:
                win32gui.DestroyWindow(self.overlay_hwnd)
            except:
                pass
            self.overlay_hwnd = None
        logger.info("Forbidden area overlay stopped")
    
    def _create_overlay(self):
        try:
            wc = win32gui.WNDCLASS()
            wc.lpfnWndProc = self._wnd_proc
            wc.lpszClassName = "ForbiddenAreaOverlay"
            wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
            wc.hbrBackground = win32gui.GetStockObject(win32con.NULL_BRUSH)
            
            try:
                class_atom = win32gui.RegisterClass(wc)
            except Exception as e:
                pass
            
            target_rect = win32gui.GetClientRect(self.target_hwnd)
            target_pos = win32gui.ClientToScreen(self.target_hwnd, (0, 0))
            width = target_rect[2] - target_rect[0]
            height = target_rect[3] - target_rect[1]
            
            self.overlay_hwnd = win32gui.CreateWindowEx(
                win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW,
                "ForbiddenAreaOverlay",
                "Forbidden Area Overlay",
                win32con.WS_POPUP,
                target_pos[0], target_pos[1],
                width, height,
                0, 0, 0, None
            )
            
            win32gui.SetLayeredWindowAttributes(
                self.overlay_hwnd,
                0,
                128,
                win32con.LWA_ALPHA
            )
            
            win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)
            win32gui.UpdateWindow(self.overlay_hwnd)
            
            self._draw_zones()
            
            last_pos = target_pos
            while self.running:
                try:
                    new_pos = win32gui.ClientToScreen(self.target_hwnd, (0, 0))
                    if new_pos != last_pos:
                        last_pos = new_pos
                        win32gui.SetWindowPos(
                            self.overlay_hwnd,
                            win32con.HWND_TOPMOST,
                            new_pos[0], new_pos[1],
                            width, height,
                            win32con.SWP_SHOWWINDOW
                        )
                        self._draw_zones()
                    
                except Exception as e:
                    logger.error(f"Error in overlay update loop: {e}")
                    break
                
                import time
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Failed to create overlay window: {e}")
        finally:
            self.running = False
    
    def _draw_zones(self):
        if not self.overlay_hwnd:
            return
            
        try:
            hdc = win32gui.GetDC(self.overlay_hwnd)
            
            red_brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
            
            for x_min, x_max, y_min, y_max in self.forbidden_zones:
                old_brush = win32gui.SelectObject(hdc, red_brush)
                
                win32gui.Rectangle(hdc, int(x_min), int(y_min), int(x_max), int(y_max))
                
                win32gui.SelectObject(hdc, old_brush)
            
            win32gui.DeleteObject(red_brush)
            win32gui.ReleaseDC(self.overlay_hwnd, hdc)
            
        except Exception as e:
            logger.error(f"Error drawing zones: {e}")
    
    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            
            red_brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
            
            for x_min, x_max, y_min, y_max in self.forbidden_zones:
                old_brush = win32gui.SelectObject(hdc, red_brush)
                win32gui.Rectangle(hdc, int(x_min), int(y_min), int(x_max), int(y_max))
                win32gui.SelectObject(hdc, old_brush)
            
            win32gui.DeleteObject(red_brush)
            win32gui.EndPaint(hwnd, ps)
            return 0
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

