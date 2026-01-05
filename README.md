# Eatventure Bot 🎮🤖

An intelligent automation bot for the Eatventure mobile game using advanced computer vision and state machine architecture. The bot automatically detects on-screen elements, clicks buttons, manages upgrades, and progresses through game levels with Telegram notifications.

## 🎬 Demo

https://github.com/user-attachments/assets/4560ed96-00ef-4f9d-842f-6cd6317f2a22

> **Note:** Upload your video to a GitHub issue/PR comment, then paste the auto-generated link here for best compatibility.

**Direct Link:** [Watch Demo Video](Assets/demo.mp4)

## ✨ Features

- 🎯 **Computer Vision**: Advanced template matching using OpenCV with multi-template detection
- 🖱️ **Intelligent Mouse Control**: Automated clicking, holding, and dragging with forbidden zone protection
- 🔄 **State Machine Architecture**: Robust state management for complex game automation
- 📸 **Window Capture**: Direct window capture using Win32 API for optimal performance
- 🎨 **Multi-Template Matching**: Detects red icons using multiple template variations for accuracy
- 🛡️ **Safe Zone Detection**: Prevents accidental clicks in UI areas (menus, buttons) with configurable forbidden zones
- 📊 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- 📱 **Telegram Integration**: Real-time notifications about bot activity and level completions
- 🎨 **Visual Debugging**: Optional overlay to visualize forbidden zones
- ⚙️ **Highly Configurable**: Easy configuration through `config.py` with extensive comments

## 🎮 How It Works

The bot operates through several intelligent states:

1. **Find Red Icons**: Scans the screen for collectible items using multi-template matching
2. **Click & Unlock**: Automatically clicks detected icons and handles unlock prompts
3. **Upgrade Stations**: Holds upgrade buttons to level up restaurants
4. **Open Boxes**: Collects reward boxes automatically
5. **Stats Upgrade**: Manages character statistics upgrades
6. **Smart Scrolling**: Navigates through the game map intelligently
7. **Level Transitions**: Detects and progresses to new levels with Telegram notifications

## 📋 Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.8 or higher
- **Android Device**: Connected via scrcpy

## 🚀 Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install and Configure scrcpy

1. **Download scrcpy**: [https://github.com/Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)
2. **Extract** scrcpy to a convenient location
3. **Connect your Android device** via USB with USB debugging enabled
4. **Run scrcpy**:
   ```bash
   scrcpy --window-title "YourDeviceName"
   ```

### Step 3: Configure the Bot

Open `config.py` and configure the following settings:

#### Window Configuration
```python
# The exact title of your scrcpy window
# To find it: Look at the window's title bar after running scrcpy
WINDOW_TITLE = "SM-M315F"  # Replace with your device name
```

**How to find your WINDOW_TITLE:**
1. Run scrcpy normally: `scrcpy --window-title "YourDeviceName"`
2. Look at the window's title bar (usually shows device model like "SM-M315F", "Pixel 6", etc.)
3. Copy that exact name to `config.py`
4. Alternative: While bot is running, press **X** to test if the window is detected

#### Telegram Notifications (Optional but Recommended)

The bot can send you real-time notifications via Telegram:
- 🤖 Bot start/stop events
- 🎉 Level completions with time tracking
- 📊 Progress updates

**Setup Steps:**

1. **Create a Telegram Bot:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the **bot token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Chat ID:**
   - Send any message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for `"chat":{"id": YOUR_CHAT_ID` (a number like `1352878588`)

3. **Configure in config.py:**
   ```python
   TELEGRAM_ENABLED = True  # Set to False to disable notifications
   TELEGRAM_BOT_TOKEN = "your-bot-token-here"
   TELEGRAM_CHAT_ID = "your-chat-id-here"
   ```

**Telegram Messages You'll Receive:**
- `🤖 Bot Started` - When you press Z to start
- `⏹️ Bot Stopped` - When you press Z to stop
- `5. restaurant completed! Time spent: 03:45` - After each level completion

### Step 4: Add Template Images

Place your template images in the `Assets/` folder. The bot needs these templates to recognize game elements:

```
Assets/
# The exact title of your scrcpy window (see in window title bar)
WINDOW_TITLE = "SM-M315F"
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 780
```

### Telegram Notifications
```python
# Master switch for all Telegram notifications
TELEGRAM_ENABLED = True  # Set to False to disable

# Your bot credentials (get from @BotFather)
TELEGRAM_BOT_TOKEN = "your-token-here"
TELEGRAM_CHAT_ID = "your-chat-id-here"
```

### Detection Thresholds
```python
MATCH_THRESHOLD = 0.98           # General matching confidence (0.0-1.0)
RED_ICON_THRESHOLD = 0.95        # Red icon detection threshold
RED_ICON_MIN_MATCHES = 3         # Minimum template matches required
```

### Visual Debugging
```python
# Shows red overlay rectangles on forbidden zones
ShowForbiddenArea = False  # Set to True to visualize forbidden zones
```

When `ShowForbiddenArea = True`, the bot displays a semi-transparent overlay showing all forbidden zones in red. This is useful for:
- Debugging click position issues
- Visualizing protected UI areas
- Adjusting forbidden zone coordinates

### Click Positions
```python
IDLE_CLICK_POS = (2, 390)        # Safe idle click position
STATS_UPGRADE_POS = (270, 304)   # Stats upgrade button
SCROLL_START_POS = (170, 380)    # Scroll start position
SCROLL_END_POS = (170, 200)      # Scroll end position
```

### Forbidden Zones

Forbidden zones prevent the bot from clicking on critical UI elements. Each zone is defined by X and Y coordinate boundaries:

```python
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

# ... and more zones
```

**How Forbidden Zones Work:**
- Bot checks every click position before executing
- If position is inside any forbidden zone, click is blocked
- Prevents accidental UI interactions (settings, shop, ads, etc.)

**Adding New Forbidden Zones:**
1. Set `ShowForbiddenArea = True` to visualize current zones
2. Press **X** while hovering over the area you want to protect
3. Note the coordinates shown in the log
4. Add a new zone in `config.py`:
   ```python
   FORBIDDEN_ZONE_6_X_MIN = your_x_min
   FORBIDDEN_ZONE_6_X_MAX = your_x_max
   FORBIDDEN_ZONE_6_Y_MIN = your_y_min
   FORBIDDEN_ZONE_6_Y_MAX = your_y_max
   ```
5. Update `mouse_controller.py` to include the new zone check
6. Update `bot.py` to include the zone in the overlay (if using `ShowForbiddenArea`)Press **Z** to start automation
5. Monitor the console and `logs/bot.log` for activity

## ⚙️ Configuration

All settings are in `config.py`. Key configurations:

### Window Settings
```python
WINDOW_TITLE = "SM-M315F"        # Your scrcpy window title
WINDOW_WIDTH = 360               # Window width
WINDOW_HEIGHT = 780              # Window height
```

### Detection Thresholds
```python
MATCH_THRESHOLD = 0.98           # General matching confidence (0.0-1.0)
RED_ICON_THRESHOLD = 0.95        # Red icon detection threshold
RED_ICON_MIN_MATCHES = 3         # Minimum template matches required
```

### Click Positions
```python
IDLE_CLICK_POS = (2, 390)        # Safe idle click position
STATS_UPGRADE_POS = (270, 304)   # Stats upgrade button
SCROLL_START_POS = (170, 380)    # Scroll start position
SCROLL_END_POS = (170, 200)      # Scroll end position
```

### Forbidden Zones
Configure areas where the bot should never click:
```python
FORBIDDEN_ZONE_1_X_MIN = 290     # Right menu area
FORBIDDEN_ZONE_1_X_MAX = 350
FORBIDDEN_ZONE_1_Y_MIN = 93
FORBIDDEN_ZONE_1_Y_MAX = 260
```

## 📁 Project Structure

```
eatventure-bot/
├── main.py                 # Entry point, keyboard controls
├── bot.py                  # Core bot logic and state handlers
├── state_machine.py        # State machine implementation
├── window_capture.py       # Win32 window capture & forbidden zone overlay
├── image_matcher.py        # OpenCV template matching
├── mouse_controller.py     # Mouse automation with zone protection
├── telegram_notifier.py    # Telegram notification system
├── config.py               # Configuration settings (with detailed comments)
├── requirements.txt        # Python dependencies
├── Assets/                 # Template images (PNG)
├── logs/                   # Log files
└── README.md               # This file
```

## 📊 Configuration Files Explained

### config.py
The main configuration file with extensive comments explaining each setting:
- **Window Configuration**: WINDOW_TITLE and dimensions
- **Telegram Settings**: TELEGRAM_ENABLED, bot token, and chat ID
- **Detection Thresholds**: Template matching sensitivity
- **Forbidden Zones**: Protected UI areas (5 zones by default, expandable)
- **Debug Options**: ShowForbiddenArea for visual debugging
- **Click Positions**: All automated click coordinates
- **Bot Behavior**: Timing, delays, and automation parameters

## 🔧 Troubleshooting

### Window Not Found
- Ensure scrcpy is running
- Verify `WINDOW_TITLE` in `config.py` matches your scrcpy window exactly
- Check window title with the **X** key while bot is running
- Try running: `scrcpy --window-title "YourDeviceName"` with a custom title

### Template Not Detected
- Verify template images are in `Assets/` folder
- Lower the threshold values in `config.py`
- Use **X** key to capture exact coordinates
- Ensure templates are clear PNG images with transparency if needed

### Bot Clicking Wrong Areas
- Enable `ShowForbiddenArea = True` to visualize protected zones
- Adjust click positions in `config.py`
- Configure additional forbidden zones to protect UI elements
- Review logs in `logs/bot.log` for coordinate information
- Use **X** key to find correct coordinates

### Telegram Not Working
- Verify `TELEGRAM_ENABLED = True` in config.py
- Double-check bot token and chat ID
- Test by visiting: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
- Make sure you sent at least one message to your bot first
- Check logs for Telegram-related error messages

### Performance Issues
- Close unnecessary applications
- Ensure USB debugging is stable
- Reduce `CLICK_DELAY` in config (current: 0.1s)
- Check CPU usage during bot operation
- Consider lowering image matching thresholds

## 📊 Logging

Logs are stored in `logs/bot.log` with detailed information:
- State transitions
- Template detection results
- Click coordinates
- Error messages

Set `DEBUG = True` in `config.py` for verbose logging.

## 🛡️ Safety Features

- **Forbidden Zone Protection**: Prevents clicks in critical UI areas with configurable zones
- **Visual Debugging**: Optional overlay to visualize forbidden zones (`ShowForbiddenArea`)
- **Window Activity Check**: Stops if the game window closes
- **Keyboard Interrupt**: Clean shutdown with Ctrl+C or P key
- **Smart Retry Logic**: Automatic recovery from detection failures
- **Telegram Monitoring**: Real-time notifications to track bot activity remotely

## 🤝 Contributing

This is a personal automation project. Feel free to fork and adapt it for your needs.

## ⚠️ Disclaimer

This bot is for educational purposes only. Use of automation tools may violate the game's Terms of Service. Use at your own risk.

## 📝 License

MIT License - Feel free to use and modify as needed.

## 🙏 Credits

- **OpenCV**: Computer vision library

# Eatventure Bot 🎮🤖
Intelligent automation bot for Eatventure mobile game

**Keywords:** Eatventure, Eatventure bot, game automation Python, OpenCV game bot, mobile game automation, Android game bot, scrcpy automation, computer vision gaming, Python game bot, automated gameplay, image recognition bot, restaurant game bot, idle game automation
- **scrcpy**: Android screen mirroring tool
- **pywin32**: Windows API access

---

Made with ❤️ for game automation enthusiasts
