import logging
from pathlib import Path
import sys
import time
import win32api
import win32gui
from pynput import keyboard

import config
from bot import EatventureBot

current_match_index = 0
current_matches = []
bot_instance = None
z_pressed = False
should_exit = False


def on_press(key):
    global current_match_index, bot_instance, z_pressed, current_matches, should_exit
    try:
        if hasattr(key, 'char'):
            if key.char == 'x':
                screen_x, screen_y = win32api.GetCursorPos()
                logger = logging.getLogger(__name__)
                if bot_instance and bot_instance.window_capture.hwnd:
                    win_x, win_y = win32gui.ClientToScreen(bot_instance.window_capture.hwnd, (0, 0))
                    rel_x = screen_x - win_x
                    rel_y = screen_y - win_y
                    logger.info(f"[X pressed] Window position: ({rel_x}, {rel_y})")
                else:
                    logger.info(f"[X pressed] Bot not initialized yet")
            elif key.char == 'z':
                logger = logging.getLogger(__name__)
                if bot_instance:
                    bot_instance.running = not bot_instance.running
                    if bot_instance.running:
                        logger.info("[Z pressed] Bot STARTED")
                    else:
                        logger.info("[Z pressed] Bot STOPPED")
            elif key.char == 'p':
                logger = logging.getLogger(__name__)
                logger.info("[P pressed] Exiting program...")
                should_exit = True
    except Exception as e:
        pass


def setup_logging():
    logs_dir = Path(config.LOGS_DIR)
    logs_dir.mkdir(exist_ok=True)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG if config.DEBUG else logging.INFO
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    file_handler = logging.FileHandler(logs_dir / 'bot.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def main():
    global cursor_showing_enabled
    
    print("=" * 60)
    print("Eatventure Bot - Screen Automation Tool")
    print("=" * 60)
    print(f"Window Title: {config.WINDOW_TITLE}")
    print(f"Match Threshold: {config.MATCH_THRESHOLD * 100}%")
    print(f"Templates Directory: {config.TEMPLATES_DIR}")
    print("=" * 60)
    
    setup_logging()
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    try:
        global bot_instance
        bot = EatventureBot()
        bot_instance = bot
        
        logger = logging.getLogger(__name__)
        logger.info("Bot initialized and ready")
        logger.info("Press Z to START/STOP the bot")
        logger.info("Press X to see window-relative cursor position")
        logger.info("Press P to EXIT the program")
        
        while not should_exit:
            if bot.running:
                bot.state_machine.update()
            time.sleep(0.1)
        
        logger.info("Program exiting...")
        
    except KeyboardInterrupt:
        logging.info("\nBot stopped by user (Ctrl+C)")
        listener.stop()
        return 0
    except Exception as e:
        logging.error(f"\nFatal error: {e}", exc_info=True)
        listener.stop()
        return 1
    finally:
        listener.stop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
