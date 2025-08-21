
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import find_one, dbcol
from helper.progress import humanbytes

@Client.on_message(filters.command(["top10"]))
async def top10_users(bot, message):
    try:
        # Get top 10 users by total renamed files (uploads)
        pipeline = [
            {"$match": {"_id": {"$ne": "free_premium_config"}}},
            {"$addFields": {
                "total_rename_int": {"$toInt": {"$ifNull": ["$total_rename", "0"]}},
                "used_limit_int": {"$toInt": {"$ifNull": ["$used_limit", "0"]}}
            }},
            {"$sort": {"total_rename_int": -1, "used_limit_int": -1}},
            {"$limit": 10}
        ]
        top_users = list(dbcol.aggregate(pipeline))
        
        if not top_users:
            await message.reply_text("❌ No users found!")
            return
            
        text = "🏆 **TOP 10 USERS BY FILE UPLOADS**\n\n"
        for i, user in enumerate(top_users, 1):
            user_id = user.get("_id", "Unknown")
            total_rename = user.get("total_rename", 0)
            used_limit = user.get("used_limit", 0)
            user_type = user.get("usertype", "Free")
            
            # Convert to int if string
            if isinstance(total_rename, str):
                total_rename = int(total_rename) if total_rename.isdigit() else 0
            if isinstance(used_limit, str):
                used_limit = int(used_limit) if used_limit.isdigit() else 0
            
            # Try to get user info (only show first name for privacy)
            try:
                user_info = await bot.get_users(user_id)
                name = user_info.first_name[:15] + "..." if len(user_info.first_name) > 15 else user_info.first_name
            except:
                name = "Unknown User"
            
            text += f"**{i}.** {name}\n"
            text += f"   **📁 Files Uploaded:** {total_rename}\n"
            text += f"   **📊 Data Used:** {humanbytes(used_limit)}\n"
            text += f"   **👤 Plan:** {user_type}\n\n"
        
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])
        
        await message.reply_text(text, reply_markup=button, quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Viizet Developer 
# Telegram Channel @Phioza
# Developer @viizet
