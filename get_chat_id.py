"""
Helper script to get your Telegram Chat ID

Steps:
1. Start your bot by messaging @YourBotName on Telegram
2. Send any message to your bot (e.g., "Hello")
3. Run this script: python get_chat_id.py
4. Copy your chat_id from the output
5. Paste it into config.py as TELEGRAM_CHAT_ID
"""

import requests
import config

bot_token = config.TELEGRAM_BOT_TOKEN

if not bot_token:
    print("ERROR: No bot token found in config.py")
    print("Please set TELEGRAM_BOT_TOKEN in config.py")
    exit(1)

url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

try:
    response = requests.get(url)
    data = response.json()
    
    if data.get("ok"):
        updates = data.get("result", [])
        
        if not updates:
            print("No messages found!")
            print("\nPlease:")
            print("1. Open Telegram and find your bot")
            print("2. Send any message to your bot (e.g., 'Hello')")
            print("3. Run this script again")
        else:
            print("Found messages!\n")
            
            # Get unique chat IDs
            chat_ids = set()
            for update in updates:
                if "message" in update:
                    chat = update["message"]["chat"]
                    chat_id = chat["id"]
                    chat_ids.add(chat_id)
                    
                    print(f"Chat ID: {chat_id}")
                    print(f"Chat Type: {chat['type']}")
                    if "username" in chat:
                        print(f"Username: @{chat['username']}")
                    if "first_name" in chat:
                        print(f"Name: {chat['first_name']}")
                    print("-" * 40)
            
            if chat_ids:
                print("\n✅ Copy one of the Chat IDs above")
                print("✅ Paste it into config.py as TELEGRAM_CHAT_ID")
                print(f"\nExample:")
                print(f'TELEGRAM_CHAT_ID = "{list(chat_ids)[0]}"')
    else:
        print(f"Error: {data}")
        
except Exception as e:
    print(f"Error: {e}")
