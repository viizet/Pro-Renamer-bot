from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram import Client , filters




@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
    text = """**📢 Upload Limits & Plans**

**✅ Free Users**
Daily Upload Limit: 15GB
Max File Size: 2GB
Price: Free

**🪙 Basic Users**
Daily Upload Limit: 60GB
Max File Size: 2GB
Price: 🌎 0.50$ per Month

**⚡ Standard Users**
Daily Upload Limit: 60GB
Max File Size: 4GB
Price: 🌎 1.50$ per Month

**💎 Pro Users**
Daily Upload Limit: 150GB
Max File Size: 4GB
Price: 🌎 3.00$ per Month

Payment Details :-
<b>➜ BITCOIN :</b> <code>Soon</code>

After Payment Send Screenshots Of Payment To Admin @viizet"""
    
    keybord = InlineKeyboardMarkup([
        [InlineKeyboardButton("🦋 Admin", url = "https://t.me/Viizet"),
        InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]
        ])
    
    await update.message.edit(text = text,reply_markup = keybord, disable_web_page_preview=True)
    
    

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot,message):
    text = """**📢 Upload Limits & Plans**

**✅ Free Users**
Daily Upload Limit: 15GB
Max File Size: 2GB
Price: Free

**🪙 Basic Users**
Daily Upload Limit: 60GB
Max File Size: 2GB
Price: 🌎 0.50$ per Month

**⚡ Standard Users**
Daily Upload Limit: 60GB
Max File Size: 4GB
Price: 🌎 1.50$ per Month

**💎 Pro Users**
Daily Upload Limit: 150GB
Max File Size: 4GB
Price: 🌎 3.00$ per Month

Payment Details :-
<b>➜ BITCOIN :</b> <code>Soon</code>

After Payment Send Screenshots Of Payment To Admin @Viizet"""
    
    keybord = InlineKeyboardMarkup([
        [InlineKeyboardButton("🦋 Admin", url = "https://t.me/viizet"),
        InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]
        ])
    
    await message.reply_text(text=text, reply_markup=keybord, quote=True, disable_web_page_preview=True)
    
	
    
    
    


# Developer @viizet
