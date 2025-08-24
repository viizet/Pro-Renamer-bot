from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb





@Client.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client,message):
    print(message.chat.id)
    thumb = find(int(message.chat.id))[0]
    if thumb :
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])
        await client.send_photo(
            message.chat.id,
            photo=f"{thumb}",
            caption="🖼️ **Your Custom Thumbnail**",
            reply_markup=button
        )
    else:
        await message.reply_text("You Don't Have Any Thumbnail ❌")
	
    
	 
@Client.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client,message):
    delthumb(int(message.chat.id))
    await message.reply_text("Thumbnail Deleted Successfully 🗑️")



@Client.on_message(filters.private & filters.photo)
async def addthumbs(client,message):
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    file_id = str(message.photo.file_id)
    addthumb(message.chat.id , file_id)
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
    ])
    await message.reply_text(
        "Thumbnail Saved Successfully ✅",
        reply_markup=button
    )






