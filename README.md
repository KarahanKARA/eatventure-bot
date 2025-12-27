# Eatventure Bot 🎮🤖

An intelligent automation bot for the Eatventure mobile game using advanced computer vision and state machine architecture. The bot automatically detects on-screen elements, clicks buttons, manages upgrades, and progresses through game levels.

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
- 🛡️ **Safe Zone Detection**: Prevents accidental clicks in UI areas (menus, buttons)
- 📊 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- ⚙️ **Highly Configurable**: Easy configuration through `config.py`

## 🎮 How It Works

The bot operates through several intelligent states:

1. **Find Red Icons**: Scans the screen for collectible items using multi-template matching
2. **Click & Unlock**: Automatically clicks detected icons and handles unlock prompts
3. **Upgrade Stations**: Holds upgrade buttons to level up restaurants
4. **Open Boxes**: Collects reward boxes automatically
5. **Stats Upgrade**: Manages character statistics upgrades
6. **Smart Scrolling**: Navigates through the game map intelligently
7. **Level Transitions**: Detects and progresses to new levels

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

Open `config.py` and update the window title to match your scrcpy window:

```python
WINDOW_TITLE = "YourDeviceName"  # Replace with your device name from scrcpy
```

**To find your device name:**
1. Run scrcpy normally
2. Look at the window title (usually shows your device model, e.g., "SM-M315F")
3. Copy that exact name to `config.py`

### Step 4: Add Template Images

Place your template images in the `Assets/` folder. The bot needs these templates to recognize game elements:

```
Assets/
├── RedIcon.png          # Red notification icons
├── RedIcon2.png         # Variations of red icons
├── box1.png             # Reward box templates
├── upgradeStation.png   # Upgrade button
├── unlock.png           # Unlock popup
└── newLevel.png         # New level button
```

## 🎯 Usage

### Running the Bot

```bash
python main.py
```

### Keyboard Controls

- **Z**: Start/Stop the bot
- **X**: Show current cursor position (for configuration)
- **P**: Exit the program

### First Time Setup

1. Start scrcpy with your device
2. Launch the Eatventure game
3. Run the bot with `python main.py`
4. Press **Z** to start automation
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
├── window_capture.py       # Win32 window capture
├── image_matcher.py        # OpenCV template matching
├── mouse_controller.py     # Mouse automation
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── Assets/                 # Template images (PNG)
├── logs/                   # Log files
└── README.md               # This file
```

## 🔧 Troubleshooting

### Window Not Found
- Ensure scrcpy is running
- Verify `WINDOW_TITLE` in `config.py` matches your scrcpy window exactly
- Check window title with the **X** key while bot is running

### Template Not Detected
- Verify template images are in `Assets/` folder
- Lower the threshold values in `config.py`
- Use **X** key to capture exact coordinates
- Ensure templates are clear PNG images with transparency if needed

### Bot Clicking Wrong Areas
- Adjust click positions in `config.py`
- Configure forbidden zones to protect UI elements
- Review logs in `logs/bot.log` for coordinate information

### Performance Issues
- Close unnecessary applications
- Ensure USB debugging is stable
- Check CPU usage and adjust `CLICK_DELAY` if needed

## 📊 Logging

Logs are stored in `logs/bot.log` with detailed information:
- State transitions
- Template detection results
- Click coordinates
- Error messages

Set `DEBUG = True` in `config.py` for verbose logging.

## 🛡️ Safety Features

- **Forbidden Zone Protection**: Prevents clicks in critical UI areas
- **Window Activity Check**: Stops if the game window closes
- **Keyboard Interrupt**: Clean shutdown with Ctrl+C or P key
- **Smart Retry Logic**: Automatic recovery from detection failures

## 🤝 Contributing

This is a personal automation project. Feel free to fork and adapt it for your needs.

## ⚠️ Disclaimer

This bot is for educational purposes only. Use of automation tools may violate the game's Terms of Service. Use at your own risk.

## 📝 License

MIT License - Feel free to use and modify as needed.

## 🙏 Credits

- **OpenCV**: Computer vision library

**Keywords:** Eatventure, Eatventure bot, game automation Python, OpenCV game bot, mobile game automation, Android game bot, scrcpy automation, computer vision gaming, Python game bot, automated gameplay, image recognition bot, restaurant game bot, idle game automation
- **scrcpy**: Android screen mirroring tool
- **pywin32**: Windows API access

---

Made with ❤️ for game automation enthusiasts
