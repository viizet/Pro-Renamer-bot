
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from script import script

@Client.on_message(filters.command(["help"]))
async def help_command(bot, message):
    text = script.HELP_TXT.format(message.from_user.mention)
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Caption", callback_data='caption_help'),
        InlineKeyboardButton("🖼️ Thumbnail", callback_data='thumb_help')],
        [InlineKeyboardButton("🔙 Back", callback_data='home'),
        InlineKeyboardButton("✖️ Close", callback_data='cancel')]
    ])
    
    await message.reply_text(text, reply_markup=button, quote=True)

@Client.on_callback_query(filters.regex('help'))
async def help_callback(bot, update):
    text = script.HELP_TXT.format(update.from_user.mention)
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Caption", callback_data='caption_help'),
        InlineKeyboardButton("🖼️ Thumbnail", callback_data='thumb_help')],
        [InlineKeyboardButton("🔙 Back", callback_data='home'),
        InlineKeyboardButton("✖️ Close", callback_data='cancel')]
    ])
    
    await update.message.edit_text(text, reply_markup=button)

@Client.on_callback_query(filters.regex('caption_help'))
async def caption_help(bot, update):
    text = script.CAPTION_TXT
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data='help')]
    ])
    
    await update.message.edit_text(text, reply_markup=button)

@Client.on_callback_query(filters.regex('thumb_help'))
async def thumb_help(bot, update):
    text = script.THUMBNAIL_TXT
    
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data='help')]
    ])
    
    await update.message.edit_text(text, reply_markup=button)

# Viizet Developer 
# Telegram Channel @Phioza
# Developer @viizet
