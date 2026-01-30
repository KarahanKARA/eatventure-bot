# Window Configuration
# WINDOW_TITLE: The exact title of the scrcpy window (visible at the top of the window)
# To find it: Look at your scrcpy window's title bar, it usually shows your device model
WINDOW_TITLE = "V2352GA"
WINDOW_WIDTH = 300 * 1.2
WINDOW_HEIGHT = 650 * 1.2

# Detection Thresholds
MATCH_THRESHOLD = 0.98
RED_ICON_THRESHOLD = 0.94
RED_ICON_MIN_MATCHES = 2
STATS_RED_ICON_THRESHOLD = 0.97
SEARCH_INTERVAL = 0.5
CLICK_DELAY = 0.03

# Directory Paths
TEMPLATES_DIR = "templates"
ASSETS_DIR = "Assets"
LOGS_DIR = "logs"
SCREENSHOTS_DIR = "screenshots"

# Debug and Visualization Settings
DEBUG = True
SAVE_SCREENSHOTS = True

# ShowForbiddenArea: Enables a visual overlay showing forbidden zones in red
# When True, displays red rectangles over areas where the bot won't click
# Useful for debugging and visualizing the forbidden zones configuration
ShowForbiddenArea = False

# Telegram Bot Configuration
# TELEGRAM_ENABLED: Master switch to enable/disable all Telegram notifications
# Set to True if you want to receive any Telegrazm messages from the bot
TELEGRAM_ENABLED = False

# TELEGRAM_BOT_TOKEN: Your Telegram bot API token from @BotFather
# To get one: Message @BotFather on Telegram, use /newbot command
TELEGRAM_BOT_TOKEN = ""

# TELEGRAM_CHAT_ID: Your Telegram chat ID to receive messages
# To get it: Message your bot, then visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
# Look for "chat":{"id": YOUR_CHAT_ID in the response
TELEGRAM_CHAT_ID = ""

# Game Element Detection
MAX_SEARCH_Y = 660
EXTENDED_SEARCH_Y = 710

# Click Positions (relative to window)
UPGRADE_POS = (320, 726)
NEW_LEVEL_POS = (40, 726)
REDICON_CHECK_POS = (60, 704)
LEVEL_TRANSITION_POS = (183, 561)
IDLE_CLICK_POS = (2, 390)
INIT_CLICK_POS = (180, 472)
STATS_UPGRADE_POS = (270, 304)
STATS_UPGRADE_BUTTON_POS = (310, 698)
SCROLL_START_POS = (170, 380)
SCROLL_END_POS = (170, 200)
NEW_LEVEL_BUTTON_POS = (30, 692)

# Template Matching Settings
UPGRADE_STATION_THRESHOLD = 0.94
UPGRADE_STATION_COLOR_CHECK = False
BOX_THRESHOLD = 0.97
UNLOCK_THRESHOLD = 0.85
NEW_LEVEL_THRESHOLD = 0.95

# Bot Behavior Configuration
RED_ICON_CYCLE_COUNT = 3
STATS_UPGRADE_CLICK_DURATION = 2.0
STATS_UPGRADE_CLICK_DELAY = 0.010
STATS_ICON_PADDING = 25
CAPTURE_CACHE_TTL = 0.08
UPGRADE_HOLD_DURATION = 5.0
UPGRADE_CLICK_INTERVAL = 0.010
SCROLL_UP_CYCLES = 2

# Red Icon Detection Offsets
RED_ICON_OFFSET_X = 10
RED_ICON_OFFSET_Y = 10

# Red Icon Detection Zones
NEW_LEVEL_RED_ICON_X_MIN = 40
NEW_LEVEL_RED_ICON_X_MAX = 60
NEW_LEVEL_RED_ICON_Y_MIN = 665
NEW_LEVEL_RED_ICON_Y_MAX = 680

UPGRADE_RED_ICON_X_MIN = 280
UPGRADE_RED_ICON_X_MAX = 310
UPGRADE_RED_ICON_Y_MIN = 665
UPGRADE_RED_ICON_Y_MAX = 680

# State Machine Settings
STATE_DELAY = 0.05
MAX_SCROLL_CYCLES = 3

# Forbidden Zones Configuration
# These zones prevent the bot from clicking on critical UI elements
# Each zone is defined by: X_MIN, X_MAX, Y_MIN, Y_MAX coordinates
# You can add more zones by following the same pattern (FORBIDDEN_ZONE_6, etc.)

# General forbidden click area (bottom bar)
FORBIDDEN_CLICK_X_MIN = 60
FORBIDDEN_CLICK_X_MAX = 280
FORBIDDEN_CLICK_Y_MIN = 668

# Zone 1: Right side menu area
FORBIDDEN_ZONE_1_X_MIN = 290
FORBIDDEN_ZONE_1_X_MAX = 350
FORBIDDEN_ZONE_1_Y_MIN = 93
FORBIDDEN_ZONE_1_Y_MAX = 270

# Zone 2: Left side top menu area
FORBIDDEN_ZONE_2_X_MIN = 0
FORBIDDEN_ZONE_2_X_MAX = 60
FORBIDDEN_ZONE_2_Y_MIN = 50
FORBIDDEN_ZONE_2_Y_MAX = 280

# Zone 3: Left side bottom menu area
FORBIDDEN_ZONE_3_X_MIN = 0
FORBIDDEN_ZONE_3_X_MAX = 60
FORBIDDEN_ZONE_3_Y_MIN = 590
FORBIDDEN_ZONE_3_Y_MAX = 667

# Zone 4: Top center notification area
FORBIDDEN_ZONE_4_X_MIN = 145
FORBIDDEN_ZONE_4_X_MAX = 200
FORBIDDEN_ZONE_4_Y_MIN = 65
FORBIDDEN_ZONE_4_Y_MAX = 110

# Zone 5: Bottom navigation bar
FORBIDDEN_ZONE_5_X_MIN = 55
FORBIDDEN_ZONE_5_X_MAX = 285
FORBIDDEN_ZONE_5_Y_MIN = 660
FORBIDDEN_ZONE_5_Y_MAX = 725
