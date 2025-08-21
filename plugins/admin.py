from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config import *
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre





@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
async def warn(c, m):
    if len(m.command) < 3:
        await m.reply_text("**Usage:** /warn <user_id> <message>")
        return
    
    try:
        user_id = int(m.command[1])
        reason = " ".join(m.command[2:])
        await c.send_message(chat_id=user_id, text=f"⚠️ **Warning from Admin:**\n\n{reason}")
        await m.reply_text(f"✅ User {user_id} notified successfully!")
    except ValueError:
        await m.reply_text("❌ Invalid user ID!")
    except Exception as e:
        await m.reply_text(f"❌ Failed to notify user: {str(e)}")
            
            

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
async def buypremium(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Basic", callback_data="vip1"),
        InlineKeyboardButton("⚡ Standard", callback_data="vip2")],
        [InlineKeyboardButton("💎 Pro", callback_data="vip3")],
        [InlineKeyboardButton("✖️ Cancel ✖️",callback_data = "cancel")]
        ])
        
    await message.reply_text("🦋 Select Plan To Upgrade...", quote=True, reply_markup=button)
    
    

@Client.on_message((filters.channel | filters.private) & filters.user(ADMIN) & filters.command(["ceasepower"]))
async def ceasepremium(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Limit 1GB", callback_data="cp1"),
        InlineKeyboardButton("All Power Cease", callback_data="cp2")],
        [InlineKeyboardButton("✖️ Cancel ✖️",callback_data = "cancel")]
        ])
	
    await message.reply_text("😁 Power Cease Mode...", quote=True, reply_markup=button)



@Client.on_message((filters.channel | filters.private) & filters.user(ADMIN) & filters.command(["resetpower"]))
async def resetpower(bot, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes",callback_data = "dft"),
        InlineKeyboardButton("❌ No",callback_data = "cancel")]
        ])
        
    await message.reply_text(text=f"Do You Really Want To Reset Daily Limit To Default Data Limit 2GB ?", quote=True, reply_markup=button)
    


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
• /ping - Check bot response time
• /myplan - View current subscription plan
• /upgrade - View premium plans
• /donate - Support the developer
• /help - Get help information
• /top10 - View top 10 users

<b>🔧 ADMIN COMMANDS:</b>
• /users - View total user count
• /allids - List all user IDs
• /broadcast - Broadcast message to all users
• /warn - Send warning to specific user
• /addpremium - Upgrade user to premium
• /ceasepower - Downgrade user capacity
• /resetpower - Reset user to default plan
• /restart - Restart the bot
• /admin - Show admin panel
• /allcommand - Show all bot commands (this command)
• /free - Manage free premium
• /removefree - Remove free premium from user
• /top10 - Show top 10 users (admin view)

<b>Made By:</b> @viizet"""
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("✖️ Close ✖️", callback_data="cancel")]
    ])
    
    await message.reply_text(commands_text, quote=True, reply_markup=button)
    

# PREMIUM POWER MODE @JISHUDEVELOPER
@Client.on_callback_query(filters.regex('vip1'))
async def vip1(bot,update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit  = 21474836500
    uploadlimit(int(user_id),21474836500)
    usertype(int(user_id),"🪙 Basic")
    addpre(int(user_id))
    await update.message.edit("Added Successfully To Premium Upload Limit 20 GB")
    await bot.send_message(user_id, f"Hey {update.from_user.mention} \n\nYou Are Upgraded To <b>🪙 Basic</b>. Check Your Plan Here /myplan")



@Client.on_callback_query(filters.regex('vip2'))
async def vip2(bot,update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 53687091200
    uploadlimit(int(user_id), 53687091200)
    usertype(int(user_id),"⚡ Standard")
    addpre(int(user_id))
    await update.message.edit("Added Successfully To Premium Upload Limit 50 GB")
    await bot.send_message(user_id, f"Hey {update.from_user.mention} \n\nYou Are Upgraded To <b>⚡ Standard</b>. Check Your Plan Here /myplan")



@Client.on_callback_query(filters.regex('vip3'))
async def vip3(bot,update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 107374182400
    uploadlimit(int(user_id), 107374182400)
    usertype(int(user_id),"💎 Pro")
    addpre(int(user_id))
    await update.message.edit("Added Successfully To Premium Upload Limit 100 GB")
    await bot.send_message(user_id, f"Hey {update.from_user.mention} \n\nYou Are Upgraded To <b>💎 Pro</b>. Check Your Plan Here /myplan")





# CEASE POWER MODE 
@Client.on_callback_query(filters.regex('cp1'))
async def cp1(bot,update):
    try:
        reply_text = update.message.reply_to_message.text
        parts = reply_text.split()
        if len(parts) >= 2:
            user_id = int(parts[1])
        else:
            await update.message.edit("❌ Invalid command format")
            return
        
        uploadlimit(user_id, 2147483652)
        usertype(user_id, "⚠️ Account Downgraded")
        addpre(user_id)
        await update.message.edit("✅ User downgraded to 2GB limit successfully")
        await bot.send_message(user_id, f"⚠️ Your account has been downgraded to <b>2GB limit</b>.\n\nCheck your plan: /myplan\n\n<b>Contact Admin:</b> @viizet")
    except Exception as e:
        await update.message.edit(f"❌ Error: {str(e)}")

@Client.on_callback_query(filters.regex('cp2'))
async def cp2(bot,update):
    try:
        reply_text = update.message.reply_to_message.text
        parts = reply_text.split()
        if len(parts) >= 2:
            user_id = int(parts[1])
        else:
            await update.message.edit("❌ Invalid command format")
            return
        
        uploadlimit(user_id, 0)
        usertype(user_id, "⚠️ Account Downgraded")
        addpre(user_id)
        await update.message.edit("✅ User downgraded to 0GB limit successfully")
        await bot.send_message(user_id, f"⚠️ Your account has been downgraded to <b>0GB limit</b>.\n\nCheck your plan: /myplan\n\n<b>Contact Admin:</b> @viizet")
    except Exception as e:
        await update.message.edit(f"❌ Error: {str(e)}")

# RESET POWER MODE
@Client.on_callback_query(filters.regex('dft'))
async def dft(bot,update):
    try:
        reply_text = update.message.reply_to_message.text
        parts = reply_text.split()
        if len(parts) >= 2:
            user_id = int(parts[1])
        else:
            await update.message.edit("❌ Invalid command format")
            return
        
        uploadlimit(user_id, 2147483652)
        usertype(user_id, "🆓 Free")
        addpre(user_id)
        await update.message.edit("✅ User reset to default 2GB plan successfully")
        await bot.send_message(user_id, f"✅ Your account has been reset to default plan.\n\nCheck your plan: /myplan\n\n<b>Contact Admin:</b> @viizet")
    except Exception as e:
        await update.message.edit(f"❌ Error: {str(e)}")






@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["top10"]))
async def top10_admin(bot, message):
    try:
        # Get top 10 users by usage (you can modify this query based on your needs)
        pipeline = [
            {"$match": {"_id": {"$ne": "free_premium_config"}}},
            {"$sort": {"used_limit": -1}},
            {"$limit": 10}
        ]
        top_users = list(dbcol.aggregate(pipeline))
        
        if not top_users:
            await message.reply_text("❌ No users found!")
            return
            
        text = "🏆 **TOP 10 USERS**\n\n"
        for i, user in enumerate(top_users, 1):
            user_id = user.get("_id", "Unknown")
            used_limit = user.get("used_limit", 0)
            user_type = user.get("usertype", "Free")
            
            # Try to get user info
            try:
                user_info = await bot.get_users(user_id)
                name = user_info.first_name
            except:
                name = "Unknown"
            
            text += f"**{i}.** {name} (`{user_id}`)\n"
            text += f"   **Type:** {user_type}\n"
            text += f"   **Used:** {humanbytes(used_limit)}\n\n"
        
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])
        
        await message.reply_text(text, reply_markup=button, quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Viizet Developer 
# Telegram Channel @Phioza
# Developer @viizet
