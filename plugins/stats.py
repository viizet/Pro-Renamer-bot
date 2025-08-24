

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN
from helper.database import find_one, getid, get_user_statistics
from helper.progress import humanbytes

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["stats"]))
async def stats_menu(bot, message):
    """Main listall menu with user category buttons"""
    stats = get_user_statistics()
    
    status_text = f"""**📊 USER MANAGEMENT PANEL**

**Total Statistics:**
👥 Total Users: {stats['total_users']}
💎 Premium Users: {stats['premium_users']}
🆓 Free Users: {stats['free_users']}
🚫 Banned Users: {stats['banned_users']}

**Select category to view users:**"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Paid Premium Users", callback_data="list_paid_premium")],
        [InlineKeyboardButton("🎁 Free Premium Users", callback_data="list_free_premium")],
        [InlineKeyboardButton("🆓 Free Users", callback_data="list_free_users")],
        [InlineKeyboardButton("🚫 Banned Users", callback_data="list_banned_users")],
        [InlineKeyboardButton("📊 All Users", callback_data="list_all_users")],
        [InlineKeyboardButton("🔄 Refresh Stats", callback_data="refresh_listall")],
        [InlineKeyboardButton("❌ Close", callback_data="cancel")]
    ])

    await message.reply_text(status_text, reply_markup=keyboard, quote=True)

@Client.on_callback_query(filters.regex("list_paid_premium"))
async def list_paid_premium(bot, update):
    """List all paid premium users"""
    user_ids = getid()
    paid_premium_users = []
    
    for user_id in user_ids:
        if user_id != "free_premium_config":
            user_data = find_one(user_id)
            if user_data and user_data.get("paid_premium", False):
                user_type = user_data.get("usertype", "Unknown")
                used = user_data.get("used_limit", 0)
                limit = user_data.get("uploadlimit", 0)
                paid_premium_users.append(f"• `{user_id}` - {user_type} - Used: {humanbytes(used)}/{humanbytes(limit)}")
    
    if not paid_premium_users:
        text = "**💎 PAID PREMIUM USERS**\n\nNo paid premium users found."
    else:
        text = f"**💎 PAID PREMIUM USERS ({len(paid_premium_users)})**\n\n" + "\n".join(paid_premium_users[:20])
        if len(paid_premium_users) > 20:
            text += f"\n\n... and {len(paid_premium_users) - 20} more users"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
    ])
    
    await update.message.edit_text(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_free_premium"))
async def list_free_premium(bot, update):
    """List all free premium users"""
    user_ids = getid()
    free_premium_users = []
    
    for user_id in user_ids:
        if user_id != "free_premium_config":
            user_data = find_one(user_id)
            if user_data and user_data.get("free_premium", False) and not user_data.get("paid_premium", False):
                user_type = user_data.get("usertype", "Unknown")
                used = user_data.get("used_limit", 0)
                limit = user_data.get("uploadlimit", 0)
                free_premium_users.append(f"• `{user_id}` - {user_type} - Used: {humanbytes(used)}/{humanbytes(limit)}")
    
    if not free_premium_users:
        text = "**🎁 FREE PREMIUM USERS**\n\nNo free premium users found."
    else:
        text = f"**🎁 FREE PREMIUM USERS ({len(free_premium_users)})**\n\n" + "\n".join(free_premium_users[:20])
        if len(free_premium_users) > 20:
            text += f"\n\n... and {len(free_premium_users) - 20} more users"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
    ])
    
    await update.message.edit_text(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_free_users"))
async def list_free_users(bot, update):
    """List all free users"""
    user_ids = getid()
    free_users = []
    
    for user_id in user_ids:
        if user_id != "free_premium_config":
            user_data = find_one(user_id)
            if user_data and user_data.get("usertype") == "Free" and not user_data.get("free_premium", False) and not user_data.get("paid_premium", False):
                used = user_data.get("used_limit", 0)
                limit = user_data.get("uploadlimit", 0)
                free_users.append(f"• `{user_id}` - Free - Used: {humanbytes(used)}/{humanbytes(limit)}")
    
    if not free_users:
        text = "**🆓 FREE USERS**\n\nNo free users found."
    else:
        text = f"**🆓 FREE USERS ({len(free_users)})**\n\n" + "\n".join(free_users[:20])
        if len(free_users) > 20:
            text += f"\n\n... and {len(free_users) - 20} more users"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
    ])
    
    await update.message.edit_text(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_banned_users"))
async def list_banned_users(bot, update):
    """List all banned users"""
    user_ids = getid()
    banned_users = []
    
    for user_id in user_ids:
        if user_id != "free_premium_config":
            user_data = find_one(user_id)
            if user_data and user_data.get("banned", False):
                ban_reason = user_data.get("ban_reason", "No reason")
                user_type = user_data.get("usertype", "Unknown")
                banned_users.append(f"• `{user_id}` - {user_type} - Reason: {ban_reason}")
    
    if not banned_users:
        text = "**🚫 BANNED USERS**\n\nNo banned users found."
    else:
        text = f"**🚫 BANNED USERS ({len(banned_users)})**\n\n" + "\n".join(banned_users[:20])
        if len(banned_users) > 20:
            text += f"\n\n... and {len(banned_users) - 20} more users"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
    ])
    
    await update.message.edit_text(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_all_users"))
async def list_all_users(bot, update):
    """List all users with their status"""
    user_ids = getid()
    all_users = []
    
    for user_id in user_ids:
        if user_id != "free_premium_config":
            user_data = find_one(user_id)
            if user_data:
                user_type = user_data.get("usertype", "Unknown")
                is_banned = user_data.get("banned", False)
                is_paid_premium = user_data.get("paid_premium", False)
                is_free_premium = user_data.get("free_premium", False)
                
                status = "🚫 Banned" if is_banned else (
                    "💎 Paid Premium" if is_paid_premium else (
                        "🎁 Free Premium" if is_free_premium else "🆓 Free"
                    )
                )
                
                used = user_data.get("used_limit", 0)
                limit = user_data.get("uploadlimit", 0)
                all_users.append(f"• `{user_id}` - {status} - {user_type} - {humanbytes(used)}/{humanbytes(limit)}")
    
    if not all_users:
        text = "**📊 ALL USERS**\n\nNo users found."
    else:
        text = f"**📊 ALL USERS ({len(all_users)})**\n\n" + "\n".join(all_users[:15])
        if len(all_users) > 15:
            text += f"\n\n... and {len(all_users) - 15} more users"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
    ])
    
    await update.message.edit_text(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("refresh_listall"))
async def refresh_listall(bot, update):
    """Refresh the listall menu"""
    stats = get_user_statistics()
    
    status_text = f"""**📊 USER MANAGEMENT PANEL**

**Total Statistics:**
👥 Total Users: {stats['total_users']}
💎 Premium Users: {stats['premium_users']}
🆓 Free Users: {stats['free_users']}
🚫 Banned Users: {stats['banned_users']}

**Select category to view users:**"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Paid Premium Users", callback_data="list_paid_premium")],
        [InlineKeyboardButton("🎁 Free Premium Users", callback_data="list_free_premium")],
        [InlineKeyboardButton("🆓 Free Users", callback_data="list_free_users")],
        [InlineKeyboardButton("🚫 Banned Users", callback_data="list_banned_users")],
        [InlineKeyboardButton("📊 All Users", callback_data="list_all_users")],
        [InlineKeyboardButton("🔄 Refresh Stats", callback_data="refresh_listall")],
        [InlineKeyboardButton("❌ Close", callback_data="cancel")]
    ])

    await update.message.edit_text(status_text, reply_markup=keyboard)

# Developer @viizet
