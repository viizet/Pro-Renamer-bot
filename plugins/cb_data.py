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

app = Client("viizet", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)


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
    metadata_path = None
    if _bool_metadata:
        metadata = find(int(message.chat.id))[3]
        metadata_path = f"Metadata/{new_filename}"
        await add_metadata(path, metadata_path, metadata, ms)
    else:
        await ms.edit("🚀 Mode Changing...  ⚡")

    # Rename the downloaded file to the new filename
    splitpath = path.split("/downloads/")
    if len(splitpath) > 1:
        dow_file_name = splitpath[1]
        old_file_name = f"downloads/{dow_file_name}"
        if os.path.exists(old_file_name):
            os.rename(old_file_name, file_path)
        elif os.path.exists(path):
            os.rename(path, file_path)
    else:
        if os.path.exists(path):
            os.rename(path, file_path)
    
    # Verify file exists and has size
    if not os.path.exists(file_path):
        await ms.edit("❌ Error: File not found after processing")
        return
    
    if os.path.getsize(file_path) == 0:
        await ms.edit("❌ Error: File size is 0 bytes")
        os.remove(file_path)
        return
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
            if metadata_path and os.path.exists(metadata_path):
                os.remove(metadata_path)
            try: os.remove(ph_path)
            except: pass

        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            os.remove(file_path)
            if metadata_path and os.path.exists(metadata_path):
                os.remove(metadata_path)
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
            if metadata_path and os.path.exists(metadata_path):
                os.remove(metadata_path)

        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            if os.path.exists(file_path):
                os.remove(file_path)
            if metadata_path and os.path.exists(metadata_path):
                os.remove(metadata_path)


# -------------- VID & AUD same change (resize_thumb replace)
# (I can paste full vid + aud updated too if you want)


@Client.on_callback_query(filters.regex("upload_video"))
async def vid(bot, update):
    if not os.path.isdir("downloads"):
        os.mkdir("downloads")
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    try:
        new_name = update.message.text
        used_ = find_one(update.from_user.id)
        used = used_["used_limit"]
        date = used_["date"]
        name = new_name.split(":-")
        new_filename = name[1]
        file_path = f"downloads/{new_filename}"
        message = update.message.reply_to_message
        file = message.document or message.video or message.audio
        ms = await update.message.edit("🚀 Try To Download...  ⚡")
        used_limit(update.from_user.id, file.file_size)
        c_time = time.time()
        total_used = used + int(file.file_size)
        used_limit(update.from_user.id, total_used)
        
        try:
            path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("🚀 Downloading Media...   ⚡",  ms, c_time))
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            return
        
        # Metadata Adding Code
        _bool_metadata = find(int(message.chat.id))[2]
        metadata_path = None
        
        if _bool_metadata:
            metadata = find(int(message.chat.id))[3]
            metadata_path = f"Metadata/{new_filename}"
            await add_metadata(path, metadata_path, metadata, ms)
        else:
            await ms.edit("🚀 Mode Changing...  ⚡") 

        # Rename the downloaded file to the new filename
        splitpath = path.split("/downloads/")
        if len(splitpath) > 1:
            dow_file_name = splitpath[1]
            old_file_name = f"downloads/{dow_file_name}"
            if os.path.exists(old_file_name):
                os.rename(old_file_name, file_path)
            elif os.path.exists(path):
                os.rename(path, file_path)
        else:
            if os.path.exists(path):
                os.rename(path, file_path)
        
        # Verify file exists and has size
        if not os.path.exists(file_path):
            await ms.edit("❌ Error: File not found after processing")
            return
        
        if os.path.getsize(file_path) == 0:
            await ms.edit("❌ Error: File size is 0 bytes")
            os.remove(file_path)
            return
        user_id = int(update.message.chat.id)
        data = find(user_id)
        
        try:
            c_caption = data[1]
        except:
            c_caption = None
        
        thumb = data[0]

        duration = 0
        width = None
        height = None
        
        # Get original video metadata
        try:
            metadata_parser = extractMetadata(createParser(file_path))
            if metadata_parser and metadata_parser.has("duration"):
                duration = metadata_parser.get('duration').seconds
            if metadata_parser and metadata_parser.has("width"):
                width = metadata_parser.get('width')
            if metadata_parser and metadata_parser.has("height"):
                height = metadata_parser.get('height')
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            duration = 0
            
        if c_caption:
            vid_list = ["filename", "filesize", "duration"]
            new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
            caption = new_tex.format(filename=new_filename, filesize=humanbytes(
                file.file_size), duration=timedelta(seconds=duration))
        else:
            caption = f"**{new_filename}**"
            
        if thumb:
            ph_path = await bot.download_media(thumb)
            resize_thumb(ph_path)
            c_time = time.time()
        else:
            try:
                ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                width, height, ph_path = await fix_thumb(ph_path_)
            except Exception as e:
                ph_path = None
                print(e)

        value = 2090000000
        if value < file.file_size:
            await ms.edit("🚀 Try To Upload...  ⚡")
            try:
                filw = await app.send_video(LOG_CHANNEL, video=metadata_path if _bool_metadata else file_path, thumb=ph_path, duration=duration, width=width, height=height, caption=caption, progress=progress_for_pyrogram, progress_args=("🚀 Uploading Video...   ⚡",  ms, c_time))
                from_chat = filw.chat.id
                mg_id = filw.id
                time.sleep(2)
                await bot.copy_message(update.from_user.id, from_chat, mg_id)
                await ms.delete()
                
                os.remove(file_path)
                try:
                    os.remove(ph_path)
                except:
                    pass
                    
            except Exception as e:
                neg_used = used - int(file.file_size)
                used_limit(update.from_user.id, neg_used)
                await ms.edit(str(e))
                os.remove(file_path)
                try:
                    os.remove(ph_path)
                except:
                    return
        else:
            await ms.edit("🚀 Try To Upload...  ⚡")
            c_time = time.time()
            try:
                await bot.send_video(update.from_user.id, video=metadata_path if _bool_metadata else file_path, thumb=ph_path, duration=duration, width=width, height=height, caption=caption, progress=progress_for_pyrogram, progress_args=("🚀 Try To Uploading...  ⚡",  ms, c_time))
                await ms.delete()
                
                os.remove(file_path)
                
            except Exception as e:
                neg_used = used - int(file.file_size)
                used_limit(update.from_user.id, neg_used)
                await ms.edit(str(e))
                os.remove(file_path)
                return
                
    except Exception as e:
        await update.message.edit(f"An error occurred: {str(e)}")