import win32api
import win32con
import win32gui
import time
import logging
import config

logger = logging.getLogger(__name__)


class MouseController:
    def __init__(self, hwnd, click_delay=0.1):
        self.hwnd = hwnd
        self.click_delay = click_delay
    
    def is_in_forbidden_zone(self, x, y):
        if (y >= config.FORBIDDEN_CLICK_Y_MIN and 
            config.FORBIDDEN_CLICK_X_MIN <= x <= config.FORBIDDEN_CLICK_X_MAX):
            logger.warning(f"Coordinates ({x}, {y}) blocked - FORBIDDEN_CLICK zone")
            return True
        
        if (config.FORBIDDEN_ZONE_1_Y_MIN <= y <= config.FORBIDDEN_ZONE_1_Y_MAX and
            config.FORBIDDEN_ZONE_1_X_MIN <= x <= config.FORBIDDEN_ZONE_1_X_MAX):
            logger.warning(f"Coordinates ({x}, {y}) blocked - FORBIDDEN_ZONE_1")
            return True
        
        if (config.FORBIDDEN_ZONE_2_Y_MIN <= y <= config.FORBIDDEN_ZONE_2_Y_MAX and
            config.FORBIDDEN_ZONE_2_X_MIN <= x <= config.FORBIDDEN_ZONE_2_X_MAX):
            logger.warning(f"Coordinates ({x}, {y}) blocked - FORBIDDEN_ZONE_2")
            return True
        
        if (config.FORBIDDEN_ZONE_3_Y_MIN <= y <= config.FORBIDDEN_ZONE_3_Y_MAX and
            config.FORBIDDEN_ZONE_3_X_MIN <= x <= config.FORBIDDEN_ZONE_3_X_MAX):
            logger.warning(f"Coordinates ({x}, {y}) blocked - FORBIDDEN_ZONE_3")
            return True
        
        if (config.FORBIDDEN_ZONE_4_Y_MIN <= y <= config.FORBIDDEN_ZONE_4_Y_MAX and
            config.FORBIDDEN_ZONE_4_X_MIN <= x <= config.FORBIDDEN_ZONE_4_X_MAX):
            logger.warning(f"Coordinates ({x}, {y}) blocked - FORBIDDEN_ZONE_4")
            return True
        
        if (config.FORBIDDEN_ZONE_5_Y_MIN <= y <= config.FORBIDDEN_ZONE_5_Y_MAX and
            config.FORBIDDEN_ZONE_5_X_MIN <= x <= config.FORBIDDEN_ZONE_5_X_MAX):
            logger.warning(f"Coordinates ({x}, {y}) blocked - FORBIDDEN_ZONE_5")
            return True
        
        return False
    
    def get_window_position(self):
        x, y = win32gui.ClientToScreen(self.hwnd, (0, 0))
        return x, y
    
    def move_to(self, x, y, relative=True):
        if relative:
            win_x, win_y = self.get_window_position()
            screen_x = win_x + x
            screen_y = win_y + y
        else:
            screen_x = x
            screen_y = y
        
        win32api.SetCursorPos((int(screen_x), int(screen_y)))
        logger.info(f"Cursor moved to window position ({x}, {y})")
    
    def click(self, x, y, relative=True, delay=None):
        if relative:
            if self.is_in_forbidden_zone(x, y):
                return
            
            win_x, win_y = self.get_window_position()
            screen_x = win_x + x
            screen_y = win_y + y
        else:
            screen_x = x
            screen_y = y
        
        win32api.SetCursorPos((screen_x, screen_y))
        time.sleep(0.02)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
        time.sleep(0.02)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
        
        logger.info(f"Clicked at ({screen_x}, {screen_y})")
        
        time.sleep(self.click_delay if delay is None else delay)
    
    def double_click(self, x, y, relative=True):
        self.click(x, y, relative)
        time.sleep(0.1)
    
    def hold_at(self, x, y, duration=None, relative=True):
        if duration is None:
            duration = config.UPGRADE_HOLD_DURATION
        click_interval = config.UPGRADE_CLICK_INTERVAL
        if relative:
            if self.is_in_forbidden_zone(x, y):
                return
            
            win_x, win_y = self.get_window_position()
            screen_x = win_x + x
            screen_y = win_y + y
        else:
            screen_x = x
            screen_y = y
        
        win32api.SetCursorPos((int(screen_x), int(screen_y)))
        time.sleep(0.02)
        
        logger.info(
            "Spamming click at (%s, %s) every %ss for %ss",
            screen_x,
            screen_y,
            click_interval,
            duration,
        )
        end_time = time.monotonic() + duration
        while time.monotonic() < end_time:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
            time.sleep(click_interval)
        
        time.sleep(self.click_delay)
    
    def drag(self, from_x, from_y, to_x, to_y, duration=0.3, relative=True):
        if relative:
            win_x, win_y = self.get_window_position()
            screen_from_x = win_x + from_x
            screen_from_y = win_y + from_y
            screen_to_x = win_x + to_x
            screen_to_y = win_y + to_y
        else:
            screen_from_x = from_x
            screen_from_y = from_y
            screen_to_x = to_x
            screen_to_y = to_y
        
        win32api.SetCursorPos((int(screen_from_x), int(screen_from_y)))
        time.sleep(0.02)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_from_x, screen_from_y, 0, 0)
        time.sleep(0.02)
        
        steps = 20
        for i in range(steps + 1):
            t = i / steps
            current_x = int(screen_from_x + (screen_to_x - screen_from_x) * t)
            current_y = int(screen_from_y + (screen_to_y - screen_from_y) * t)
            win32api.SetCursorPos((current_x, current_y))
            time.sleep(duration / steps)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_to_x, screen_to_y, 0, 0)
        logger.info(f"Dragged from ({from_x}, {from_y}) to ({to_x}, {to_y})")
        time.sleep(self.click_delay)
