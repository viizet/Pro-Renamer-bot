from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram import Client , filters




@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
    text = """**🚀 PREMIUM PLANS & FEATURES**

**✅ Free Plan**
• Daily Upload Limit: 10GB
• Max File Size: 2GB
• Price: Free Forever
• Basic Features

**🪙 Basic Plan - $0.50/month**
• Daily Upload Limit: 60GB
• Max File Size: 2GB
• Priority Processing
• No Timeout Delays

**⚡ Standard Plan - $1.50/month**
• Daily Upload Limit: 60GB
• Max File Size: 4GB
• High Priority Processing
• Advanced Features
• Unlimited Parallel Processing

**💎 Pro Plan - $3.00/month**
• Daily Upload Limit: Unlimited
• Max File Size: 4GB
• Highest Priority Processing
• All Premium Features
• 24/7 Priority Support

**💳 Payment Methods:**
• Bitcoin: Coming Soon
• PayPal: Available
• Crypto: Multiple Options

**📞 After Payment:**
Send payment screenshot to admin @viizet for instant activation!

**✨ Premium Benefits:**
✅ Faster Processing • ✅ Large File Support • ✅ No Delays • ✅ Priority Support"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Contact Admin", url = "https://t.me/viizet"),
        InlineKeyboardButton("📊 My Plan", callback_data="myplan")],
        [InlineKeyboardButton("🔄 Refresh Plans", callback_data="upgrade"),
        InlineKeyboardButton("❓ FAQ", callback_data="premium_faq")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])

    await update.message.edit(text = text,reply_markup = keyboard, disable_web_page_preview=True)



@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot,message):
    text = """**🚀 PREMIUM PLANS & FEATURES**

**✅ Free Plan**
• Daily Upload Limit: 10GB
• Max File Size: 2GB
• Price: Free Forever
• Basic Features

**🪙 Basic Plan - $0.50/month**
• Daily Upload Limit: 60GB
• Max File Size: 2GB
• Priority Processing
• No Timeout Delays

**⚡ Standard Plan - $1.50/month**
• Daily Upload Limit: 60GB
• Max File Size: 4GB
• High Priority Processing
• Advanced Features
• Unlimited Parallel Processing

**💎 Pro Plan - $3.00/month**
• Daily Upload Limit: Unlimited
• Max File Size: 4GB
• Highest Priority Processing
• All Premium Features
• 24/7 Priority Support

**💳 Payment Methods:**
• Bitcoin: Coming Soon
• PayPal: Available
• Crypto: Multiple Options

**📞 After Payment:**
Send payment screenshot to admin @viizet for instant activation!

**✨ Premium Benefits:**
✅ Faster Processing • ✅ Large File Support • ✅ No Delays • ✅ Priority Support"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Contact Admin", url = "https://t.me/viizet"),
        InlineKeyboardButton("📊 My Plan", callback_data="myplan")],
        [InlineKeyboardButton("🔄 Refresh Plans", callback_data="upgrade"),
        InlineKeyboardButton("❓ FAQ", callback_data="premium_faq")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])

    await message.reply_text(text=text, reply_markup=keyboard, quote=True, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex('premium_faq'))
async def premium_faq(bot, update):
    faq_text = """**❓ PREMIUM FAQ**

**Q: How do I upgrade to premium?**
A: Contact admin @viizet with your preferred plan and make payment.

**Q: How long does activation take?**
A: Instant activation after payment verification (usually within 5 minutes).

**Q: Can I change plans later?**
A: Yes! Contact admin to upgrade or downgrade anytime.

**Q: What payment methods do you accept?**
A: PayPal, Bitcoin, and various cryptocurrencies.

**Q: Is there a refund policy?**
A: 7-day money-back guarantee for all premium plans.

**Q: Do limits reset daily?**
A: Yes, upload limits reset every 24 hours at midnight UTC.

**Q: Can I share my premium account?**
A: No, premium is tied to your Telegram account only.

**Need more help?** Contact @viizet"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back to Plans", callback_data="upgrade")],
        [InlineKeyboardButton("💳 Contact Admin", url="https://t.me/viizet")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
    ])

    await update.message.edit(text=faq_text, reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex('myplan'))
async def myplan_callback(bot, update):
    # Handle myplan directly in callback without redirecting
    from helper.database import find_one, used_limit
    from helper.database import daily as daily_
    from datetime import datetime, date as date_
    from helper.progress import humanbytes
    from helper.date import check_expi
    from helper.database import uploadlimit, usertype
    import time

    user_data = find_one(update.from_user.id)
    if user_data is None:
        await update.message.edit_text(
            "❌ **User not found in database!**\n\nPlease send /start first to initialize your account.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Close", callback_data="cancel")]])
        )
        return

    # Rest of the myplan logic
    daily = user_data["daily"]
    expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
    if expi != 0:
        today = date_.today()
        pattern = '%Y-%m-%d'
        epcho = int(time.mktime(time.strptime(str(today), pattern)))
        daily_(update.from_user.id, epcho)
        used_limit(update.from_user.id, 0)

    _newus = find_one(update.from_user.id)
    used = _newus["used_limit"]
    limit = _newus["uploadlimit"]
    remain = int(limit) - int(used)
    user = _newus["usertype"]
    ends = _newus["prexdate"]

    if ends:
        pre_check = check_expi(ends)
        if pre_check == False:
            uploadlimit(update.from_user.id, 10737418240)
            usertype(update.from_user.id, "Free")

    is_free_premium = _newus.get("free_premium", False)
    is_paid_premium = _newus.get("paid_premium", False)
    premium_badge = " 🎁" if (is_free_premium and not is_paid_premium) else ""

    if ends == None:
        # Format usage display - show "0 B" when usage is 0
        used_display = "0 B" if used == 0 else humanbytes(used)

        text = f"<b>User ID :</b> <code>{update.from_user.id}</code> \n<b>Name :</b> {update.from_user.mention} \n\n<b>🏷 Plan :</b> {user}{premium_badge} \n\n✓ Max File Size: 2GB \n✓ Daily Upload : {humanbytes(limit)} \n✓ Today Used : {used_display} \n✓ Remain : {humanbytes(remain)} \n✓ Timeout : 2 Minutes \n✓ Parallel process : Unlimited \n✓ Time Gap : Yes \n\n<b>Validity :</b> Lifetime"
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
        
        # Format daily upload and remain for Pro users
        if "Pro" in user:
            daily_upload_display = "Unlimited"
            remain_display = "Unlimited"
        else:
            daily_upload_display = humanbytes(limit)
            remain_display = humanbytes(remain)

        text = f"<b>User ID :</b> <code>{update.from_user.id}</code> \n<b>Name :</b> {update.from_user.mention} \n\n<b>🏷 Plan :</b> {plan_info} \n\n✓ High Priority \n✓ Max File Size: {max_file_size} \n✓ Daily Upload : {daily_upload_display} \n✓ Today Used : {used_display} \n✓ Remain : {remain_display} \n✓ Timeout : 0 Second \n✓ Parallel process : Unlimited \n✓ Time Gap : Yes \n\n<b>Your Plan Ends On :</b> {normal_date}"

    if user == "Free":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Upgrade", callback_data="upgrade")],
            [InlineKeyboardButton("⬅️ Back to Plans", callback_data="upgrade"),
             InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back to Plans", callback_data="upgrade")],
            [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
        ])

    await update.message.edit_text(text, reply_markup=keyboard, disable_web_page_preview=True)


# Developer @viizet