
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN, BOT_TOKEN
from helper.database import find_one, getid, get_user_statistics, botdata
from helper.progress import humanbytes

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["stats"]))
async def stats_menu(bot, message):
    """Main listall menu with user category buttons"""
    # Get user statistics
    stats = get_user_statistics()
    
    # Get bot file statistics
    token = BOT_TOKEN
    botid = token.split(':')[0]
    botdata(int(botid))
    data = find_one(int(botid))
    total_rename = data["total_rename"] if data and "total_rename" in data else 0
    total_size = data["total_size"] if data and "total_size" in data else 0
    
    status_text = f"""**📊 USER MANAGEMENT PANEL**

**Total Statistics:**
👥 Total Users: {stats['total_users']}
💎 Premium Users: {stats['premium_users']}
🆓 Free Users: {stats['free_users']}
🚫 Banned Users: {stats['banned_users']}

**📁 FILE STATISTICS:**
• Total Files Renamed: {total_rename}
• Total Size Processed: {humanbytes(int(total_size)) if total_size else "0 B"}

**Select category to view users:**"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Paid Premium Users", callback_data="list_paid_premium")],
        [InlineKeyboardButton("🎁 Free Premium Users", callback_data="list_free_premium")],
        [InlineKeyboardButton("🆓 Free Users", callback_data="list_free_users")],
        [InlineKeyboardButton("🚫 Banned Users", callback_data="list_banned_users")],
        [InlineKeyboardButton("📊 All Users", callback_data="list_all_users")],
        [InlineKeyboardButton("🔄 Refresh Stats", callback_data="refresh_listall")],
        [InlineKeyboardButton("❌ Close", callback_data="cancel")]
    ])

    await message.reply_text(status_text, reply_markup=keyboard, quote=True)

@Client.on_callback_query(filters.regex("list_paid_premium"))
async def list_paid_premium(bot, update):
    """List all paid premium users with plan expiry dates"""
    try:
        user_ids = getid()
        paid_premium_users = []
        
        for user_id in user_ids:
            if user_id != "free_premium_config":
                try:
                    user_data = find_one(user_id)
                    if user_data:
                        # Check for paid premium users (users with premium plans but not free premium)
                        user_type = user_data.get("usertype", "Unknown")
                        is_paid_premium = user_data.get("paid_premium", False)
                        is_free_premium = user_data.get("free_premium", False)
                        
                        # Consider as paid premium if: explicitly marked as paid_premium OR has premium plan but not free_premium
                        if is_paid_premium or (user_type in ["🪙 Basic", "⚡ Standard", "💎 Pro"] and not is_free_premium):
                            used = user_data.get("used_limit", 0)
                            limit = user_data.get("uploadlimit", 0)
                            expiry_date = user_data.get("prexdate", "N/A")
                            
                            try:
                                used_str = humanbytes(used) if used else "0 B"
                                limit_str = humanbytes(limit) if limit else "0 B"
                                
                                # Format expiry status
                                if expiry_date and expiry_date != "N/A":
                                    from datetime import datetime
                                    try:
                                        if isinstance(expiry_date, str):
                                            expiry_display = expiry_date
                                        else:
                                            expiry_display = datetime.fromtimestamp(expiry_date).strftime('%Y-%m-%d')
                                        
                                        # Check if expired
                                        current_date = datetime.now().strftime('%Y-%m-%d')
                                        if expiry_display < current_date:
                                            status_emoji = "⏰"
                                            status_text = f"EXPIRED ({expiry_display})"
                                        else:
                                            status_emoji = "✅"
                                            status_text = f"Valid until {expiry_display}"
                                    except:
                                        status_emoji = "❓"
                                        status_text = f"Expires: {expiry_date}"
                                else:
                                    status_emoji = "♾️"
                                    status_text = "Lifetime"
                                
                                paid_premium_users.append(
                                    f"**👤 User ID:** `{user_id}`\n"
                                    f"**📊 Plan:** {user_type}\n"
                                    f"**📈 Usage:** {used_str}/{limit_str}\n"
                                    f"**{status_emoji} Expiry:** {status_text}\n"
                                    f"{'─' * 30}"
                                )
                            except Exception as e:
                                paid_premium_users.append(f"• `{user_id}` - {user_type} - Error loading data")
                except Exception as e:
                    continue
        
        if not paid_premium_users:
            text = "**💎 PAID PREMIUM USERS**\n\n❌ No paid premium users found."
        else:
            text = f"**💎 PAID PREMIUM USERS ({len(paid_premium_users)})**\n\n" + "\n\n".join(paid_premium_users[:10])
            if len(paid_premium_users) > 10:
                text += f"\n\n**📊 Showing 10 of {len(paid_premium_users)} users**"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        
        await update.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        error_text = f"❌ **Error loading paid premium users:**\n{str(e)}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        await update.message.edit_text(error_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_free_premium"))
async def list_free_premium(bot, update):
    """List all free premium users with expiry dates"""
    try:
        user_ids = getid()
        free_premium_users = []
        
        for user_id in user_ids:
            if user_id != "free_premium_config":
                try:
                    user_data = find_one(user_id)
                    if user_data and user_data.get("free_premium", False) and not user_data.get("paid_premium", False):
                        user_type = user_data.get("usertype", "Unknown")
                        used = user_data.get("used_limit", 0)
                        limit = user_data.get("uploadlimit", 0)
                        expiry_date = user_data.get("prexdate", "N/A")
                        
                        try:
                            used_str = humanbytes(used) if used else "0 B"
                            limit_str = humanbytes(limit) if limit else "0 B"
                        except:
                            used_str = "0 B"
                            limit_str = "0 B"
                        
                        # Format expiry status
                        if expiry_date and expiry_date != "N/A":
                            from datetime import datetime
                            try:
                                if isinstance(expiry_date, str):
                                    expiry_display = expiry_date
                                else:
                                    expiry_display = datetime.fromtimestamp(expiry_date).strftime('%Y-%m-%d')
                                
                                # Check if expired
                                current_date = datetime.now().strftime('%Y-%m-%d')
                                if expiry_display < current_date:
                                    status_emoji = "⏰"
                                    status_text = f"EXPIRED ({expiry_display})"
                                else:
                                    status_emoji = "✅"
                                    status_text = f"Valid until {expiry_display}"
                            except:
                                status_emoji = "❓"
                                status_text = f"Expires: {expiry_date}"
                        else:
                            status_emoji = "🎁"
                            status_text = "Active"
                        
                        free_premium_users.append(
                            f"**👤 User ID:** `{user_id}`\n"
                            f"**📊 Plan:** {user_type} 🎁\n"
                            f"**📈 Usage:** {used_str}/{limit_str}\n"
                            f"**{status_emoji} Status:** {status_text}\n"
                            f"{'─' * 30}"
                        )
                except Exception as e:
                    continue
        
        if not free_premium_users:
            text = "**🎁 FREE PREMIUM USERS**\n\n❌ No free premium users found."
        else:
            text = f"**🎁 FREE PREMIUM USERS ({len(free_premium_users)})**\n\n" + "\n\n".join(free_premium_users[:10])
            if len(free_premium_users) > 10:
                text += f"\n\n**📊 Showing 10 of {len(free_premium_users)} users**"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        
        await update.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        error_text = f"❌ **Error loading free premium users:**\n{str(e)}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        await update.message.edit_text(error_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_free_users"))
async def list_free_users(bot, update):
    """List all free users with detailed information"""
    try:
        user_ids = getid()
        free_users = []
        
        for user_id in user_ids:
            if user_id != "free_premium_config":
                try:
                    user_data = find_one(user_id)
                    if user_data and user_data.get("usertype") == "Free" and not user_data.get("free_premium", False) and not user_data.get("paid_premium", False):
                        used = user_data.get("used_limit", 0)
                        limit = user_data.get("uploadlimit", 0)
                        
                        try:
                            used_str = humanbytes(used) if used else "0 B"
                            limit_str = humanbytes(limit) if limit else "10 GB"
                        except:
                            used_str = "0 B"
                            limit_str = "10 GB"
                        
                        # Calculate usage percentage
                        try:
                            usage_percent = (used / limit * 100) if limit > 0 else 0
                            if usage_percent < 50:
                                usage_emoji = "🟢"
                            elif usage_percent < 80:
                                usage_emoji = "🟡"
                            else:
                                usage_emoji = "🔴"
                        except:
                            usage_emoji = "⚪"
                            usage_percent = 0
                        
                        free_users.append(
                            f"**👤 User ID:** `{user_id}`\n"
                            f"**📊 Plan:** Free 🆓\n"
                            f"**📈 Usage:** {used_str}/{limit_str}\n"
                            f"**{usage_emoji} Progress:** {usage_percent:.1f}% used\n"
                            f"{'─' * 30}"
                        )
                except Exception as e:
                    continue
        
        if not free_users:
            text = "**🆓 FREE USERS**\n\n❌ No free users found."
        else:
            text = f"**🆓 FREE USERS ({len(free_users)})**\n\n" + "\n\n".join(free_users[:10])
            if len(free_users) > 10:
                text += f"\n\n**📊 Showing 10 of {len(free_users)} users**"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        
        await update.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        error_text = f"❌ **Error loading free users:**\n{str(e)}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        await update.message.edit_text(error_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_banned_users"))
async def list_banned_users(bot, update):
    """List all banned users with detailed ban information"""
    try:
        user_ids = getid()
        banned_users = []
        
        for user_id in user_ids:
            if user_id != "free_premium_config":
                try:
                    user_data = find_one(user_id)
                    if user_data and user_data.get("banned", False):
                        ban_reason = user_data.get("ban_reason", "No reason provided")
                        user_type = user_data.get("usertype", "Unknown")
                        used = user_data.get("used_limit", 0)
                        limit = user_data.get("uploadlimit", 0)
                        
                        try:
                            used_str = humanbytes(used) if used else "0 B"
                            limit_str = humanbytes(limit) if limit else "0 B"
                        except:
                            used_str = "0 B"
                            limit_str = "0 B"
                        
                        # Format ban reason for better display
                        if len(ban_reason) > 50:
                            display_reason = ban_reason[:47] + "..."
                        else:
                            display_reason = ban_reason
                        
                        banned_users.append(
                            f"**👤 User ID:** `{user_id}`\n"
                            f"**📊 Plan:** {user_type}\n"
                            f"**📈 Usage:** {used_str}/{limit_str}\n"
                            f"**🚫 Ban Reason:** {display_reason}\n"
                            f"{'─' * 30}"
                        )
                except Exception as e:
                    continue
        
        if not banned_users:
            text = "**🚫 BANNED USERS**\n\n✅ No banned users found."
        else:
            text = f"**🚫 BANNED USERS ({len(banned_users)})**\n\n" + "\n\n".join(banned_users[:10])
            if len(banned_users) > 10:
                text += f"\n\n**📊 Showing 10 of {len(banned_users)} users**"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        
        await update.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        error_text = f"❌ **Error loading banned users:**\n{str(e)}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        await update.message.edit_text(error_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("list_all_users"))
async def list_all_users(bot, update):
    """List all users with their status"""
    try:
        user_ids = getid()
        all_users = []
        
        for user_id in user_ids:
            if user_id != "free_premium_config":
                try:
                    user_data = find_one(user_id)
                    if user_data:
                        user_type = user_data.get("usertype", "Unknown")
                        is_banned = user_data.get("banned", False)
                        is_paid_premium = user_data.get("paid_premium", False)
                        is_free_premium = user_data.get("free_premium", False)
                        
                        status = "🚫 Banned" if is_banned else (
                            "💎 Paid Premium" if is_paid_premium else (
                                "🎁 Free Premium" if is_free_premium else "🆓 Free"
                            )
                        )
                        
                        used = user_data.get("used_limit", 0)
                        limit = user_data.get("uploadlimit", 0)
                        try:
                            used_str = humanbytes(used) if used else "0 B"
                            limit_str = humanbytes(limit) if limit else "0 B"
                            all_users.append(f"• `{user_id}` - {status} - {user_type} - {used_str}/{limit_str}")
                        except Exception as e:
                            all_users.append(f"• `{user_id}` - {status} - {user_type} - Error/Error")
                except Exception as e:
                    continue
        
        if not all_users:
            text = "**📊 ALL USERS**\n\nNo users found."
        else:
            text = f"**📊 ALL USERS ({len(all_users)})**\n\n" + "\n".join(all_users[:15])
            if len(all_users) > 15:
                text += f"\n\n... and {len(all_users) - 15} more users"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        
        await update.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        error_text = f"❌ **Error loading all users:**\n{str(e)}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="refresh_listall")]
        ])
        await update.message.edit_text(error_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("refresh_listall"))
async def refresh_listall(bot, update):
    """Refresh the listall menu"""
    try:
        # Get user statistics
        stats = get_user_statistics()
        
        # Get bot file statistics
        token = BOT_TOKEN
        botid = token.split(':')[0]
        botdata(int(botid))
        data = find_one(int(botid))
        total_rename = data["total_rename"] if data and "total_rename" in data else 0
        total_size = data["total_size"] if data and "total_size" in data else 0
        
        # Add timestamp to prevent MESSAGE_NOT_MODIFIED error
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        status_text = f"""**📊 USER MANAGEMENT PANEL**

**Total Statistics:**
👥 Total Users: {stats['total_users']}
💎 Premium Users: {stats['premium_users']}
🆓 Free Users: {stats['free_users']}
🚫 Banned Users: {stats['banned_users']}

**📁 FILE STATISTICS:**
• Total Files Renamed: {total_rename}
• Total Size Processed: {humanbytes(int(total_size)) if total_size else "0 B"}

**Select category to view users:**

*Last updated: {timestamp}*"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Paid Premium Users", callback_data="list_paid_premium")],
            [InlineKeyboardButton("🎁 Free Premium Users", callback_data="list_free_premium")],
            [InlineKeyboardButton("🆓 Free Users", callback_data="list_free_users")],
            [InlineKeyboardButton("🚫 Banned Users", callback_data="list_banned_users")],
            [InlineKeyboardButton("📊 All Users", callback_data="list_all_users")],
            [InlineKeyboardButton("🔄 Refresh Stats", callback_data="refresh_listall")],
            [InlineKeyboardButton("❌ Close", callback_data="cancel")]
        ])

        try:
            await update.message.edit_text(status_text, reply_markup=keyboard)
        except Exception as edit_error:
            if "MESSAGE_NOT_MODIFIED" in str(edit_error):
                await update.answer("📊 Statistics are already up to date!", show_alert=True)
            else:
                raise edit_error
    except Exception as e:
        error_text = f"❌ **Error refreshing stats:**\n{str(e)}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Try Again", callback_data="refresh_listall")],
            [InlineKeyboardButton("❌ Close", callback_data="cancel")]
        ])
        try:
            await update.message.edit_text(error_text, reply_markup=keyboard)
        except:
            await update.answer(f"Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("cancel"))
async def cancel_callback(bot, update):
    """Handle cancel button"""
    await update.message.delete()

# Developer @viizet
