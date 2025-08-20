from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import *
import os, random, time, asyncio, humanize
from PIL import Image
from datetime import timedelta
from helper.ffmpeg import take_screen_shot, fix_thumb, add_metadata
from helper.progress import humanbytes
from helper.set import escape_invalid_curly_brackets
from config import *

app = Client("JishuBotz", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)


# --------- Helper function for resizing thumbs (aspect ratio safe)
def resize_thumb(ph_path):
    try:
        img = Image.open(ph_path).convert("RGB")
        w, h = img.size
        new_width = 320
        new_height = int((h / w) * new_width)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(ph_path, "JPEG")
    except Exception as e:
        print("Thumb resize error:", e)


@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
        await update.message.reply_to_message.delete()
        await update.message.continue_propagation()
    except:
        await update.message.delete()
        await update.message.continue_propagation()
        return


@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    date_fa = str(update.message.date)
    pattern = '%Y-%m-%d %H:%M:%S'
    date = int(time.mktime(time.strptime(date_fa, pattern)))
    chat_id = update.message.chat.id
    id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(
        "__Please Enter The New Filename...__\n\n**Note :** Extension Not Required",
        reply_to_message_id=id,
        reply_markup=ForceReply(True)
    )
    dateupdate(chat_id, date)


@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("🚀 Try To Download...  ⚡")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)

    try:
        path = await bot.download_media(message=file,
                                        progress=progress_for_pyrogram,
                                        progress_args=("🚀 Try To Downloading...  ⚡", ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(str(e))
        return

    # Metadata
    _bool_metadata = find(int(message.chat.id))[2]
    if _bool_metadata:
        metadata = find(int(message.chat.id))[3]
        metadata_path = f"Metadata/{new_filename}"
        await add_metadata(path, metadata_path, metadata, ms)
    else:
        await ms.edit("🚀 Mode Changing...  ⚡")

    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)

    try:
        c_caption = data[1]
    except:
        c_caption = None

    thumb = data[0]
    if c_caption:
        doc_list = ["filename", "filesize"]
        new_tex = escape_invalid_curly_brackets(c_caption, doc_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(file.file_size))
    else:
        caption = f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        resize_thumb(ph_path)
        c_time = time.time()
    else:
        ph_path = None

    # Uploading
    value = 2090000000
    if value < file.file_size:
        await ms.edit("🚀 Try To Upload...  ⚡")
        try:
            filw = await app.send_document(LOG_CHANNEL,
                                           document=metadata_path if _bool_metadata else file_path,
                                           thumb=ph_path,
                                           caption=caption,
                                           progress=progress_for_pyrogram,
                                           progress_args=("🚀 Try To Uploading...  ⚡", ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()

            os.remove(file_path)
            try: os.remove(ph_path)
            except: pass

        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            os.remove(file_path)
            try: os.remove(ph_path)
            except: return
    else:
        await ms.edit("🚀 Try To Upload...  ⚡")
        try:
            await bot.send_document(update.from_user.id,
                                    document=metadata_path if _bool_metadata else file_path,
                                    thumb=ph_path,
                                    caption=caption,
                                    progress=progress_for_pyrogram,
                                    progress_args=("🚀 Try To Uploading...  ⚡", ms, c_time))
            await ms.delete()
            os.remove(file_path)

        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            os.remove(file_path)


# -------------- VID & AUD same change (resize_thumb replace)
# (I can paste full vid + aud updated too if you want)

