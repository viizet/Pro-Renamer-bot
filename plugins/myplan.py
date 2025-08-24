import time
from datetime import datetime, date as date_
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import find_one, used_limit, daily as daily_, uploadlimit, usertype
from helper.progress import humanbytes
from helper.date import check_expi


@Client.on_message(filters.private & filters.command(["myplan"]))
async def start(client, message):
    # Hel xogta user-ka database, haddii aysan jirin samee default
    used_ = find_one(message.from_user.id) or {}
    
    daily = used_.get("daily", 0)
    today = date_.today()
    today_epcho = int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))
    
    expi = daily - today_epcho
    if expi != 0:
        daily_(message.from_user.id, today_epcho)
        used_limit(message.from_user.id, 0)
    
    # Refresh xogta user ka dib update
    _newus = find_one(message.from_user.id) or {}
    
    used = max(0, int(_newus.get("used_limit", 0)))
    limit = int(_newus.get("uploadlimit", 0))
    remain = max(0, limit - used)
    
    # Haddii used ka hooseeyo 0 → reset
    if int(_newus.get("used_limit", 0)) < 0:
        used_limit(message.from_user.id, 0)
    
    user = _newus.get("usertype", "Free")
    ends = _newus.get("prexdate", None)
    
    # Haddii plan-ka uu dhacay → ku celi free 15GB
    if ends:
        pre_check = check_expi(ends)
        if pre_check is False:
            uploadlimit(message.from_user.id, 16106127360)  # 15GB
            usertype(message.from_user.id, "Free")
    
    # Check premium
    is_free_premium = _newus.get("free_premium", False)
    is_paid_premium = _newus.get("paid_premium", False)
    premium_badge = " 🎁" if (is_free_premium and not is_paid_premium) else ""
    
    # Plan info
    if ends is None:
        text = f"""<b>User ID :</b> <code>{message.from_user.id}</code> 
<b>Name :</b> {message.from_user.mention} 

<b>🏷 Plan :</b> {user}{premium_badge} 

✓ Max File Size: 2GB 
✓ Daily Upload : {humanbytes(limit)} 
✓ Today Used : {humanbytes(used)} 
✓ Remain : {humanbytes(remain)} 
✓ Timeout : 2 Minutes 
✓ Parallel process : Unlimited 
✓ Time Gap : Yes 

<b>Validity :</b> Lifetime"""
    else:
        normal_date = datetime.fromtimestamp(ends).strftime('%Y-%m-%d')
        plan_info = f"{user}{premium_badge}"
        if is_free_premium:
            plan_info += " (Free Premium)"
        
        # Xadka max size ku saley usertype
        if "Basic" in user:
            max_file_size = "2GB"
        elif "Standard" in user or "Pro" in user:
            max_file_size = "4GB"
        else:
            max_file_size = "2GB"
        
        text = f"""<b>User ID :</b> <code>{message.from_user.id}</code> 
<b>Name :</b> {message.from_user.mention} 

<b>🏷 Plan :</b> {plan_info} 

✓ High Priority 
✓ Max File Size: {max_file_size} 
✓ Daily Upload : {humanbytes(limit)} 
✓ Today Used : {humanbytes(used)} 
✓ Remain : {humanbytes(remain)} 
✓ Timeout : 0 Second 
✓ Parallel process : Unlimited 
✓ Time Gap : Yes 

<b>Your Plan Ends On :</b> {normal_date}"""
    
    # Reply oo ku dar button-yada
    if user == "Free":
        await message.reply(
            text,
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("💳 Upgrade", callback_data="upgrade"),
                    InlineKeyboardButton("✖️ Cancel", callback_data="cancel")
                ]
            ])
        )
    else:
        await message.reply(
            text,
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✖️ Cancel ✖️", callback_data="cancel")]
            ])
        )


# viizet Developer 
# Don't Remove Credit 🥺
