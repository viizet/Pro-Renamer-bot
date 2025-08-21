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
        [InlineKeyboardButton("🪙 Basic (20GB)", callback_data="select_plan_basic")],
        [InlineKeyboardButton("⚡ Standard (50GB)", callback_data="select_plan_standard")],
        [InlineKeyboardButton("💎 Pro (100GB)", callback_data="select_plan_pro")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        "**🎁 SELECT PLAN FOR FREE PREMIUM**\n\nChoose which plan to give to users:",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("select_plan_(.+)"))
async def select_plan(bot, update):
    """Plan selection handler"""
    plan_key = update.data.split("_")[-1]
    plan_name = PLAN_MAP[plan_key]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("1 Day", callback_data=f"select_duration_{plan_key}_1day")],
        [InlineKeyboardButton("30 Days", callback_data=f"select_duration_{plan_key}_30days")],
        [InlineKeyboardButton("3 Months", callback_data=f"select_duration_{plan_key}_3months")],
        [InlineKeyboardButton("6 Months", callback_data=f"select_duration_{plan_key}_6months")],
        [InlineKeyboardButton("1 Year", callback_data=f"select_duration_{plan_key}_1year")],
        [InlineKeyboardButton("🔙 Back", callback_data="start_free_premium")]
    ])

    await update.message.edit_text(
        f"**🎁 SELECT DURATION FOR {plan_name}**\n\nChoose how long the free premium should last:",
        reply_markup=keyboard
    )

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
                else:
                    skipped_count += 1
            except:
                skipped_count += 1
                continue

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        f"**✅ FREE PREMIUM APPLIED!**\n\n"
        f"Successfully applied {config['plan']} for {config['duration_days']} days to {applied_count} free users!\n"
        f"Skipped {skipped_count} paid premium users.",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("remove_from_all"))
async def remove_free_premium_from_all(bot, update):
    """Remove free premium from all users"""
    user_ids = getid()
    removed_count = 0

    await update.message.edit_text("**🔄 Removing free premium from all users...**\n\nPlease wait...")

    for user_id in user_ids:
        if user_id != "free_premium_config":  # Skip config document
            try:
                remove_free_premium_from_user(user_id)
                removed_count += 1
            except Exception as e:
                print(f"Error removing free premium from user {user_id}: {e}")
                continue

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_free_menu")]
    ])

    await update.message.edit_text(
        f"**✅ FREE PREMIUM REMOVED!**\n\n"
        f"Successfully removed free premium from {removed_count} users!",
        reply_markup=keyboard
    )

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
        remove_free_premium_from_user(user_id)
        await message.reply_text(f"✅ **Free premium removed from user:** `{user_id}`", quote=True)

        # Notify the user
        try:
            await bot.send_message(
                user_id, 
                "⚠️ **Your free premium has been removed by admin.**\n\nYou are now on the Free plan. Check /myplan for details."
            )
        except:
            pass

    except ValueError:
        await message.reply_text("❌ **Invalid user ID!**", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}", quote=True)


