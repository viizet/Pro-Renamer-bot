# 🤖 Advanced Telegram File Renamer Bot

<div align="center">
  <img src="https://graph.org/file/ad48ac09b1e6f30d2dae4.jpg" alt="Bot Logo" width="200"/>
  
  [![Telegram](https://img.shields.io/badge/Telegram-@Madflix_Bots-blue?style=flat&logo=telegram)](https://t.me/Madflix_Bots)
  [![Support](https://img.shields.io/badge/Support-@MadflixBots_Support-red?style=flat&logo=telegram)](https://t.me/MadflixBots_Support)
  [![Developer](https://img.shields.io/badge/Developer-@MadflixOfficials-green?style=flat&logo=telegram)](https://t.me/MadflixOfficials)
</div>

## 📋 Table of Contents
- [Features](#-features)
- [Premium Features](#-premium-features)
- [User Commands](#-user-commands)
- [Admin Commands](#️-admin-commands)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Premium Plans](#-premium-plans)
- [Support](#-support)
- [Contributing](#-contributing)

## ✨ Features

### 🔧 Core Features
- **File Renaming**: Rename any file with custom names
- **Thumbnail Support**: Set custom thumbnails for videos and documents
- **Custom Captions**: Add personalized captions to your files
- **Format Conversion**: Convert videos to documents and vice versa
- **Metadata Editing**: Modify file metadata information
- **Flood Protection**: Smart flood control to prevent spam
- **User Management**: Comprehensive user tracking and management

### 📊 File Processing
- **Multi-Format Support**: Works with videos, documents, audio files
- **Size Optimization**: Efficient handling of large files
- **DC ID Detection**: Shows file datacenter information
- **Progress Tracking**: Real-time upload/download progress
- **File Validation**: Automatic file type detection and validation

### 🛡️ Security & Limits
- **Daily Limits**: Configurable daily upload limits per user
- **Premium Tiers**: Multiple subscription levels with different limits
- **Admin Controls**: Comprehensive admin panel for user management
- **Secure Database**: MongoDB integration for data persistence

## 🌟 Premium Features

### 🪙 Basic Plan (20GB)
- 20GB daily upload limit
- Priority processing
- Custom thumbnails
- Basic support

### ⚡ Standard Plan (50GB)
- 50GB daily upload limit
- Faster processing
- Advanced features
- Priority support

### 💎 Pro Plan (100GB)
- 100GB daily upload limit
- Fastest processing
- All premium features
- VIP support

## 👥 User Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/viewthumb` | View your current thumbnail |
| `/delthumb` | Delete your current thumbnail |
| `/set_caption` | Set a custom caption for files |
| `/see_caption` | View your current caption |
| `/del_caption` | Delete your custom caption |
| `/ping` | Check bot response time |
| `/myplan` | View your current subscription plan |
| `/upgrade` | View available premium plans |
| `/donate` | Support the developer |

## 🔧 Admin Commands

| Command | Description |
|---------|-------------|
| `/users` | View total user count and statistics |
| `/allids` | List all user IDs |
| `/allcommand` | Show all available bot commands |
| `/broadcast` | Send message to all users |
| `/warn` | Send warning to specific user |
| `/addpremium` | Upgrade user to premium plan |
| `/ceasepower` | Downgrade user capacity |
| `/resetpower` | Reset user to default plan |
| `/restart` | Restart the bot |

## 🚀 Installation

### Prerequisites
- Python 3.8+
- MongoDB Database
- Telegram Bot Token
- API ID & Hash from my.telegram.org

### Quick Deploy on Replit
1. Fork this repository
2. Set up environment variables
3. Run the bot

### Manual Installation
```bash
git clone https://github.com/YourUsername/Telegram-File-Renamer-Bot
cd Telegram-File-Renamer-Bot
pip install -r requirements.txt
python bot.py
```

## ⚙️ Configuration

### Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Your API ID from my.telegram.org | Yes |
| `API_HASH` | Your API Hash from my.telegram.org | Yes |
| `BOT_TOKEN` | Bot token from @BotFather | Yes |
| `ADMIN` | Admin user ID | Yes |
| `DATABASE_URL` | MongoDB connection string | Yes |
| `LOG_CHANNEL` | Log channel ID | Yes |

### Optional Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `STRING_SESSION` | Premium client session for 4GB+ files | No |
| `FORCE_SUBS` | Force subscription channel username | No |
| `DATABASE_NAME` | Custom database name | No |
| `START_PIC` | Custom start image URL | No |

### Example .env file
```env
API_ID=1234567
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
ADMIN=123456789
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/
LOG_CHANNEL=-1001234567890
STRING_SESSION=optional_session_string
```

## 💰 Premium Plans

### Free Plan
- ✅ 2GB daily limit
- ✅ Basic renaming
- ✅ Thumbnail support
- ✅ Community support

### Paid Plans
- **Basic (🪙)**: 20GB daily limit
- **Standard (⚡)**: 50GB daily limit  
- **Pro (💎)**: 100GB daily limit

## 🛠️ Technical Details

### Architecture
- **Framework**: Pyrogram (MTProto API)
- **Database**: MongoDB with PyMongo
- **File Handling**: Custom progress tracking
- **Deployment**: Docker & Replit ready

### File Size Limits
- **Free Users**: Up to 2GB per file
- **Premium Users**: Up to 4GB per file (with string session)
- **Daily Limits**: Based on subscription plan

### Performance
- **Concurrent Processing**: Multi-threaded file handling
- **Memory Optimization**: Efficient large file processing
- **Error Handling**: Comprehensive error management

## 📊 Statistics & Monitoring

- Real-time user statistics
- File processing analytics
- Daily usage tracking
- Admin dashboard
- Comprehensive logging

## 🔒 Security Features

- User authentication
- Rate limiting
- Flood protection
- Admin-only commands
- Secure session handling

## 🐛 Known Issues

- Large file processing may take time
- Some file formats may not be supported
- Thumbnail generation depends on file type

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

- **Updates Channel**: [@Madflix_Bots](https://t.me/Madflix_Bots)
- **Support Group**: [@MadflixBots_Support](https://t.me/MadflixBots_Support)
- **Developer**: [@MadflixOfficials](https://t.me/MadflixOfficials)

## 🙏 Credits

- **Developer**: [@JishuDeveloper](https://t.me/JishuDeveloper) & [@MadflixOfficials](https://t.me/MadflixOfficials)
- **Framework**: [Pyrogram](https://pyrogram.org/)
- **Database**: [MongoDB](https://www.mongodb.com/)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

<div align="center">
  <b>Made with ❤️ by <a href="https://t.me/MadflixOfficials">@MadflixOfficials</a></b>
</div>
