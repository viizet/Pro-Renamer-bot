# 🤖 Telegram File Renamer Bot

A powerful Telegram bot for renaming files with custom thumbnails, premium features, and comprehensive user management.

## ✨ Features

🚀 **Fast File Renaming** - Rename files quickly and efficiently  
📁 **4GB File Support** - Handle large files with premium upgrade  
🖼️ **Custom Thumbnails** - Set permanent custom thumbnails  
📝 **Custom Captions** - Add personalized captions to files  
📢 **Broadcast System** - Send messages to all users (Admin only)  
🔄 **File Conversion** - Convert between video and file formats  
⚡ **Unlimited Renaming** - No limits on concurrent operations  
🎨 **Custom Start Picture** - Personalized bot interface  
💎 **Premium Plans** - Multiple subscription tiers (Free, Basic, Standard, Pro)  
🛡️ **Admin Controls** - User management with ban/unban functionality  
📊 **Statistics Dashboard** - Real-time user statistics with refresh  
🎁 **Free Premium System** - Automated premium distribution

## 🚀 Hosting Platforms

✅ **This bot works on multiple hosting platforms:**

- **🟢 Replit** - Ready to deploy (current platform)
- **🟣 Render** - Configured with Procfile
- **🟡 Heroku** - Configured with app.json and buildpacks
- **🔵 Docker** - Dockerfile and docker-compose included
- **⚫ VPS/Cloud** - Works on any Linux server

## 🚀 Quick Setup

### For Replit:
1. **Fork** this repository to Replit
2. **Configure** environment variables in Secrets tab
3. **Click Run** to start the bot

### For Render/Heroku:
1. **Deploy** using the respective platform's deployment methods
2. **Set** environment variables in platform settings
3. **Start** the worker process automatically

### For Docker/VPS:
1. **Clone** the repository
2. **Install** dependencies: `pip install -r requirements.txt`
3. **Set** environment variables
4. **Run** with: `python3 bot.py`

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

- **🆓 Free** - 15GB daily upload limit, 2GB max file size
- **🪙 Basic** - 60GB daily upload limit, 2GB max file size
- **⚡ Standard** - 60GB daily upload limit, 4GB max file size  
- **💎 Pro** - 150GB daily upload limit, 4GB max file size

### Premium Benefits
✅ High priority processing • ✅ Upload large files (4GB for Standard/Pro) • ✅ No timeout delays • ✅ Unlimited parallel processing

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

- **Developer:** [@VIIZET](https://t.me/VIIZET)
- **Channel:** [@Phioza](https://t.me/Phioza)
- **Support:** [@Phioza](https://t.me/Phioza)

## 🚀 Getting Started

### Platform-Specific Instructions:

**Replit:**
1. **Deploy** - Fork to Replit and set environment variables in Secrets
2. **Configure** - Set up MongoDB connection
3. **Start** - Click Run button

**Render:**
1. **Connect** your GitHub repository to Render
2. **Set** environment variables in Render dashboard
3. **Deploy** - Automatic deployment with Procfile configuration

**Heroku:**
1. **Deploy** using Heroku CLI or GitHub integration
2. **Configure** environment variables via Heroku Config Vars
3. **Enable** worker dyno for bot operation

**Docker/VPS:**
1. **Clone** repository and install dependencies
2. **Set** environment variables in system or .env file
3. **Run** with `python3 bot.py` or use Docker containers

### Common Setup:
1. **Admin** - Add your user ID to ADMIN variable
2. **Premium** - Configure free premium system as needed

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits

Made with ❤️ by [@VIIZET](https://t.me/VIIZET)

---

⚠️ **Important:** Keep credentials secure • Regular database backups recommended • Monitor performance through admin panel
