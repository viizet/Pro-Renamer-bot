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
            await message.reply_text(f"""__What Do You Want Me To Do With This File ?__\n\n**File Name :** `{filename}`\n**File Size :** {humanize.naturalsize(file.file_size)}\n**DC ID :** {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Rename", callback_data="rename"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
        else:
            await message.reply_text("You Can't Upload More Than 2GB File.\n\nYour Plan Doesn't Allow To Upload Files That Are Larger Than 2GB.\n\nUpgrade Your Plan To Rename Files Larger Than 2GB.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")]]))
            return
    else:
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
        await message.reply_text(f"""__What Do You Want Me To Do With This File ?__\n\n**File Name :** `{filename}`\n**File Size :** {filesize}\n**DC ID :** {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📝 Rename", callback_data="rename"),
              InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))