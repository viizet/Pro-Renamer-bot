# 🤖 Telegram File Renamer Bot

A powerful Telegram bot for renaming files with custom thumbnails, premium features, and comprehensive user management.

## ✨ Features

- **File Renaming** - Rename any file type with custom names
- **Custom Thumbnails** - Set thumbnails for videos and documents  
- **Custom Captions** - Add personalized captions to files
- **Format Conversion** - Convert videos to documents and vice versa
- **Premium Plans** - Multiple subscription tiers (Free, Basic, Standard, Pro)
- **Admin Controls** - User management with ban/unban functionality
- **Statistics Dashboard** - Real-time user statistics with refresh
- **Free Premium System** - Automated premium distribution

## 🚀 Quick Setup

1. **Fork** this repository to Replit
2. **Configure** environment variables in Secrets tab
3. **Click Run** to start the bot

## ⚙️ Environment Variables

**Required:**
```env
API_ID=your_api_id_from_my.telegram.org
API_HASH=your_api_hash_from_my.telegram.org
BOT_TOKEN=your_bot_token_from_botfather
ADMIN=your_admin_user_id
DATABASE_URL=your_mongodb_connection_url
DATABASE_NAME=your_database_name
LOG_CHANNEL=your_log_channel_id
```

**Optional:**
```env
STRING_SESSION=session_for_4gb_files
FORCE_SUB=force_subscription_channel
START_PIC=custom_start_image_url
```

## 💎 Premium Plans

- **🆓 Free** - 2GB daily upload limit
- **🪙 Basic** - 20GB daily upload limit
- **⚡ Standard** - 50GB daily upload limit  
- **💎 Pro** - 100GB daily upload limit

### Premium Benefits
✅ High priority processing • ✅ Upload large files (4GB) • ✅ No timeout delays • ✅ Unlimited parallel processing

## 👥 User Commands

- `/start` - Start the bot
- `/viewthumb` / `/delthumb` - Manage thumbnails
- `/set_caption` / `/del_caption` - Manage captions
- `/myplan` - View subscription details
- `/upgrade` - View premium plans
- `/help` - Get help information
- `/ping` - Check bot status

## 🔧 Admin Commands

**User Management:**
- `/users` - View bot statistics
- `/ban` / `/unban` - Manage user access
- `/broadcast` - Send message to all users
- `/top10` - View most active users

**Premium Management:**
- `/addpremium` - Add paid premium
- `/removepremium` - Remove paid premium
- `/free` - Manage free premium system
- `/removefree` - Remove free premium

**System:**
- `/admin` - Admin control panel
- `/restart` - Restart bot

## 🛠️ Tech Stack

- **Framework:** Pyrogram v2
- **Database:** MongoDB
- **Language:** Python 3.12+
- **Deployment:** Replit Ready
- **Web Server:** Flask health checks

## 🔒 Security Features

- **User Ban System** - Complete access restriction
- **Premium Separation** - Free vs paid premium tracking
- **Admin Protection** - Restricted administrative functions
- **Environment Security** - All sensitive data in environment variables

## 📊 Bot Statistics

The admin panel provides:
- **User Counts** - Total, premium, free, and banned users
- **File Statistics** - Total files processed and data handled
- **Real-time Updates** - Refresh functionality with cooldown protection

## 📱 Key Features

### Free Premium System
- **Smart Distribution** - Only applies to free users
- **Paid User Exclusion** - Never affects users added with `/addpremium`
- **Automatic Application** - New users get free premium automatically

### Interactive Admin Panel
- **Statistics View** - Real-time bot statistics
- **Quick Actions** - User management shortcuts
- **System Controls** - Restart and broadcast functionality

## 📞 Support

- **Developer:** [@viizet](https://t.me/viizet)
- **Channel:** [@Phioza](https://t.me/Phioza)
- **Support:** [@Phioza](https://t.me/Phioza)

## 🚀 Getting Started

1. **Deploy** - Fork to Replit and set environment variables
2. **Configure** - Set up MongoDB connection
3. **Start** - Click Run button
4. **Admin** - Add your user ID to ADMIN variable
5. **Premium** - Configure free premium system as needed

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits

Made with ❤️ by [@viizet](https://t.me/viizet)

---

⚠️ **Important:** Keep credentials secure • Regular database backups recommended • Monitor performance through admin panel
