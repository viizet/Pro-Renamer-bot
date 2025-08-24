import time
from datetime import datetime, date as date_
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from helper.database import find_one, used_limit
from helper.database import daily as daily_
from helper.progress import humanbytes
from helper.date import check_expi
from helper.database import uploadlimit, usertype




@Client.on_message(filters.private & filters.command(["myplan"]))
async def start(client, message):
    used_ = find_one(message.from_user.id)
    daily = used_["daily"]
    expi = daily - \
        int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if expi != 0:
        today = date_.today()
        pattern = '%Y-%m-%d'
        epcho = int(time.mktime(time.strptime(str(today), pattern)))
        daily_(message.from_user.id, epcho)
        used_limit(message.from_user.id, 0)
    _newus = find_one(message.from_user.id)
    used_raw = _newus.get("used_limit", 0)
    # Handle None, negative values, or any other invalid data
    if used_raw is None or used_raw < 0:
        used = 0
        used_limit(message.from_user.id, 0)  # Reset in database
    else:
        used = int(used_raw)
    
    limit = _newus["uploadlimit"]
    remain = int(limit) - int(used)
    user = _newus["usertype"]
    ends = _newus["prexdate"]
    if ends:
        # Convert string timestamp to integer if needed
        if isinstance(ends, str):
            try:
                ends = int(ends)
            except ValueError:
                # If it's a date string, convert to timestamp
                from datetime import datetime
                try:
                    ends = int(datetime.strptime(ends, '%Y-%m-%d').timestamp())
                except:
                    ends = None
        
        if ends:
            pre_check = check_expi(ends)
            if pre_check == False:
                uploadlimit(message.from_user.id, 16106127360)  # 15GB for free users
                usertype(message.from_user.id, "Free")
                # Remove expired premium status
                from helper.database import dbcol
                dbcol.update_one({"_id": message.from_user.id}, {"$set": {"free_premium": False, "paid_premium": False}})
    
    # Check if user has free premium (but not paid premium)
    is_free_premium = _newus.get("free_premium", False)
    is_paid_premium = _newus.get("paid_premium", False)
    premium_badge = " 🎁" if (is_free_premium and not is_paid_premium) else ""
    
    if ends == None:
        # Format usage display - show "0 B" when usage is 0
        used_display = "0 B" if used == 0 else humanbytes(used)
        
        text = f"<b>User ID :</b> <code>{message.from_user.id}</code> \n<b>Name :</b> {message.from_user.mention} \n\n<b>🏷 Plan :</b> {user}{premium_badge} \n\n✓ Max File Size: 2GB \n✓ Daily Upload : {humanbytes(limit)} \n✓ Today Used : {used_display} \n✓ Remain : {humanbytes(remain)} \n✓ Timeout : 2 Minutes \n✓ Parallel process : Unlimited \n✓ Time Gap : Yes \n\n<b>Validity :</b> Lifetime"
    else:
        # Handle timestamp conversion properly
        if isinstance(ends, str):
            try:
                # If it's already a date string
                normal_date = ends
            except:
                normal_date = "Unknown"
        else:
            try:
                # Convert timestamp to date string
                normal_date = datetime.fromtimestamp(ends).strftime('%Y-%m-%d')
            except:
                normal_date = "Unknown"
            
        plan_info = f"{user}{premium_badge}"
        if is_free_premium and not is_paid_premium:
            plan_info += " (Free Premium)"
        
        # Determine max file size based on plan
        if "Basic" in user:
            max_file_size = "2GB"
        elif "Standard" in user or "Pro" in user:
            max_file_size = "4GB"
        else:
            max_file_size = "2GB"
            
        # Format usage display - show "0 B" when usage is 0
    used_display = "0 B" if used == 0 else humanbytes(used)
    
    text = f"<b>User ID :</b> <code>{message.from_user.id}</code> \n<b>Name :</b> {message.from_user.mention} \n\n<b>🏷 Plan :</b> {plan_info} \n\n✓ High Priority \n✓ Max File Size: {max_file_size} \n✓ Daily Upload : {humanbytes(limit)} \n✓ Today Used : {used_display} \n✓ Remain : {humanbytes(remain)} \n✓ Timeout : 0 Second \n✓ Parallel process : Unlimited \n✓ Time Gap : Yes \n\n<b>Your Plan Ends On :</b> {normal_date}"

    if user == "Free":
        await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Upgrade", callback_data="upgrade"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
    else:
        await message.reply(text, quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Cancel ✖️", callback_data="cancel")]]))





# viizet Developer 
# Don't Remove Credit 🥺
