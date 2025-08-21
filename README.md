# 🤖 Telegram File Renamer Bot

A powerful Telegram bot for renaming files with custom thumbnails, captions, and comprehensive user management system.

## ✨ Features

- **File Renaming**: Rename any file type with custom names
- **Custom Thumbnails**: Set thumbnails for videos and documents  
- **Custom Captions**: Add personalized captions to files
- **Format Conversion**: Convert videos to documents and vice versa
- **Premium Plans**: Multiple subscription tiers with different limits
- **Admin Controls**: Comprehensive user management with ban/unban functionality
- **Detailed Statistics**: Real-time user statistics with refresh functionality
- **Free Premium System**: Automated premium distribution for new users
- **User Ban System**: Ban/unban users with reasons and notifications

## 🚀 Quick Deploy on Replit

1. Fork this repository to Replit
2. Set up your environment variables in the Secrets tab
3. Click Run to start the bot

## ⚙️ Environment Variables

Required variables (add these in Replit Secrets):

```env
API_ID=your_api_id_from_my.telegram.org
API_HASH=your_api_hash_from_my.telegram.org
BOT_TOKEN=your_bot_token_from_botfather
ADMIN=your_admin_user_id
DATABASE_URL=your_mongodb_connection_url
DATABASE_NAME=your_database_name
LOG_CHANNEL=your_log_channel_id
```

Optional variables:
```env
STRING_SESSION=session_for_4gb_files
FORCE_SUB=force_subscription_channel_username
START_PIC=custom_start_image_url
```

## 👥 User Commands

- `/start` - Start the bot and view welcome message
- `/viewthumb` - View your current thumbnail
- `/delthumb` - Delete your current thumbnail
- `/set_caption` - Set custom caption for files
- `/see_caption` - View your current caption
- `/del_caption` - Delete your current caption
- `/myplan` - View your subscription plan details
- `/upgrade` - View available premium plans
- `/help` - Get detailed help information
- `/ping` - Check bot response time and status

## 🔧 Admin Commands

### User Management
- `/users` - View detailed bot statistics with real-time refresh
- `/broadcast` - Send message to all bot users
- `/warn <user_id> <message>` - Send warning to specific user
- `/ban <user_id> <reason>` - Ban user with specified reason
- `/unban <user_id>` - Unban previously banned user
- `/top10` - View top 10 most active users

### Premium Management
- `/addpremium` - Upgrade user to premium plan
- `/free` - Manage free premium system settings
- `/removefree` - Remove free premium from specific user

### System Commands
- `/admin` - Show admin control panel
- `/allcommand` - Display all available commands
- `/restart` - Restart the bot (cancels all processes)

## 💎 Premium Plans

- **🆓 Free**: 2GB daily upload limit
- **🪙 Basic**: 20GB daily upload limit - $0.50/month
- **⚡ Standard**: 50GB daily upload limit - $1.50/month
- **💎 Pro**: 100GB daily upload limit - $3.00/month

### Premium Benefits
- ✓ High priority processing
- ✓ Upload large files (up to 4GB for premium users)
- ✓ No timeout delays
- ✓ Unlimited parallel processing
- ✓ Custom metadata support

## 📊 Bot Statistics Features

The `/users` command provides comprehensive statistics:
- **Total Users**: Complete user count
- **Premium Users**: Users with active premium plans
- **Free Users**: Users on free plan
- **Banned Users**: Number of banned users
- **File Statistics**: Total files processed and data handled
- **Refresh Button**: Real-time statistics updates

## 🚫 Ban System

Admins can manage user access with:
- **Ban with Reason**: `/ban <user_id> <reason>`
- **Unban Users**: `/unban <user_id>`
- **Automatic Notifications**: Users are notified when banned/unbanned
- **Reason Tracking**: Ban reasons are stored and displayed

## 🎁 Free Premium System

- Automatic premium assignment for new users
- Configurable plan types and durations
- Apply to existing users or new registrations only
- Easy management through admin commands

## 🛠️ Tech Stack

- **Framework**: Pyrogram v2
- **Database**: MongoDB
- **Language**: Python 3.12+
- **Deployment**: Replit Ready
- **File Handling**: FFmpeg integration

## 📁 Project Structure

```
├── bot.py              # Main bot file
├── config.py           # Configuration settings
├── script.py           # Text templates
├── helper/
│   ├── database.py     # Database operations
│   ├── progress.py     # Upload/download progress
│   └── ffmpeg.py       # Media processing
├── plugins/
│   ├── start.py        # Start command and file handling
│   ├── admin.py        # Admin commands
│   ├── totalusers.py   # User statistics
│   ├── freepremium.py  # Free premium system
│   └── ...             # Other plugin files
└── README.md
```

## 🔒 Security Features

- User ban system with reason tracking
- Admin-only command restrictions
- Secure database operations
- Environment variable protection

## 📞 Support & Links

- **Developer**: [@viizet](https://t.me/viizet)
- **Channel**: [@Phioza](https://t.me/Phioza)
- **Support**: [@Phioza](https://t.me/Phioza)

## 🚀 Getting Started

1. **Clone/Fork** this repository to Replit
2. **Set Environment Variables** in Replit Secrets
3. **Install Dependencies** (automatic on Replit)
4. **Run the Bot** using the Run button
5. **Set Admin** by adding your user ID to ADMIN variable
6. **Configure Premium** plans and free premium settings

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

Made with ❤️ by [@viizet](https://t.me/viizet)

---

**⚠️ Note**: Make sure to keep your bot token and database credentials secure. Never share them publicly.
