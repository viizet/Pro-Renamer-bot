from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram import Client , filters




@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
    text = """**Free Plan User**
Daily  Upload limit 2GB
Price 0

**🪙 Basic**
Daily  Upload  limit 20GB
Price 🌎 0.50$  per Month

**⚡ Standard**
Daily Upload limit 50GB
Price 🌎 1.50$  per Month

**💎 Pro**
Daily Upload limit 100GB
Price 🌎 3.00$  per Month

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
    text = """**Free Plan User**
Daily  Upload limit 2GB
Price 0

**🪙 Basic**
Daily  Upload  limit 20GB
Price  🌎 0.50$  per Month

**⚡ Standard**
Daily Upload limit 50GB
Price  🌎 1.50$  per Month

**💎 Pro**
Daily Upload limit 100GB
Price  🌎 3.00$  per Month

Payment Details :-
<b>➜ BITCOIN :</b> <code>Soon</code>

After Payment Send Screenshots Of Payment To Admin @Viizet"""
    
    keybord = InlineKeyboardMarkup([
        [InlineKeyboardButton("🦋 Admin", url = "https://t.me/viizet"),
        InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]
        ])
    
    await message.reply_text(text=text, reply_markup=keybord, quote=True, disable_web_page_preview=True)
    
	
    
    
    


# Developer @viizet
