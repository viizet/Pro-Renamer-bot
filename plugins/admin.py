from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config import *
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre





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


<b>🔧 ADMIN COMMANDS:</b>
• /users - View total user count

• /broadcast - Broadcast message to all users
• /warn - Send warning to specific user
• /addpremium - Upgrade user to premium
• /ban - Ban user with reason
• /unban - Unban user
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














# Viizet Developer 
# Telegram Channel @Phioza
# Developer @viizet
