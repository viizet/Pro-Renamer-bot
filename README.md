
# 🤖 Telegram File Renamer Bot

A powerful Telegram bot for renaming files with custom thumbnails, captions, and comprehensive user management system with advanced premium features.

## ✨ Features

- **File Renaming**: Rename any file type with custom names
- **Custom Thumbnails**: Set thumbnails for videos and documents  
- **Custom Captions**: Add personalized captions to files
- **Format Conversion**: Convert videos to documents and vice versa
- **Premium Plans**: Multiple subscription tiers with different limits
- **Admin Controls**: Comprehensive user management with ban/unban functionality
- **Detailed Statistics**: Real-time user statistics with refresh functionality
- **Free Premium System**: Automated premium distribution with smart exclusions
- **User Ban System**: Ban/unban users with reasons and notifications
- **Metadata Support**: Custom metadata for processed files

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
- `/addpremium` - Upgrade user to premium plan (paid premium)
- `/removepremium <user_id>` - Remove paid premium from specific user
- `/free` - Manage free premium system settings
- `/removefree <user_id>` - Remove free premium from specific user

### System Commands
- `/admin` - Show admin control panel with interactive buttons
- `/allcommand` - Display all available commands
- `/restart` - Restart the bot (cancels all processes)

## 💎 Premium Plans

- **🆓 Free**: 2GB daily upload limit
- **🪙 Basic**: 20GB daily upload limit
- **⚡ Standard**: 50GB daily upload limit  
- **💎 Pro**: 100GB daily upload limit

### Premium Benefits
- ✅ High priority processing
- ✅ Upload large files (up to 4GB for premium users)
- ✅ No timeout delays
- ✅ Unlimited parallel processing
- ✅ Custom metadata support
- ✅ Premium badge display

## 📊 Bot Statistics Features

The `/users` command provides comprehensive statistics:
- **Total Users**: Complete user count
- **Premium Users**: Users with active premium plans
- **Free Users**: Users on free plan
- **Banned Users**: Number of banned users
- **File Statistics**: Total files processed and data handled
- **Refresh Button**: Real-time statistics updates with cooldown protection

## 🚫 Ban System

Admins can manage user access with:
- **Ban with Reason**: `/ban <user_id> <reason>`
- **Unban Users**: `/unban <user_id>`
- **Automatic Notifications**: Users are notified when banned/unbanned
- **Reason Tracking**: Ban reasons are stored and displayed
- **Access Blocking**: Banned users cannot use any bot features

## 🎁 Free Premium System

### Smart Premium Distribution
- **Free Users Only**: Only applies to users with "Free" usertype
- **Paid User Exclusion**: Never applies to users added with `/addpremium`
- **Automatic Application**: New free users get free premium automatically
- **Configurable Plans**: Admin can set plan type and duration

### Free Premium Management
- **Global Control**: Enable/disable free premium for new users
- **Individual Removal**: Remove free premium from specific users
- **Mass Removal**: "Remove Free Premium from All" button (excludes paid users)
- **Plan Tracking**: Separate tracking of free vs paid premium status

### Key Rules
1. **Free Premium** = Only for free users (Standard, Basic, or Pro trial users)
2. **Paid Premium** = Users added with `/addpremium` (excluded from free premium)
3. **Removal Commands**:
   - `/removefree` - Removes free premium only
   - `/removepremium` - Removes paid premium only

## 🛠️ Tech Stack

- **Framework**: Pyrogram v2
- **Database**: MongoDB with advanced aggregation
- **Language**: Python 3.12+
- **Deployment**: Replit Ready
- **File Handling**: FFmpeg integration
- **Web Server**: Flask for health checks

## 📁 Project Structure

```
├── bot.py              # Main bot file with Flask integration
├── config.py           # Configuration settings
├── script.py           # Text templates and messages
├── helper/
│   ├── database.py     # Database operations with premium logic
│   ├── progress.py     # Upload/download progress tracking
│   ├── date.py         # Date utilities for premium expiry
│   └── ffmpeg.py       # Media processing
├── plugins/
│   ├── start.py        # Start command and file handling
│   ├── admin.py        # Admin commands with interactive panel
│   ├── totalusers.py   # User statistics with refresh
│   ├── freepremium.py  # Free premium management system
│   ├── myplan.py       # User plan display with premium badges
│   ├── top10.py        # Top users ranking
│   └── ...             # Other plugin files
└── README.md
```

## 🔒 Security Features

- **User Ban System**: Complete access restriction with reason tracking
- **Premium Separation**: Clear distinction between free and paid premium
- **Admin-Only Commands**: Restricted access to administrative functions
- **Database Security**: Secure MongoDB operations with error handling
- **Environment Protection**: All sensitive data in environment variables

## 📱 Interactive Features

### Admin Panel (`/admin`)
- **Statistics View**: Real-time bot statistics with refresh button
- **User Management**: Quick access to user management commands
- **Premium Control**: Premium management shortcuts
- **System Controls**: Restart and broadcast functionality

### Premium Display
- **Plan Badges**: Visual indicators for premium users
- **Usage Tracking**: Daily upload limit monitoring
- **Expiry Dates**: Clear premium expiration information
- **Free vs Paid**: Distinguished premium types in user interface

## 📞 Support & Links

- **Developer**: [@viizet](https://t.me/viizet)
- **Channel**: [@Phioza](https://t.me/Phioza)
- **Support**: [@Phioza](https://t.me/Phioza)

## 🚀 Getting Started

1. **Deploy on Replit**: Fork this repository to your Replit account
2. **Set Environment Variables**: Add all required variables in Replit Secrets
3. **Configure Database**: Set up MongoDB connection
4. **Start the Bot**: Click the Run button to start
5. **Set Admin Access**: Add your user ID to ADMIN variable
6. **Configure Premium**: Set up free premium system as needed

## ⚡ Bot Performance

- **High Availability**: Flask health check server on port 5000
- **Error Handling**: Comprehensive error handling and logging
- **Database Optimization**: Efficient MongoDB queries with indexing
- **Memory Management**: Optimized file processing for large files
- **Concurrent Processing**: Supports multiple users simultaneously

## 🔄 Updates & Maintenance

- **Auto-restart**: Bot automatically restarts on crashes
- **Real-time Statistics**: Live user and file statistics
- **Database Backups**: Regular MongoDB backups recommended
- **Log Monitoring**: Comprehensive logging for debugging

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

Made with ❤️ by [@viizet](https://t.me/viizet)

---

**⚠️ Important Notes**:
- Keep your bot token and database credentials secure
- Regular database backups are recommended
- Monitor bot performance through the admin panel
- Free premium system automatically excludes paid users
- Use `/removepremium` only for paid premium users
