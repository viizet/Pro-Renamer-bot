from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from script import script

@Client.on_message(filters.command(["help"]))
async def help_command(bot, message):
    text = script.HELP_TXT.format(message.from_user.mention)
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Caption", callback_data='caption'),
        InlineKeyboardButton("🖼️ Thumbnail", callback_data='thumbnail')],
        [InlineKeyboardButton("🔙 Back", callback_data='home'),
        InlineKeyboardButton("✖️ Close", callback_data='cancel')]
    ])
    
    await message.reply_text(text, reply_markup=button, quote=True)



# Viizet Developer 
# Telegram Channel @Phioza
# Developer @viizet
