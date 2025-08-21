#
# 🤖 Telegram File Renamer Bot

A powerful Telegram bot for renaming files with custom thumbnails and captions.

## ✨ Features

- **File Renaming**: Rename any file type with custom names
- **Custom Thumbnails**: Set thumbnails for videos and documents  
- **Custom Captions**: Add personalized captions to files
- **Format Conversion**: Convert videos to documents and vice versa
- **Premium Plans**: Multiple subscription tiers with different limits
- **Admin Controls**: Comprehensive user management system

## 🚀 Quick Deploy on Replit

1. Fork this repository to Replit
2. Set up your environment variables
3. Click Run to start the bot

## ⚙️ Environment Variables

Create a `.env` file with these required variables:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
ADMIN=your_admin_user_id
DATABASE_URL=your_mongodb_url
LOG_CHANNEL=your_log_channel_id
```

Optional variables:
```env
STRING_SESSION=session_for_4gb_files
FORCE_SUBS=force_subscription_channel
START_PIC=custom_start_image_url
```

## 👥 User Commands

- `/start` - Start the bot
- `/viewthumb` - View current thumbnail
- `/delthumb` - Delete thumbnail
- `/set_caption` - Set custom caption
- `/see_caption` - View current caption
- `/del_caption` - Delete caption
- `/myplan` - View subscription plan
- `/upgrade` - View premium plans
- `/Help` - Get help
- `/ping` - Check bot status

## 🔧 Admin Commands

- `/users` - View total users
- `/broadcast` - Send message to all users
- `/warn <user_id> <message>` - Warn specific user
- `/addpremium` - Upgrade user to premium
- `/ceasepower` - Downgrade user
- `/resetpower` - Reset user to default
- `/top10` - View top 10 most active users
- `/free` - Manage free premium
- `/admin` - Show admin panel
- `/removefree` - Remove free premium from user
- `/allcommand` - Show all commands

## 💎 Premium Plans

- **Free**: 2GB daily limit
- **Basic 🪙**: 20GB daily limit
- **Standard ⚡**: 50GB daily limit
- **Pro 💎**: 100GB daily limit

## 🛠️ Tech Stack

- **Framework**: Pyrogram
- **Database**: MongoDB
- **Language**: Python 3.8+
- **Deployment**: Replit Ready

## 📞 Support

- **Owner**: @viizet
- **Channel**: @Phioza

---

Made with ❤️ by @viizet
