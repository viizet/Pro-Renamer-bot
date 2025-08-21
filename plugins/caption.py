from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import *





@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("<b><u>Give Me A Caption To Set</u></b>\n\n<b>Example :</b> <code>/set_caption 📕 Name ➠ : {filename} \n\n🔗 Size ➠ : {filesize} \n\n⏰ Duration ➠ : {duration}</code>")
    caption = message.text.split(" ", 1)[1]
    addcaption(int(message.chat.id), caption)
    await message.reply_text("Your Caption Successfully Added ✅")



@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message): 
    caption = find(int(message.chat.id))[1]
    if not caption:
        await message.reply_text("You Don't Have Any Custom Caption ❌")
        return
    delcaption(int(message.chat.id))
    await message.reply_text("Your Caption Successfully Deleted 🗑️")
                                      
                                      
                                       
@Client.on_message(filters.private & filters.command('see_caption'))
async def see_caption(client, message): 
    caption = find(int(message.chat.id))[1]
    if caption:
       await message.reply_text(f"<b><u>Your Caption:</b></u>\n\n<code>{caption}</code>")
    else:
       await message.reply_text("You Don't Have Any Custom Caption ❌")
          





