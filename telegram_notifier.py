import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token, chat_id, enabled=True):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.enabled = enabled and bool(bot_token and chat_id)
        
        if self.enabled:
            logger.info("Telegram notifier enabled")
        else:
            logger.warning("Telegram notifier disabled")
    
    def send_message(self, message):
        if not self.enabled:
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                logger.debug(f"Telegram message sent: {message}")
                return True
            else:
                logger.error(f"Failed to send Telegram message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def notify_bot_started(self):
        message = "🤖 <b>Bot Started</b>"
        self.send_message(message)
    
    def notify_bot_stopped(self):
        message = "⏹️ <b>Bot Stopped</b>"
        self.send_message(message)
    
    def notify_new_level(self, level_number, time_spent):
        minutes = int(time_spent // 60)
        seconds = int(time_spent % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        message = f"{level_number}. restaurant completed! Time spent: {time_str}"
        self.send_message(message)
    
    def notify_level_milestone(self, total_levels):
        message = f"📊 <b>Milestone Reached!</b>\nTotal cities completed: {total_levels}"
        self.send_message(message)
