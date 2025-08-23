from helper.progress import progress_for_pyrogram, humanbytes
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import *
import os, random, time, asyncio, humanize
from PIL import Image
from datetime import timedelta
from helper.ffmpeg import take_screen_shot, fix_thumb, add_metadata
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
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img.save(ph_path, "JPEG")
    except Exception as e:
        print("Thumb resize error:", e)


# ---------------- Cancel
@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        if update.message:
            await update.message.delete()
        if update.message and update.message.reply_to_message:
            await update.message.reply_to_message.delete()
        await update.answer()  # Instead of continue_propagation
    except Exception as e:
        print(f"Cancel error: {e}")


# ---------------- Rename
@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    chat_id = update.message.chat.id
    if update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id
    else:
        reply_id = None

    await update.message.delete()
    await update.message.reply_text(
        "__Please Enter The New Filename...__\n\n**Note :** Extension Not Required",
        reply_to_message_id=reply_id,
        reply_markup=ForceReply(True)
    )

    # Use message date or current timestamp
    date = int(update.message.date.timestamp()) if update.message.date else int(time.time())
    dateupdate(chat_id, date)


# ---------------- Document Upload
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")
    if not os.path.isdir("downloads"):
        os.mkdir("downloads")

    new_name = update.data  # CallbackQuery data
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    try:
        new_filename = new_name.split(":-")[1]
    except IndexError:
        await update.answer("❌ Invalid filename format", show_alert=True)
        return

    file_path = os.path.join("downloads", new_filename)
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading...  ⚡")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)

    # Download media
    try:
        path = await bot.download_media(
            message=file,
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=("🚀 Downloading...  ⚡", ms, c_time)
        )
    except Exception as e:
        used_limit(update.from_user.id, used)  # revert
        await ms.edit(f"❌ Download failed: {e}")
        return

    # Verify download
    if not path or not os.path.exists(path) or os.path.getsize(path) == 0:
        await ms.edit("❌ Downloaded file is invalid")
        if os.path.exists(path):
            os.remove(path)
        return

    # Metadata
    _bool_metadata = find(int(message.chat.id))[2]
    metadata_path = None
    if _bool_metadata:
        metadata = find(int(message.chat.id))[3]
        metadata_path = os.path.join("Metadata", new_filename)
        try:
            await add_metadata(path, metadata_path, metadata, ms)
        except Exception as e:
            await ms.edit(f"❌ Metadata failed: {e}")
            if os.path.exists(path):
                os.remove(path)
            return

    final_file_path = metadata_path if _bool_metadata else path

    # Caption
    user_id = int(update.message.chat.id)
    data = find(user_id)
    c_caption = data[1] if data and len(data) > 1 else None
    thumb = data[0] if data else None

    if c_caption:
        doc_list = ["filename", "filesize"]
        new_tex = escape_invalid_curly_brackets(c_caption, doc_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(file.file_size))
    else:
        caption = f"**{new_filename}**"

    # Thumbnail
    ph_path = None
    if thumb:
        ph_path = await bot.download_media(thumb)
        resize_thumb(ph_path)

    # Upload
    try:
        await bot.send_document(
            update.from_user.id,
            document=final_file_path,
            thumb=ph_path,
            caption=caption,
            progress=progress_for_pyrogram,
            progress_args=("🚀 Uploading...  ⚡", ms, c_time)
        )
        await ms.delete()
    except Exception as e:
        used_limit(update.from_user.id, used)  # revert usage
        await ms.edit(f"❌ Upload failed: {e}")
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)
        if metadata_path and os.path.exists(metadata_path):
            os.remove(metadata_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)


# ---------------- Video Upload
@Client.on_callback_query(filters.regex("upload_video"))
async def vid(bot, update):
    if not os.path.isdir("downloads"):
        os.mkdir("downloads")
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_name = update.data  # CallbackQuery data
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]

    try:
        new_filename = new_name.split(":-")[1]
    except IndexError:
        await update.answer("❌ Invalid filename format", show_alert=True)
        return

    file_path = os.path.join("downloads", new_filename)
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading... ⚡")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)

    # Download media
    try:
        path = await bot.download_media(
            message=file,
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=("🚀 Downloading... ⚡", ms, c_time)
        )
    except Exception as e:
        used_limit(update.from_user.id, used)  # revert
        await ms.edit(f"❌ Download failed: {e}")
        return

    # Verify download
    if not path or not os.path.exists(path) or os.path.getsize(path) == 0:
        await ms.edit("❌ Downloaded file is invalid")
        if os.path.exists(path):
            os.remove(path)
        return

    # Metadata
    _bool_metadata = find(int(message.chat.id))[2]
    metadata_path = None
    if _bool_metadata:
        metadata = find(int(message.chat.id))[3]
        metadata_path = os.path.join("Metadata", new_filename)
        try:
            await add_metadata(path, metadata_path, metadata, ms)
        except Exception as e:
            await ms.edit(f"❌ Metadata failed: {e}")
            if os.path.exists(path):
                os.remove(path)
            return

    final_file_path = metadata_path if _bool_metadata else path

    # Caption
    user_id = int(update.message.chat.id)
    data = find(user_id)
    c_caption = data[1] if data and len(data) > 1 else None
    thumb = data[0] if data else None

    # Extract video metadata
    duration, width, height = 0, None, None
    try:
        metadata_parser = extractMetadata(createParser(path))
        if metadata_parser and metadata_parser.has("duration"):
            duration = metadata_parser.get("duration").seconds
        if metadata_parser and metadata_parser.has("width"):
            width = metadata_parser.get("width")
        if metadata_parser and metadata_parser.has("height"):
            height = metadata_parser.get("height")
    except Exception as e:
        print(f"Metadata extraction error: {e}")

    if c_caption:
        vid_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(file.file_size),
                                 duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"

    # Thumbnail
    ph_path = None
    if thumb:
        ph_path = await bot.download_media(thumb)
        resize_thumb(ph_path)
    else:
        try:
            sec = random.randint(0, max(duration - 1, 0))
            ph_path_ = await take_screen_shot(path, os.path.dirname(os.path.abspath(path)), sec)
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(f"Thumbnail error: {e}")

    # Upload
    try:
        await bot.send_video(
            update.from_user.id,
            video=final_file_path,
            thumb=ph_path,
            duration=duration,
            width=width,
            height=height,
            caption=caption,
            progress=progress_for_pyrogram,
            progress_args=("🚀 Uploading... ⚡", ms, c_time)
        )
        await ms.delete()
    except Exception as e:
        used_limit(update.from_user.id, used)  # revert usage
        await ms.edit(f"❌ Upload failed: {e}")
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)
        if metadata_path and os.path.exists(metadata_path):
            os.remove(metadata_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)
