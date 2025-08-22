from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config import *
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre, botdata, find_one, get_user_statistics
from helper.progress import humanbytes
import asyncio

token = BOT_TOKEN
botid = token.split(':')[0]





@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
async def warn(c, m):
    if len(m.command) < 3:
        await m.reply_text("**Usage:** /warn <user_id> <message>\n\n**Example:** `/warn 123456789 Please follow bot rules`")
        return

    try:
        user_id = int(m.command[1])
        reason = " ".join(m.command[2:])

        # First check if user exists in database
        from helper.database import find_one
        user_data = find_one(user_id)
        if not user_data:
            await m.reply_text(f"❌ User {user_id} not found in database!\n\nThe user must start the bot first before you can warn them.")
            return

        # Try to get user info to verify the user exists
        try:
            user_info = await c.get_users(user_id)
            user_name = user_info.first_name
        except Exception:
            await m.reply_text(f"❌ Invalid user ID {user_id}!\n\nMake sure the user ID is correct and the user has interacted with the bot.")
            return

        # Send warning message
        try:
            await c.send_message(
                chat_id=user_id, 
                text=f"⚠️ **Warning from Admin (@viizet):**\n\n{reason}\n\n**Note:** Please follow bot rules to avoid restrictions."
            )
            await m.reply_text(f"✅ Warning sent successfully to {user_name} ({user_id})!")
        except Exception as send_error:
            if "PEER_ID_INVALID" in str(send_error):
                await m.reply_text(f"❌ Cannot send message to user {user_id}!\n\n**Reason:** The user hasn't started the bot or has blocked it.\n\n**Solution:** Ask the user to start the bot first: /start")
            else:
                await m.reply_text(f"❌ Failed to send warning: {str(send_error)}")

    except ValueError:
        await m.reply_text("❌ Invalid user ID format!\n\n**Usage:** `/warn <user_id> <message>`\n**Example:** `/warn 123456789 Please follow rules`")
    except Exception as e:
        await m.reply_text(f"❌ Unexpected error: {str(e)}")


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["ban"]))
async def ban_user_cmd(bot, message):
    if len(message.command) < 3:
        await message.reply_text("**Usage:** /ban <user_id> <reason>\n\n**Example:** `/ban 123456789 Spamming the bot`")
        return

    try:
        user_id = int(message.command[1])
        reason = " ".join(message.command[2:])

        # First check if user exists in database
        from helper.database import find_one, ban_user
        user_data = find_one(user_id)
        if not user_data:
            await message.reply_text(f"❌ User {user_id} not found in database!\n\nThe user must start the bot first before you can ban them.")
            return

        # Check if user is already banned
        if user_data.get("banned", False):
            await message.reply_text(f"⚠️ User {user_id} is already banned!")
            return

        # Try to get user info to verify the user exists
        try:
            user_info = await bot.get_users(user_id)
            user_name = user_info.first_name
        except Exception:
            await message.reply_text(f"❌ Invalid user ID {user_id}!")
            return

        # Ban the user
        ban_user(user_id, reason)

        # Send ban notification to user
        try:
            await bot.send_message(
                chat_id=user_id, 
                text=f"🚫 **You have been banned from the bot!**\n\n**Reason:** {reason}\n\n**Contact Admin:** @viizet"
            )
        except Exception:
            pass  # User might have blocked the bot

        await message.reply_text(f"✅ User {user_name} ({user_id}) has been banned successfully!\n\n**Reason:** {reason}")

    except ValueError:
        await message.reply_text("❌ Invalid user ID format!\n\n**Usage:** `/ban <user_id> <reason>`")
    except Exception as e:
        await message.reply_text(f"❌ Unexpected error: {str(e)}")


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["unban"]))
async def unban_user_cmd(bot, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage:** /unban <user_id>\n\n**Example:** `/unban 123456789`")
        return

    try:
        user_id = int(message.command[1])

        # Check if user exists in database
        from helper.database import find_one, unban_user, is_user_banned
        user_data = find_one(user_id)
        if not user_data:
            await message.reply_text(f"❌ User {user_id} not found in database!")
            return

        # Check if user is banned
        if not is_user_banned(user_id):
            await message.reply_text(f"⚠️ User {user_id} is not banned!")
            return

        # Try to get user info
        try:
            user_info = await bot.get_users(user_id)
            user_name = user_info.first_name
        except Exception:
            user_name = "Unknown User"

        # Unban the user
        unban_user(user_id)

        # Send unban notification to user
        try:
            await bot.send_message(
                chat_id=user_id, 
                text=f"✅ **You have been unbanned!**\n\nYou can now use the bot again.\n\n**Contact Admin:** @viizet"
            )
        except Exception:
            pass  # User might have blocked the bot

        await message.reply_text(f"✅ User {user_name} ({user_id}) has been unbanned successfully!")

    except ValueError:
        await message.reply_text("❌ Invalid user ID format!\n\n**Usage:** `/unban <user_id>`")
    except Exception as e:
        await message.reply_text(f"❌ Unexpected error: {str(e)}")

        await m.reply_text("❌ Invalid user ID format!\n\n**Usage:** `/warn <user_id> <message>`\n**Example:** `/warn 123456789 Please follow rules`")
    except Exception as e:
        await m.reply_text(f"❌ Unexpected error: {str(e)}")



@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
async def buypremium(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Basic", callback_data="vip1"),
        InlineKeyboardButton("⚡ Standard", callback_data="vip2")],
        [InlineKeyboardButton("💎 Pro", callback_data="vip3")],
        [InlineKeyboardButton("✖️ Cancel ✖️",callback_data = "cancel")]
        ])

    await message.reply_text("🦋 Select Plan To Upgrade...", quote=True, reply_markup=button)







@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["removepremium"]))
async def removepremium(bot, message):
    """Remove premium from a paid premium user"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /removepremium <user_id>", quote=True)
        return

    try:
        user_id = int(message.command[1])

        # Check if user exists
        user_data = find_one(user_id)
        if not user_data:
            await message.reply_text(f"❌ User {user_id} not found in database!", quote=True)
            return

        # Check if user has paid premium
        if not user_data.get("paid_premium", False):
            await message.reply_text(f"❌ User {user_id} doesn't have paid premium!", quote=True)
            return

        # Remove premium
        from helper.database import dbcol
        uploadlimit(user_id, 2147483652)  # Reset to 2GB
        usertype(user_id, "Free")
        dbcol.update_one({"_id": user_id}, {"$set": {"prexdate": None, "paid_premium": False}})

        await message.reply_text(f"✅ **Paid premium removed from user:** `{user_id}`", quote=True)

        # Notify the user
        try:
            await bot.send_message(
                user_id, 
                "⚠️ **Your premium subscription has been removed by admin.**\n\nYou are now on the Free plan. Check /myplan for details."
            )
        except:
            pass  # User might have blocked the bot

    except ValueError:
        await message.reply_text("❌ Invalid user ID format!", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}", quote=True)


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["allcommand"]))
async def allcommand(bot, message):
    commands_text = """<b>📋 ALL BOT COMMANDS</b>

<b>👥 USER COMMANDS:</b>
• /start - Start the bot and see welcome message
• /viewthumb - View current thumbnail
• /delthumb - Delete current thumbnail  
• /set_caption - Set custom caption
• /see_caption - View current caption
• /del_caption - Delete custom caption
• /metadata - Manage file metadata settings
• /ping - Check bot response time
• /myplan - View current subscription plan
• /upgrade - View premium plans
• /donate - Support the developer
• /help - Get help information

<b>🔧 ADMIN COMMANDS:</b>

<b>📊 Statistics & Management:</b>
• /users - View detailed bot statistics
• /admin - Show interactive admin panel
• /top10 - Show top 10 active users
• /allcommand - Show all bot commands (this command)

<b>👥 User Management:</b>
• /warn [user_id] [message] - Send warning to user
• /ban [user_id] [reason] - Ban user
• /unban [user_id] - Unban user
• /broadcast - Broadcast message to all users

<b>💎 Premium Management:</b>
• /addpremium - Upgrade user to premium (paid premium)
• /removepremium [user_id] - Remove paid premium from user
• /free - Manage free premium system settings
• /removefree [user_id] - Remove free premium

<b>🛠️ System Commands:</b>
• /restart - Restart the bot

<b>📱 Developer:</b> @viizet
<b>📢 Channel:</b> @Phioza</b>"""

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔧 Admin Panel", callback_data="admin_back")],
        [InlineKeyboardButton("✖️ Close ✖️", callback_data="cancel")]
    ])

    await message.reply_text(commands_text, quote=True, reply_markup=button)


# PREMIUM POWER MODE @viizet
@Client.on_callback_query(filters.regex('vip1'))
async def vip1(bot,update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    from helper.database import dbcol
    # Original limits were 2GB for Basic, 50GB for Standard, 100GB for Pro.
    # Updated to 15GB Free, 60GB Basic, 60GB Standard, 150GB Pro.
    # Here, we handle the 'Basic' plan upgrade.
    inlimit  = 64424509440  # 60GB for Basic users
    uploadlimit(int(user_id),64424509440) # Set to 60GB
    usertype(int(user_id),"🪙 Basic")
    addpre(int(user_id))
    # Mark as paid premium and remove free premium
    dbcol.update_one({"_id": int(user_id)}, {"$set": {"paid_premium": True, "free_premium": False, "upload_limit_gb": 60}}) # Explicitly set limit in GB
    await update.message.edit("Added Successfully To Premium Upload Limit 60 GB")
    await bot.send_message(user_id, f"Hey {update.from_user.mention} \n\nYou Are Upgraded To <b>🪙 Basic</b>. Check Your Plan Here /myplan")



@Client.on_callback_query(filters.regex('vip2'))
async def vip2(bot,update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    from helper.database import dbcol
    inlimit = 64424509440 # 60GB for Standard users
    uploadlimit(int(user_id), 64424509440) # Set to 60GB
    usertype(int(user_id),"⚡ Standard")
    addpre(int(user_id))
    # Mark as paid premium and remove free premium
    dbcol.update_one({"_id": int(user_id)}, {"$set": {"paid_premium": True, "free_premium": False, "upload_limit_gb": 60}}) # Explicitly set limit in GB
    await update.message.edit("Added Successfully To Premium Upload Limit 60 GB")
    await bot.send_message(user_id, f"Hey {update.from_user.mention} \n\nYou Are Upgraded To <b>⚡ Standard</b>. Check Your Plan Here /myplan")



@Client.on_callback_query(filters.regex('vip3'))
async def vip3(bot,update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    from helper.database import dbcol
    inlimit = 161061273600 # 150GB for Pro users
    uploadlimit(int(user_id), 161061273600) # Set to 150GB
    usertype(int(user_id),"💎 Pro")
    addpre(int(user_id))
    # Mark as paid premium and remove free premium
    dbcol.update_one({"_id": int(user_id)}, {"$set": {"paid_premium": True, "free_premium": False, "upload_limit_gb": 150}}) # Explicitly set limit in GB
    await update.message.edit("Added Successfully To Premium Upload Limit 150 GB")
    await bot.send_message(user_id, f"Hey {update.from_user.mention} \n\nYou Are Upgraded To <b>💎 Pro</b>. Check Your Plan Here /myplan")














# Viizet Developer 
# Telegram Channel @Phioza
# Developer @viizet
@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["admin"]))
async def admin_panel(bot, message):
    admin_text = """<b>🔧 ADMIN CONTROL PANEL</b>

<b>👥 User Management:</b>
• /users - View bot statistics
• /broadcast - Send message to all users
• /warn [user_id] [message] - Warn user
• /ban [user_id] [reason] - Ban user
• /unban [user_id] - Unban user
• /top10 - Top 10 active users

<b>💎 Premium Management:</b>
• /addpremium - Add premium to user
• /free - Manage free premium system
• /removefree - Remove free premium
• /removepremium - Remove paid premium

<b>🛠️ System Commands:</b>
• /restart - Restart the bot
• /allcommand - Show all commands
• /ping - Check bot response time

<b>👨‍💻 Admin:</b> @viizet
<b>📊 Channel:</b> @Phioza"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
         InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("💎 Premium", callback_data="admin_premium"),
         InlineKeyboardButton("🚫 Bans", callback_data="admin_bans")],
        [InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart"),
         InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
    ])

    await message.reply_text(admin_text, quote=True, reply_markup=keyboard)


# Global variable to store last refresh time and content
last_refresh = {}

@Client.on_callback_query(filters.regex("admin_stats|refresh_stats"))
async def admin_stats_callback(bot, callback_query):
    import time
    from helper.database import get_user_statistics
    from helper.progress import humanbytes

    user_id = callback_query.from_user.id
    current_time = time.time()

    # Check cooldown (2 seconds between refreshes)
    if callback_query.data == "refresh_stats":
        if user_id in last_refresh and current_time - last_refresh[user_id]['time'] < 2:
            await callback_query.answer("⏳ Please wait a moment before refreshing again!", show_alert=True)
            return

    try:
        botdata(int(botid))
        data = find_one(int(botid))
        total_rename = data["total_rename"] if data and "total_rename" in data else 0
        total_size = data["total_size"] if data and "total_size" in data else 0

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

<b>🤖 Bot ID:</b> <code>{botid}</code>"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")],
            [InlineKeyboardButton("⬅️ Back", callback_data="admin_back"),
             InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])

        # Check if content has changed
        if user_id in last_refresh and last_refresh[user_id]['content'] == text:
            if callback_query.data == "refresh_stats":
                await callback_query.answer("📊 Statistics are already up to date!", show_alert=True)
                return

        # Update last refresh data
        last_refresh[user_id] = {'time': current_time, 'content': text}

        # Edit message with new content
        await callback_query.message.edit_text(text, reply_markup=keyboard)

        if callback_query.data == "refresh_stats":
            await callback_query.answer("✅ Statistics refreshed!")

    except Exception as e:
        await callback_query.answer(f"❌ Error refreshing: {str(e)}", show_alert=True)


@Client.on_callback_query(filters.regex("admin_back"))
async def admin_back(bot, callback_query):
    admin_text = """<b>🔧 ADMIN CONTROL PANEL</b>

<b>👥 User Management:</b>
• /users - View bot statistics
• /broadcast - Send message to all users
• /warn [user_id] [message] - Warn user
• /ban [user_id] [reason] - Ban user
• /unban [user_id] - Unban user
• /top10 - Top 10 active users

<b>💎 Premium Management:</b>
• /addpremium - Add premium to user
• /free - Manage free premium system
• /removefree - Remove free premium
• /removepremium - Remove paid premium

<b>🛠️ System Commands:</b>
• /restart - Restart the bot
• /allcommand - Show all commands
• /ping - Check bot response time

<b>👨‍💻 Admin:</b> @viizet
<b>📊 Channel:</b> @Phioza"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
         InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("💎 Premium", callback_data="admin_premium"),
         InlineKeyboardButton("🚫 Bans", callback_data="admin_bans")],
        [InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart"),
         InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
    ])

    await callback_query.message.edit_text(admin_text, reply_markup=keyboard)


@Client.on_callback_query(filters.regex("admin_restart"))
async def admin_restart(bot, callback_query):
    await callback_query.message.edit_text("🔄 Restarting bot... Please wait!")
    import os, sys
    await asyncio.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_callback_query(filters.regex("admin_broadcast"))
async def admin_broadcast(bot, callback_query):
    await callback_query.message.edit_text(
        "📢 **Broadcast Instructions:**\n\n"
        "1. Reply to any message with `/broadcast` command\n"
        "2. The replied message will be sent to all users\n\n"
        "**Example:**\n"
        "Reply to a user message: `/broadcast`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("⬅️ Back", callback_data="admin_back")
        ]])
    )


@Client.on_callback_query(filters.regex("admin_users|admin_premium|admin_bans"))
async def admin_info(bot, callback_query):
    data = callback_query.data

    if data == "admin_users":
        text = """<b>👥 USER MANAGEMENT COMMANDS</b>

• `/users` - View detailed bot statistics
• `/warn [user_id] [message]` - Send warning
• `/ban [user_id] [reason]` - Ban user  
• `/unban [user_id]` - Unban user
• `/top10` - View top 10 users

**Example:**
`/warn 123456789 Please follow rules`
`/ban 123456789 Spamming bot`
`/unban 123456789`"""

    elif data == "admin_premium":
        text = """<b>💎 PREMIUM MANAGEMENT COMMANDS</b>

• `/addpremium` - Upgrade user to premium
• `/free` - Manage free premium system
• `/removefree` - Remove free premium
• `/removepremium` - Remove paid premium

**Premium Plans:**
• <b>Free User:</b> 15GB Daily Upload Limit, 2GB Max File Size
• <b>🪙 Basic:</b> 60GB Daily Upload Limit, 2GB Max File Size
• <b>⚡ Standard:</b> 60GB Daily Upload Limit, 4GB Max File Size  
• <b>💎 Pro:</b> 150GB Daily Upload Limit, 4GB Max File Size

**Example:**
Reply to user message with `/addpremium` to upgrade."""

    else:  # admin_bans
        text = """<b>🚫 BAN MANAGEMENT</b>

**Ban User:**
`/ban [user_id] [reason]`

**Unban User:**  
`/unban [user_id]`

**Check Statistics:**
Use `/users` to see banned user count

**Example:**
`/ban 123456789 Violated terms`
`/unban 123456789`"""

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⬅️ Back", callback_data="admin_back"),
        InlineKeyboardButton("✖️ Close", callback_data="cancel")
    ]])

    await callback_query.message.edit_text(text, reply_markup=keyboard)