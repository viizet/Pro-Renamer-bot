from pyrogram import Client, idle
from plugins.cb_data import app as Client2
from config import *
import pyromod
import pyrogram.utils
import threading
from flask import Flask

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# Flask web server for health checks
web_app = Flask(__name__)

@web_app.route('/')
def hello_world():
    return '@viizet - Bot is running!'

@web_app.route('/health')
def health():
    return 'OK'

def run_flask():
    from waitress import serve
    serve(web_app, host='0.0.0.0', port=5000, threads=6)

bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

# Start Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

if STRING_SESSION:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()




# VIIZET Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Phioza
# Back-Up Channel @Phioza
# Developer @viizet
