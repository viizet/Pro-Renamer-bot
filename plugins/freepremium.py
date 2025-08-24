from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN
from helper.database import (
    set_free_premium_config, get_free_premium_config, disable_free_premium,
    apply_free_premium_to_user, remove_free_premium_from_user, getid
)

# Duration mapping
DURATION_MAP = {
    "1day": 1,
    "30days": 30,
    "3months": 90,
    "6months": 180,
    "1year": 365
}

PLAN_MAP = {
    "basic": "🪙 Basic",
    "standard": "⚡ Standard", 
    "pro": "💎 Pro"
}

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["free"]))
async def free_premium_menu(bot, message):
    """Main free premium management menu"""
    config = get_free_premium_config()

    if config and config.get("active", False):
        status_text = f"**🎁 FREE PREMIUM STATUS: ACTIVE**\n\n"
        status_text += f"**Current Plan:** {config['plan']}\n"
        status_text += f"**Duration:** {config['duration_days']} days\n\n"
        status_text += "All new users automatically get free premium!"
    else:
        status_text = "**🎁 FREE PREMIUM STATUS: INACTIVE**\n\nNo free premium is currently active."

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Start Free Premium", callback_data="start_free_premium")],
        [InlineKeyboardButton("✏️ Change Plan/Duration", callback_data="change_free_premium")],
        [InlineKeyboardButton("👥 Apply to All Current Users", callback_data="apply_to_all")],
        [InlineKeyboardButton("🗑️ Remove Free Premium from All", callback_data="remove_from_all")],
        [InlineKeyboardButton("🚫 Stop Free Premium", callback_data="stop_free_premium")],
        [InlineKeyboardButton("❌ Close", callback_data="cancel")]
    ])

    await message.reply_text(status_text, reply_markup=keyboard, quote=True)

@Client.on_callback_query(filters.regex("start_free_premium"))
async def start_free_premium(bot, update):
    """Start configuring free premium"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 View Plans Comparison", callback_data="view_plans_comparison")],
        [InlineKeyboardButton("🪙 Basic (60GB)", callback_data="select_plan_basic")],
        [InlineKeyboardButton("⚡ Standard (60GB)", callback_data="select_plan_standard")],
        [InlineKeyboardButton("💎 Pro (150GB)", callback_data="select_plan_pro")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        "**🎁 SELECT PLAN FOR FREE PREMIUM**\n\nChoose which plan to give to users:",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("select_plan_(.+)"))
async def select_plan(bot, update):
    """Plan selection handler with detailed plan info"""
    plan_key = update.data.split("_")[-1]
    plan_name = PLAN_MAP[plan_key]

    # Detailed plan information
    plan_details = {
        "basic": {
            "daily_limit": "60GB",
            "max_file": "2GB",
            "price": "$0.50/month",
            "features": "• High Priority Processing\n• Timeout: 0 Seconds\n• Parallel Process: Unlimited\n• Time Gap: Yes"
        },
        "standard": {
            "daily_limit": "60GB", 
            "max_file": "4GB",
            "price": "$1.50/month",
            "features": "• High Priority Processing\n• Timeout: 0 Seconds\n• Parallel Process: Unlimited\n• Time Gap: Yes"
        },
        "pro": {
            "daily_limit": "150GB",
            "max_file": "4GB", 
            "price": "$3.00/month",
            "features": "• Highest Priority Processing\n• Timeout: 0 Seconds\n• Parallel Process: Unlimited\n• Time Gap: Yes"
        }
    }

    details = plan_details[plan_key]

    plan_info_text = f"**📋 PLAN DETAILS: {plan_name}**\n\n"
    plan_info_text += f"**Daily Upload Limit:** {details['daily_limit']}\n"
    plan_info_text += f"**Max File Size:** {details['max_file']}\n"
    plan_info_text += f"**Original Price:** {details['price']}\n\n"
    plan_info_text += f"**Features:**\n{details['features']}\n\n"
    plan_info_text += "**Choose duration for free premium:**"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("1 Day", callback_data=f"select_duration_{plan_key}_1day")],
        [InlineKeyboardButton("30 Days", callback_data=f"select_duration_{plan_key}_30days")],
        [InlineKeyboardButton("3 Months", callback_data=f"select_duration_{plan_key}_3months")],
        [InlineKeyboardButton("6 Months", callback_data=f"select_duration_{plan_key}_6months")],
        [InlineKeyboardButton("1 Year", callback_data=f"select_duration_{plan_key}_1year")],
        [InlineKeyboardButton("🔙 Back", callback_data="start_free_premium")]
    ])

    await update.message.edit_text(plan_info_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("select_duration_(.+)_(.+)"))
async def select_duration(bot, update):
    """Duration selection and activation"""
    parts = update.data.split("_")
    plan_key = parts[2]
    duration_key = parts[3]

    plan_name = PLAN_MAP[plan_key]
    duration_days = DURATION_MAP[duration_key]

    # Set the free premium configuration
    set_free_premium_config(plan_name, duration_days)

    duration_text = duration_key.replace("days", " days").replace("months", " months").replace("year", " year").replace("day", " day")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Apply to All Current Users", callback_data="apply_to_all")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        f"**✅ FREE PREMIUM ACTIVATED!**\n\n"
        f"**Plan:** {plan_name}\n"
        f"**Duration:** {duration_text}\n\n"
        f"All new users will automatically receive this free premium!",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("change_free_premium"))
async def change_free_premium(bot, update):
    """Change existing free premium configuration"""
    await start_free_premium(bot, update)

@Client.on_callback_query(filters.regex("apply_to_all"))
async def apply_to_all_users(bot, update):
    """Apply free premium to all existing free users only"""
    config = get_free_premium_config()

    if not config or not config.get("active", False):
        await update.answer("❌ No active free premium configuration found!", show_alert=True)
        return

    # Get all user IDs
    user_ids = getid()
    applied_count = 0
    skipped_count = 0

    await update.message.edit_text("**🔄 Applying free premium to free users only...**\n\nPlease wait...")

    for user_id in user_ids:
        if user_id != "free_premium_config":  # Skip config document
            try:
                success = apply_free_premium_to_user(user_id, config["plan"], config["duration_days"])
                if success:
                    applied_count += 1

                    # Send notification to user (existing users only, skip admin)
                    if user_id != 1096693642:  # Skip admin notifications
                        try:
                            # Determine file size limit based on plan
                            file_size = "2GB" if "Basic" in config['plan'] else "4GB"

                            await bot.send_message(
                                user_id,
                                f"🎉 Congratulations! You've been upgraded to Free Premium!\n\n"
                                f"Plan: {config['plan']}\n"
                                f"Size Upload {file_size}\n"
                                f"Duration: {config['duration_days']} days\n"
                                f"Upload Limit: {'60GB' if 'Basic' in config['plan'] or 'Standard' in config['plan'] else '150GB'}\n\n"
                                f"✨ Enjoy your premium features!\n"
                                f"Check your plan: /myplan"
                            )
                        except:
                            pass  # User might have blocked the bot
                else:
                    skipped_count += 1
            except:
                skipped_count += 1
                continue

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_free_menu")]
    ])

    # Send notification to admin
    from config import ADMIN
    try:
        await bot.send_message(
            ADMIN,
            f"📊 **FREE PREMIUM BULK APPLICATION COMPLETED**\n\n"
            f"**Plan:** {config['plan']}\n"
            f"**Duration:** {config['duration_days']} days\n"
            f"**Successfully Applied:** {applied_count} users\n"
            f"**Skipped:** {skipped_count} users (paid premium)"
        )
    except:
        pass

    await update.message.edit_text(
        f"**✅ FREE PREMIUM APPLIED!**\n\n"
        f"Successfully applied {config['plan']} for {config['duration_days']} days to {applied_count} free users!\n"
        f"Skipped {skipped_count} paid premium users.",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("remove_from_all"))
async def remove_free_premium_from_all(bot, update):
    """Remove free premium from all free premium users only (NOT paid premium users)"""
    from helper.database import find_one

    user_ids = getid()
    removed_count = 0
    skipped_paid_count = 0

    await update.message.edit_text("**🔄 Removing free premium from free users only...**\n\nPlease wait...")

    for user_id in user_ids:
        if user_id != "free_premium_config":  # Skip config document
            try:
                user_data = find_one(user_id)
                if user_data:
                    # Only remove from users who have free premium (NOT paid premium)
                    if user_data.get("free_premium", False) and not user_data.get("paid_premium", False):
                        remove_free_premium_from_user(user_id)
                        removed_count += 1

                        # Send notification to user (skip admin)
                        if user_id != 1096693642:  # Skip admin notifications
                            try:
                                await bot.send_message(
                                    user_id,
                                    "⚠️ **Your free premium has been removed by admin.**\n\nYou are now on the Free plan. Check /myplan for details."
                                )
                            except:
                                pass  # User might have blocked the bot
                    elif user_data.get("paid_premium", False):
                        skipped_paid_count += 1
            except Exception as e:
                print(f"Error removing free premium from user {user_id}: {e}")
                continue

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_free_menu")]
    ])

    # Send notification to admin
    from config import ADMIN
    try:
        await bot.send_message(
            ADMIN,
            f"📊 **FREE PREMIUM BULK REMOVAL COMPLETED**\n\n"
            f"**Successfully Removed:** {removed_count} free premium users\n"
            f"**Skipped:** {skipped_paid_count} paid premium users"
        )
    except:
        pass

    status_text = f"**✅ FREE PREMIUM REMOVED!**\n\n"
    status_text += f"Successfully removed free premium from {removed_count} free users!\n"
    if skipped_paid_count > 0:
        status_text += f"Skipped {skipped_paid_count} paid premium users (use /removepremium for them)."

    await update.message.edit_text(status_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("stop_free_premium"))
async def stop_free_premium(bot, update):
    """Stop free premium"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, Stop", callback_data="confirm_stop_free")],
        [InlineKeyboardButton("❌ Cancel", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        "**⚠️ CONFIRM STOP FREE PREMIUM**\n\n"
        "This will:\n"
        "• Stop giving free premium to new users\n"
        "• Current users will keep their premium until it expires\n\n"
        "Are you sure?",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("confirm_stop_free"))
async def confirm_stop_free(bot, update):
    """Confirm stopping free premium"""
    disable_free_premium()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        "**🚫 FREE PREMIUM STOPPED**\n\n"
        "New users will no longer receive free premium.\n"
        "Existing premium users will keep their access until expiry.",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("view_plans_comparison"))
async def view_plans_comparison(bot, update):
    """Show detailed comparison of all plans"""
    comparison_text = """**📊 DETAILED PLANS COMPARISON**

**🆓 FREE PLAN**
• Daily Upload Limit: 15GB
• Max File Size: 2GB
• Timeout: 2 Minutes
• Parallel Process: Unlimited
• Time Gap: Yes
• Validity: Lifetime
• Price: FREE

**🪙 BASIC PLAN**
• Daily Upload Limit: 60GB
• Max File Size: 2GB
• High Priority Processing
• Timeout: 0 Seconds
• Parallel Process: Unlimited
• Time Gap: Yes
• Price: $0.50 per Month

**⚡ STANDARD PLAN**
• Daily Upload Limit: 60GB
• Max File Size: 4GB
• High Priority Processing
• Timeout: 0 Seconds
• Parallel Process: Unlimited
• Time Gap: Yes
• Price: $1.50 per Month

**💎 PRO PLAN**
• Daily Upload Limit: 150GB
• Max File Size: 4GB
• Highest Priority Processing
• Timeout: 0 Seconds
• Parallel Process: Unlimited
• Time Gap: Yes
• Price: $3.00 per Month

Select which plan to offer as free premium:"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Basic (60GB)", callback_data="select_plan_basic")],
        [InlineKeyboardButton("⚡ Standard (60GB)", callback_data="select_plan_standard")], 
        [InlineKeyboardButton("💎 Pro (150GB)", callback_data="select_plan_pro")],
        [InlineKeyboardButton("🔙 Back", callback_data="start_free_premium")]
    ])

    await update.message.edit_text(comparison_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("back_to_free_menu"))
async def back_to_free_menu(bot, update):
    """Go back to main free premium menu"""
    config = get_free_premium_config()

    if config and config.get("active", False):
        status_text = f"**🎁 FREE PREMIUM STATUS: ACTIVE**\n\n"
        status_text += f"**Current Plan:** {config['plan']}\n"
        status_text += f"**Duration:** {config['duration_days']} days\n\n"
        status_text += "All new users automatically get free premium!"
    else:
        status_text = "**🎁 FREE PREMIUM STATUS: INACTIVE**\n\nNo free premium is currently active."

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Start Free Premium", callback_data="start_free_premium")],
        [InlineKeyboardButton("✏️ Change Plan/Duration", callback_data="change_free_premium")],
        [InlineKeyboardButton("👥 Apply to All Current Users", callback_data="apply_to_all")],
        [InlineKeyboardButton("🗑️ Remove Free Premium from All", callback_data="remove_from_all")],
        [InlineKeyboardButton("🚫 Stop Free Premium", callback_data="stop_free_premium")],
        [InlineKeyboardButton("❌ Close", callback_data="cancel")]
    ])

    await update.message.edit_text(status_text, reply_markup=keyboard)

# Command to remove free premium from specific user (admin only)
@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["removefree"]))
async def remove_free_premium_cmd(bot, message):
    """Remove free premium from a specific user"""
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /removefree <user_id>", quote=True)
        return

    try:
        user_id = int(message.command[1])

        # Check if user has free premium
        from helper.database import find_one
        user_data = find_one(user_id)
        if not user_data or not user_data.get("free_premium", False):
            await message.reply_text(f"❌ User {user_id} doesn't have free premium!", quote=True)
            return

        # Get user info for notification
        try:
            user_info = await bot.get_users(user_id)
            user_name = user_info.first_name
        except:
            user_name = "Unknown User"

        remove_free_premium_from_user(user_id)
        await message.reply_text(f"✅ **Free premium removed from user:** `{user_id}`", quote=True)

        # Notify the user (skip admin)
        if user_id != 1096693642:  # Skip admin notifications
            try:
                await bot.send_message(
                    user_id, 
                    "⚠️ **Your free premium has been removed by admin.**\n\nYou are now on the Free plan. Check /myplan for details."
                )
            except:
                pass

        # Send notification to admin (same admin but detailed info)
        await message.reply_text(
            f"📊 **FREE PREMIUM REMOVAL NOTIFICATION**\n\n"
            f"**User:** {user_name}\n"
            f"**User ID:** `{user_id}`\n"
            f"**Action:** Free Premium Removed\n"
            f"**Status:** ✅ Success", 
            quote=True
        )

    except ValueError:
        await message.reply_text("❌ **Invalid user ID!**", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}", quote=True)


# Command to show detailed plan information for all users
@Client.on_message(filters.private & filters.command(["free"]))
async def show_plans_info(bot, message):
    """Show detailed information about all available plans"""
    text = """**📢 DETAILED UPLOAD LIMITS & PLANS**

**✅ FREE USERS**
• Daily Upload Limit: 15GB
• Max File Size: 2GB
• Timeout: 2 Minutes
• Parallel Process: Unlimited
• Time Gap: Yes
• Validity: Lifetime
• Price: FREE

**🪙 BASIC USERS**
• Daily Upload Limit: 60GB
• Max File Size: 2GB
• High Priority Processing
• Timeout: 0 Seconds
• Parallel Process: Unlimited
• Time Gap: Yes
• Price: 🌎 $0.50 per Month

**⚡ STANDARD USERS**
• Daily Upload Limit: 60GB
• Max File Size: 4GB
• High Priority Processing
• Timeout: 0 Seconds
• Parallel Process: Unlimited
• Time Gap: Yes
• Price: 🌎 $1.50 per Month

**💎 PRO USERS**
• Daily Upload Limit: 150GB
• Max File Size: 4GB
• Highest Priority Processing
• Timeout: 0 Seconds
• Parallel Process: Unlimited
• Time Gap: Yes
• Price: 🌎 $3.00 per Month

**📝 Features Comparison:**
✓ All plans support unlimited parallel processing
✓ Premium plans get priority processing
✓ Standard & Pro plans support larger files (4GB)
✓ Pro plan offers the highest daily upload limit

**💳 Want to upgrade?** Use /upgrade command
**📊 Check your current plan:** Use /myplan command"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Upgrade Plan", callback_data="upgrade")],
        [InlineKeyboardButton("📊 My Current Plan", url="https://t.me/{bot.username}?start=myplan")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
    ])

    await message.reply_text(text, reply_markup=keyboard, quote=True)