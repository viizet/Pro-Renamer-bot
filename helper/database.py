import pymongo
from datetime import datetime
from config import DATABASE_URL, DATABASE_NAME
from helper.date import add_date

mongo = pymongo.MongoClient(DATABASE_URL)
db = mongo[DATABASE_NAME]
dbcol = db["user"]



# Total User
def total_user():
    user = dbcol.count_documents({})
    return user


# Insert Bot Data
def botdata(chat_id):
    bot_id = int(chat_id)
    try:
        bot_data = {"_id": bot_id, "total_rename": 0, "total_size": 0}
        dbcol.insert_one(bot_data)
    except:
        pass


# Total Renamed Files
def total_rename(chat_id, renamed_file):
    now = int(renamed_file) + 1
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_rename": str(now)}})


# Total Renamed File Size
def total_size(chat_id, total_size, now_file_size):
    now = int(total_size) + now_file_size
    dbcol.update_one({"_id": chat_id}, {"$set": {"total_size": str(now)}})


# Insert User Data
def insert(chat_id):
    user_id = int(chat_id)
    user_det = {"_id": user_id, "file_id": None, "caption": None, "daily": 0, "date": 0,
                "uploadlimit": 2147483652, "used_limit": 0, "usertype": "Free", "prexdate": None,
                "metadata": False, "metadata_code": "By @Madflix_Bots", "free_premium": False, "paid_premium": False}
    try:
        dbcol.insert_one(user_det)

        # Check if free premium is active and apply it to new user (only for free users)
        free_config = get_free_premium_config()
        if free_config and free_config.get("active", False):
            apply_free_premium_to_user(user_id, free_config["plan"], free_config["duration_days"])

    except:
        return True
        pass


# Add Thumbnail Data
def addthumb(chat_id, file_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": file_id}})

def delthumb(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"file_id": None}})




# ============= Metadata Function Code =============== #

def setmeta(chat_id, bool_meta):
    dbcol.update_one({"_id": chat_id}, {"$set": {"metadata": bool_meta}})

def setmetacode(chat_id, metadata_code):
    dbcol.update_one({"_id": chat_id}, {"$set": {"metadata_code": metadata_code}})

# ============= Metadata Function Code =============== #



# Add Caption Data
def addcaption(chat_id, caption):
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": caption}})

def delcaption(chat_id):
    dbcol.update_one({"_id": chat_id}, {"$set": {"caption": None}})



def dateupdate(chat_id, date):
    dbcol.update_one({"_id": chat_id}, {"$set": {"date": date}})

def used_limit(chat_id, used):
    dbcol.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})

def usertype(chat_id, type):
    dbcol.update_one({"_id": chat_id}, {"$set": {"usertype": type}})

def uploadlimit(chat_id, limit):
    dbcol.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})


# Add Premium Data
def addpre(chat_id):
    date = add_date()
    dbcol.update_one({"_id": chat_id}, {"$set": {"prexdate": date[0]}})

def addpredata(chat_id):
    user_id = int(chat_id)
    user_data = dbcol.find_one({"_id": user_id})
    if user_data:
        dbcol.update_one({"_id": user_id}, {"$set": {"prexdate": None}}) # Assuming addpredata is for removing premium
    else:
        pass # User not found, do nothing

def ban_user(user_id, reason="No reason provided"):
    user_id = int(user_id)
    dbcol.update_one(
        {"_id": user_id},
        {"$set": {"banned": True, "ban_reason": reason}},
        upsert=True
    )

def unban_user(user_id):
    user_id = int(user_id)
    dbcol.update_one(
        {"_id": user_id},
        {"$set": {"banned": False, "ban_reason": None}}
    )

def is_user_banned(user_id):
    user_id = int(user_id)
    user_data = dbcol.find_one({"_id": user_id})
    if user_data:
        return user_data.get("banned", False)
    return False

def get_user_statistics():
    try:
        # Count total users (excluding config documents)
        total_users = dbcol.count_documents({"_id": {"$ne": "free_premium_config"}})

        # Count premium users (users with premium plans or free premium)
        premium_users = dbcol.count_documents({
            "_id": {"$ne": "free_premium_config"},
            "$or": [
                {"usertype": {"$regex": "Basic|Standard|Pro", "$options": "i"}},
                {"free_premium": True}
            ]
        })

        # Count free users (users with Free usertype and no premium status)
        free_users = dbcol.count_documents({
            "_id": {"$ne": "free_premium_config"},
            "usertype": "Free",
            "$or": [
                {"free_premium": {"$exists": False}},
                {"free_premium": False}
            ]
        })

        # Count banned users
        banned_users = dbcol.count_documents({
            "_id": {"$ne": "free_premium_config"},
            "banned": True
        })

        return {
            "total_users": total_users,
            "premium_users": premium_users,
            "free_users": free_users,
            "banned_users": banned_users
        }
    except Exception as e:
        print(f"Error getting user statistics: {e}")
        return {
            "total_users": 0,
            "premium_users": 0,
            "free_users": 0,
            "banned_users": 0
        }


def find(chat_id):
    id = {"_id": chat_id}
    x = dbcol.find(id)
    for i in x:
        file = i["file_id"]
        try:
            caption = i["caption"]
        except:
            caption = None
        try:
            metadata = i["metadata"]
        except:
            metadata = False
        try:
            metadata_code = i["metadata_code"]
        except:
            metadata_code = None

        return [file, caption, metadata, metadata_code]

def getid():
    values = []
    for key in dbcol.find():
        id = key["_id"]
        values.append((id))
    return values

def delete(id):
    dbcol.delete_one(id)

def find_one(id):
    return dbcol.find_one({"_id": id})

# Free Premium System Functions
def set_free_premium_config(plan, duration_days):
    """Set free premium configuration"""
    config = {
        "_id": "free_premium_config",
        "active": True,
        "plan": plan,
        "duration_days": duration_days
    }
    dbcol.replace_one({"_id": "free_premium_config"}, config, upsert=True)

def get_free_premium_config():
    """Get free premium configuration"""
    return dbcol.find_one({"_id": "free_premium_config"})

def disable_free_premium():
    """Disable free premium"""
    dbcol.update_one(
        {"_id": "free_premium_config"}, 
        {"$set": {"active": False}}
    )

def apply_free_premium_to_user(user_id, plan, duration_days):
    """Apply free premium to a user"""
    from datetime import datetime, timedelta

    # Calculate expiry date
    expiry_date = datetime.now() + timedelta(days=duration_days)
    expiry_timestamp = expiry_date.strftime('%Y-%m-%d')

    # Set premium limits based on plan
    if "Basic" in plan:
        limit = 21474836480  # 20GB
    elif "Standard" in plan:
        limit = 53687091200  # 50GB
    elif "Pro" in plan:
        limit = 107374182400  # 100GB
    else:
        limit = 21474836480  # Default to Basic

    dbcol.update_one(
        {"_id": user_id}, 
        {"$set": {
            "free_premium": True,
            "usertype": plan,
            "uploadlimit": limit,
            "prexdate": expiry_timestamp
        }}
    )

def remove_free_premium_from_user(user_id):
    """Remove free premium from a user"""

def set_free_premium_config(plan, duration_days):
    """Set global free premium configuration"""
    config_data = {"_id": "free_premium_config", "plan": plan, "duration_days": duration_days, "active": True}
    dbcol.replace_one({"_id": "free_premium_config"}, config_data, upsert=True)

def get_free_premium_config():
    """Get current free premium configuration"""
    return dbcol.find_one({"_id": "free_premium_config"})

def disable_free_premium():
    """Disable free premium for new users"""
    dbcol.update_one({"_id": "free_premium_config"}, {"$set": {"active": False}})

def apply_free_premium_to_user(user_id, plan, duration_days):
    """Apply free premium to a specific user (only if they are free users)"""
    from helper.date import add_custom_date

    # Check if user exists and is not a paid premium user
    user_data = find_one(user_id)
    if not user_data:
        return False
    
    # Do not apply free premium to paid premium users
    if user_data.get("paid_premium", False):
        return False
    
    # Only apply to users with "Free" usertype
    if user_data.get("usertype") != "Free":
        return False

    # Set plan limits based on plan type
    if plan == "🪙 Basic":
        limit = 21474836500  # 20GB
    elif plan == "⚡ Standard":
        limit = 53687091200  # 50GB
    elif plan == "💎 Pro":
        limit = 107374182400  # 100GB
    else:
        limit = 2147483652  # Default 2GB

    # Calculate expiry date
    expiry_date = add_custom_date(duration_days)

    # Update user data
    uploadlimit(user_id, limit)
    usertype(user_id, plan)
    dbcol.update_one({"_id": user_id}, {"$set": {"prexdate": expiry_date[0], "free_premium": True}})
    return True

def remove_free_premium_from_user(user_id):
    """Remove free premium from a user"""
    uploadlimit(user_id, 2147483652)  # Reset to 2GB
    usertype(user_id, "Free")
    dbcol.update_one({"_id": user_id}, {"$set": {"prexdate": None, "free_premium": False}})

def daily(chat_id, date):
    """Update daily usage date"""
    dbcol.update_one({"_id": chat_id}, {"$set": {"daily": date}})