import win32gui
import win32ui
import win32con
import win32api
import ctypes
import numpy as np
from PIL import Image
import logging

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
