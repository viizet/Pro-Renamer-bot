from config import *
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from helper.database import botdata, find_one, total_user, getid, get_user_statistics
from helper.progress import humanbytes

token = BOT_TOKEN
botid = token.split(':')[0]


# /users command removed - functionality moved to /stats (listall.py)uote=True, reply_markup=keyboard)


@Client.on_callback_query(filters.regex("refresh_stats"))
async def refresh_stats(client, callback_query):
    try:
        botdata(int(botid))
        data = find_one(int(botid))
        total_rename = data["total_rename"] if data and "total_rename" in data else 0
        total_size = data["total_size"] if data and "total_size" in data else 0
        
        # Get updated user statistics
        stats = get_user_statistics()
        
        text = f"""<b>📊 BOT STATISTICS</b>

<b>👥 USER STATISTICS:</b>
• <b>Total Users:</b> {stats['total_users']}
• <b>Premium Users:</b> {stats['premium_users']}
• <b>Free Users:</b> {stats['free_users']}
• <b>Banned Users:</b> {stats['banned_users']}

<b>📁 FILE STATISTICS:</b>
• <b>Total Files Renamed:</b> {total_rename}
• <b>Total Size Processed:</b> {humanbytes(int(total_size)) if total_size else "0 B"}

<b>🤖 Bot ID:</b> <code>{botid}</code>

<i>📊 Statistics refreshed!</i>"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")],
            [InlineKeyboardButton("🦋 Close 🦋", callback_data="cancel")]
        ])
        
        await callback_query.message.edit_text(text, reply_markup=keyboard)
        await callback_query.answer("✅ Statistics refreshed!")
    except Exception as e:
        await callback_query.answer(f"❌ Error refreshing: {str(e)}", show_alert=True)


