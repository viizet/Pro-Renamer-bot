# 🤖 Telegram File Rename Bot 4GB

<div align="center">
  <img src="https://graph.org/file/ad48ac09b1e6f30d2dae4.jpg" alt="Rename Bot Logo" width="300">
  
  [![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat&logo=telegram)](https://t.me/filerenamexprobot)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://python.org)
  [![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-green?style=flat)](https://pyrogram.org)
</div>

## 📖 Overview

An advanced Telegram bot for renaming files up to 4GB in size. Built with Python and Pyrogram, this bot offers premium features including custom thumbnails, captions, and broadcast functionality.

## ✨ Features

- 🚀 **Fast File Renaming** - Rename files quickly and efficiently
- 📁 **4GB File Support** - Handle large files with premium upgrade
- 🖼️ **Custom Thumbnails** - Set permanent custom thumbnails
- 📝 **Custom Captions** - Add personalized captions to files
- 📢 **Broadcast System** - Send messages to all users (Admin only)
- 🔄 **File Conversion** - Convert between video and file formats
- 🔒 **Force Subscribe** - Optional channel subscription requirement
- ⚡ **Unlimited Renaming** - No limits on concurrent operations
- 🎨 **Custom Start Picture** - Personalized bot interface

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB database
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- API credentials from [my.telegram.org](https://my.telegram.org)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/JishuDeveloper/Rename-Bot-4GB.git
   cd Rename-Bot-4GB
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file or set environment variables:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   ADMIN=your_user_id
   LOG_CHANNEL=your_log_channel_id
   DATABASE_URL=your_mongodb_url
   DATABASE_NAME=your_db_name
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### Deploy on Replit

1. Import this repository to Replit
2. Set up the required environment variables in Secrets
3. Click the Run button to start the bot

## 🔧 Configuration

### Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Telegram API ID from my.telegram.org | ✅ |
| `API_HASH` | Telegram API Hash from my.telegram.org | ✅ |
| `BOT_TOKEN` | Bot token from @BotFather | ✅ |
| `ADMIN` | Admin user ID (space-separated for multiple) | ✅ |
| `LOG_CHANNEL` | Log channel ID (must start with -100) | ✅ |
| `DATABASE_URL` | MongoDB connection URL | ✅ |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_NAME` | MongoDB database name | `madflixbotz` |
| `FORCE_SUBS` | Force subscribe channel username (without @) | None |
| `START_PIC` | Custom start command picture URL | Default logo |
| `STRING_SESSION` | Pyrogram session string for 4GB support | None |

## 📱 Bot Commands

### User Commands

- `/start` - Start the bot and see welcome message
- `/viewthumb` - View current thumbnail
- `/delthumb` - Delete current thumbnail
- `/set_caption` - Set custom caption
- `/see_caption` - View current caption
- `/del_caption` - Delete custom caption
- `/ping` - Check bot response time
- `/myplan` - View current subscription plan
- `/upgrade` - View premium plans
- `/donate` - Support the developer

### Admin Commands

- `/users` - View total user count
- `/allids` - List all user IDs
- `/broadcast` - Broadcast message to all users
- `/warn` - Send warning to specific user
- `/addpremium` - Upgrade user to premium
- `/ceasepower` - Downgrade user capacity
- `/resetpower` - Reset user to default plan
- `/restart` - Restart the bot

## 📊 Project Structure

```
Rename-Bot-4GB/
├── bot.py                 # Main bot file
├── config.py             # Configuration settings
├── app.py                # Flask web server
├── script.py             # Bot text messages
├── requirements.txt      # Python dependencies
├── helper/               # Helper modules
│   ├── database.py       # Database operations
│   ├── progress.py       # Progress tracking
│   ├── ffmpeg.py         # Media processing
│   └── set.py           # Utility functions
└── plugins/              # Bot command handlers
    ├── start.py          # Start command
    ├── admin.py          # Admin commands
    ├── broadcast.py      # Broadcast functionality
    ├── callback.py       # Callback handlers
    └── ...              # Other command handlers
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Credits & Support

### Developers
- [Jishu Developer](https://github.com/JishuDeveloper) - Lead Developer
- [Madflix Official](https://github.com/jishusinha) - Contributor
- [lntechnical](https://github.com/lntechnical2) - Contributor

### Channels & Support
- 📢 **Updates**: [Madflix Botz](https://t.me/Madflix_Bots)
- 🤖 **Bots**: [Jishu Botz](https://t.me/JishuBotz)
- 💬 **Support**: [Contact Developer](https://t.me/JishuDeveloper)

### Donations
If you find this project helpful, consider supporting the developer:

- 💳 **PayPal**: [Donate via PayPal](https://paypal.me/jishudeveloper/2.50USD)
- 📱 **UPI**: `madflixofficial@axl`
- 🔗 **Payment QR**: [View QR Codes](https://graph.org/QR-Payment-07-24-4)

## ⚠️ Disclaimer

This bot is for educational purposes. Please ensure you comply with Telegram's Terms of Service and respect copyright laws when using this bot.

---

<div align="center">
  <b>⭐ Star this repository if you found it helpful!</b>
  <br>
  Made with ❤️ by <a href="https://t.me/JishuDeveloper">Jishu Developer</a>
</div>
