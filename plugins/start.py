from datetime import date as date_
import os, re, datetime, random, asyncio, time, humanize
from script import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram import Client, filters, enums
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from helper.progress import humanbytes
from helper.database import botdata, find_one, total_user
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import check_expi
from config import *

token = BOT_TOKEN
botid = token.split(':')[0]

# Function to check if a user is banned
def is_user_banned(user_id):
    from helper.database import find_one
    user_data = find_one(user_id)
    if user_data:
        return user_data.get("banned", False)
    return False

# Ban check middleware - Add this before other handlers
@Client.on_message(filters.private & ~filters.user(ADMIN))
async def ban_check(client, message):
    user_id = message.from_user.id
    
    if is_user_banned(user_id):
        await message.reply_text(
            "🚫 **You are banned from using this bot!**\n\n"
            "Your access has been restricted by the administrator.\n\n"
            "**Contact Admin:** @viizet",
            quote=True
        )
        return
    
    # If not banned, continue to other handlers
    message.continue_propagation()

def get_banned_users():
    # Replace this with your actual database query to get banned user IDs
    # For demonstration purposes, returning an empty list
    return []


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message):
    # Check if user is banned
    if is_user_banned(message.from_user.id):
        await message.reply_text("🚫 **You are banned from using this bot!**\n\nContact admin: @viizet")
        return

    user_id = message.chat.id
    old = insert(int(user_id))

    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None



    text = f"""Hello {message.from_user.mention} 👋

🤖 **File Rename Bot**

✨ **Features:**
• Rename files & change thumbnails
• Convert video ↔ file
• Custom captions & metadata

💎 **Premium:** 4GB uploads available

<b>Made by @viizet</b>"""

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", url="https://t.me/Phioza"),
        InlineKeyboardButton("💬 Support", url="https://t.me/Phioza")],
        [InlineKeyboardButton("🛠️ Help", callback_data='help'),
        InlineKeyboardButton("❤️‍🩹 About", callback_data='about')],
        [InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/viizet")]
        ])

    await message.reply_photo(
        photo=START_PIC,
        caption=text,
        reply_markup=button,
        quote=True
        )
    return



@Client.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    user_id = message.chat.id
    
    # Check if user is banned (skip for admin)
    if message.from_user.id != ADMIN and is_user_banned(message.from_user.id):
        await message.reply_text(
            "🚫 **You are banned from using this bot!**\n\n"
            "Your access has been restricted by the administrator.\n\n"
            "**Contact Admin:** @viizet",
            quote=True
        )
        return
    
    old = insert(int(user_id))
    user_id = message.from_user.id

    botdata(int(botid))
    bot_data = find_one(int(botid))
    prrename = bot_data['total_rename']
    prsize = bot_data['total_size']
    user_deta = find_one(user_id)
    used_date = user_deta["date"]
    buy_date = user_deta["prexdate"]
    daily = user_deta["daily"]
    user_type = user_deta["usertype"]


        # Forward a single message
    media = await client.get_messages(message.chat.id, message.id)
    file = media.document or media.video or media.audio
    dcid = FileId.decode(file.file_id).dc_id
    filename = file.file_name
    file_id = file.file_id
    value = 2147483648
    used_ = find_one(message.from_user.id)
    used = used_["used_limit"]
    limit = used_["uploadlimit"]
    expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if expi != 0:
        today = date_.today()
        pattern = '%Y-%m-%d'
        epcho = int(time.mktime(time.strptime(str(today), pattern)))
        daily_(message.from_user.id, epcho)
        used_limit(message.from_user.id, 0)
    remain = limit - used
    if remain < int(file.file_size):
        await message.reply_text(f"100% Of Daily {humanbytes(limit)} Data Quota Exhausted.\n\n<b>File Size Detected :</b> {humanbytes(file.file_size)}\n<b>Used Daily Limit :</b> {humanbytes(used)}\n\nYou Have Only <b>{humanbytes(remain)}</b> Left On Your Account.\n\nIf U Want To Rename Large File Upgrade Your Plan", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
        return
    if value < file.file_size:
        # Check if user has premium or free premium
        is_free_premium = user_deta.get("free_premium", False)
        has_premium = buy_date and check_expi(buy_date) if buy_date else False

        if STRING_SESSION and (has_premium or is_free_premium):
            # Check plan-specific file size limits for premium users
            user_plan = user_deta.get("usertype", "Free")
            max_file_size = 2147483648  # 2GB default
            
            # Basic plan: 2GB max file size
            if "Basic" in user_plan:
                max_file_size = 2147483648  # 2GB
            # Standard and Pro plans: 4GB max file size  
            elif "Standard" in user_plan or "Pro" in user_plan:
                max_file_size = 4294967296  # 4GB
                
            if file.file_size > max_file_size:
                size_limit = "2GB" if "Basic" in user_plan else "4GB"
                await message.reply_text(f"❌ **File Too Large!**\n\nCan't upload files bigger than **{size_limit}**\n\n**File Size:** {humanize.naturalsize(file.file_size)}\n**Your Plan:** {user_plan}\n**Max File Size:** {size_limit}\n\nUpgrade to Standard or Pro for 4GB file support.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
                return
                
            # Get file extension and mime type
            file_extension = filename.split('.')[-1] if '.' in filename else 'Unknown'
            mime_type = getattr(file, 'mime_type', 'None')
            
            await message.reply_text(f"""🗂️ **Media Info :**\n\n◈ **File Name :** {filename}\n◈ **File Size :** {humanize.naturalsize(file.file_size)}\n◈ **File Extension :** {file_extension}\n◈ **Mime Type :** {mime_type}\n◈ **DC ID :** {dcid}\n\n**Please Enter The New Filename **""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Rename", callback_data="rename"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
        else:
            await message.reply_text("❌ **File Too Large!**\n\nCan't upload files bigger than **2GB**\n\n**File Size:** {}\n**Your Plan:** Free\n**Max File Size:** 2GB\n\nUpgrade Your Plan To Rename Files Larger Than 2GB.".format(humanize.naturalsize(file.file_size)), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
            return
    else:
        # For files under 2GB, check if Basic users are trying to upload files over 2GB
        is_free_premium = user_deta.get("free_premium", False)
        has_premium = buy_date and check_expi(buy_date) if buy_date else False
        user_plan = user_deta.get("usertype", "Free")
        
        # Basic plan users have 2GB file size limit even for smaller overall files
        if (has_premium or is_free_premium) and "Basic" in user_plan:
            basic_limit = 2147483648  # 2GB
            if file.file_size > basic_limit:
                await message.reply_text(f"❌ **File Too Large!**\n\nCan't upload files bigger than **2GB**\n\n**File Size:** {humanize.naturalsize(file.file_size)}\n**Your Plan:** {user_plan}\n**Max File Size:** 2GB\n\nUpgrade to Standard or Pro for 4GB file support.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
                return

        # Check if premium expired and reset to free if needed
        if buy_date:
            pre_check = check_expi(buy_date)
            if pre_check == False:
                uploadlimit(message.from_user.id, 2147483648)
                usertype(message.from_user.id, "Free")

        filesize = humanize.naturalsize(file.file_size)
        fileid = file.file_id
        total_rename(int(botid), prrename)
        total_size(int(botid), prsize, file.file_size)
        # Get file extension and mime type
        file_extension = filename.split('.')[-1] if '.' in filename else 'Unknown'
        mime_type = getattr(file, 'mime_type', 'None')
        
        await message.reply_text(f"""🗂️ **Media Info :**\n\n◈ **File Name :** {filename}\n◈ **File Size :** {filesize}\n◈ **File Extension :** {file_extension}\n◈ **Mime Type :** {mime_type}\n◈ **DC ID :** {dcid}\n\n**Please Enter The New Filename **""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📝 Rename", callback_data="rename"),
              InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))