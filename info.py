import re
import os
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
PORT = environ.get("PORT", "8080")
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS', 'https://telegra.ph/file/7e56d907542396289fee4.jpg https://telegra.ph/file/9aa8dd372f4739fe02d85.jpg https://telegra.ph/file/adffc5ce502f5578e2806.jpg https://telegra.ph/file/6937b60bc2617597b92fd.jpg https://telegra.ph/file/09a7abaab340143f9c7e7.jpg https://telegra.ph/file/5a82c4a59bd04d415af1c.jpg https://telegra.ph/file/323986d3bd9c4c1b3cb26.jpg https://telegra.ph/file/b8a82dcb89fb296f92ca0.jpg https://telegra.ph/file/31adab039a85ed88e22b0.jpg https://telegra.ph/file/c0e0f4c3ed53ac8438f34.jpg https://telegra.ph/file/eede835fb3c37e07c9cee.jpg https://telegra.ph/file/e17d2d068f71a9867d554.jpg https://telegra.ph/file/8fb1ae7d995e8735a7c25.jpg https://telegra.ph/file/8fed19586b4aa019ec215.jpg https://telegra.ph/file/8e6c923abd6139083e1de.jpg https://telegra.ph/file/0049d801d29e83d68b001.jpg')).split()
MQTTP = environ.get("MQTTP", "https://telegra.ph/file/67b8db0ce0338a7a109a0.png")
BOT_START_TIME = time()

# Filter Buttons 
MALTI_BUTTONS = os.environ.get("MALTI_BUTTONS", "6")

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None


# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Rajappan")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', '<b>👋HELLO {user}\n\n MY NAME IS {bot},\n I CAN PROVIDE MOVIES, JUST SEND ME THE NAME OF MOVIE</b>')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "⚠️ 𝙃𝙚𝙮 {query}! 𝙏𝙝𝙖𝙩'𝙨 𝙉𝙤𝙩 𝙁𝙤𝙧 𝙔𝙤𝙪. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙍𝙚𝙦𝙪𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙊𝙬𝙣")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', '𝑱𝒐𝒊𝒏 𝑶𝒖𝒓 𝑼𝒑𝒅𝒂𝒕𝒆𝒔 𝑪𝒉𝒂𝒏𝒏𝒆𝒍 𝑻𝒐 𝑼𝒔𝒆 𝑻𝒉𝒊𝒔 𝑩𝒐𝒕!')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "Hi {user}\n Welcome to {chat}")

G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = bool(environ.get("BUTTON_LOCK", False))

GRP_LNK = environ.get('GRP_LNK', 'https://t.me/imoviesrobot_group')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/iMoviesRobot_channel')

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "300"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))

SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'iMoviesRobot_channel')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b><code>{file_name}</code>\n\n┏━━━━•❅•°•❈•°•❅•━━━━┓ ✰<b>𝐉𝐨𝐢𝐧 [ 𝙈𝙤𝙫𝙞𝙚𝙨 𝙂𝙧𝙤𝙪𝙥 ](https://t.me/imoviesrobot_group)</b> 👑✰ ┗━━━━•❅•°•❈•°•❅•━━━━┛\n\n⚠️ 𝐍𝐨𝐭𝐞: This message will be Auto-deleted after 5 minutes to avoid copyright issues.\n\n𝙁𝙤𝙧𝙬𝙖𝙧𝙙 𝙩𝙤 𝙨𝙤𝙢𝙚 𝙤𝙩𝙝𝙚𝙧 𝙘𝙝𝙖𝙩 𝙤𝙧 𝙎𝙖𝙫𝙚𝙙 𝙈𝙚𝙨𝙨𝙖𝙜𝙚𝙨")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

#log srt
LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"

MALIK = environ.get("malik", "https://telegra.ph/file/f732cee3ae72fb2c8fced.png")
MALIK5 = environ.get("malik5", "https://telegra.ph/file/5b0ae1ac84e1bd86abb44.png")

# Verify 2

SHORTENER_API = environ.get("SHORTENER_API", "iQ2iqO9EXFbcjek412Dg5j6stWu2")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "shareus.in")
SHORT_URL = is_enabled((environ.get('SHORT_URL', "True")), True)

SHORTENER_API = environ.get("SHORTENER_API", "1f5f1a40bec1bb6278f0fdbe8dd67bdb12690746")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "omegalinks.in")

SHORTENER_API2 = environ.get("SHORTENER_API2", "a0e3e2e5668f839515e6617a42a5392de102556f")
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "mdiskshortners.in")

VERIFY_SHORTNER = is_enabled((environ.get('VERIFY_SHORTNER', "True")), True)

# How to verify video link
TUTORIAL_LINK_2 = os.environ.get('TUTORIAL_LINK_2', 'https://t.me/+eXJ3IXhKJRU2MGM1')
TUTORIAL_LINK_1 = os.environ.get('TUTORIAL_LINK_1', 'https://t.me/+eXJ3IXhKJRU2MGM1')

# Verify 1
VERIFY_LOG = int(environ.get('VERIFY_LOG', '-1001958530115'))


VERIFY_1_SHORTENERS = environ.get("VERIFY_1_SHORTENERS", "")

VERIFY_1_SHORTENERS = [(data.split(",")[0].strip(), data.split(",")[1].strip()) for data in VERIFY_1_SHORTENERS.splitlines()]
VERIFY_1_SHORTENERS=[("ef2de8643c023800969e9fa388807c1c9ac5f42c", "bindaaslinks.com")] 


MQTTP = environ.get("MQTTP", "https://telegra.ph/file/67b8db0ce0338a7a109a0.png")


#stream link

DIRECT_GEN_DB = int(os.environ.get("DIRECT_GEN_DB", "-1001916834570"))
DIRECT_GEN_URL = os.environ.get("DIRECT_GEN_URL", "https://filexstreambot.onrender.com/") # https://example.com/
DIRECT_GEN = bool(DIRECT_GEN_DB and DIRECT_GEN_URL)

STREAM_URL = is_enabled((environ.get('STREAM_URL', "False")), False)
STREAM_API = environ.get("STREAM_API", "1f5f1a40bec1bb6278f0fdbe8dd67bdb12690746")
STREAM_SITE = environ.get("STREAM_SITE", "omegalinks.in")
STREAM_LONG = environ.get("STREAM_LONG", False)



INST = """ᴍᴏᴠɪᴇ ʀᴇǫᴜᴇsᴛ ғᴏʀᴍᴀᴛ 

ᴇxᴀᴍᴘʟᴇ : ᴀᴠᴇɴɢᴇʀs ᴏʀ ᴀᴠᴇɴɢᴇʀs 𝟸𝟶𝟷𝟸:

sᴇʀɪᴇs ʀᴇǫᴜᴇsᴛ ғᴏʀᴍᴀᴛ: 

ᴇxᴀᴍᴘʟᴇ : ʟᴏᴋɪ S01 E01 ᴏʀ ʟᴏᴋɪ S01 E10,  

ᴅᴏɴ'ᴛ ᴜsᴇ ' : ( ! , . / ) 

ᴘᴏᴡᴇʀᴇᴅ ʙʏ : - @iMoviesRobot"""




MQTT = """<b>⚠️ 𝐇𝐞𝐲, {}!..</b>

sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs ᴡᴇʀᴇ ꜰᴏᴜɴᴅ

ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ

ʀᴇᴀᴅ ɪɴsᴛʀᴜᴄᴛɪᴏɴs ꜰᴏʀ ʙᴇᴛᴛᴇʀ ʀᴇsᴜʟᴛs ☟ <b>ᴀɴᴅ ʀᴇǫᴜᴇsᴛ ᴀᴅᴍɪɴ</b>"""

# Link Shortener False

#VERIFY = bool(environ.get("VERIFY", False))

# verify True 

VERIFY_CLOSE = bool(environ.get("VERIFY_CLOSE", False))

VERIFY = bool(environ.get("VERIFY", True))




LONG_DROPLINK_URL = environ.get("LONG_DROPLINK_URL", False)

SHORTENER = is_enabled((environ.get('SHORTENER_API', "True")), True)

SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")


#SHORT_URL = environ.get("SHORT_URL", "tinyfy.in")
#SHORT_API = environ.get("SHORT_API", "20f32231c57b129284cf6e5bc0fe736d60b4fba0")


# Main link shortner 

SHORT_URL2 = environ.get("SHORT_URL2", "omegalinks.in")
SHORT_API2 = environ.get("SHORT_API2", "1f5f1a40bec1bb6278f0fdbe8dd67bdb12690746")


#languages 

LANGUAGES = ["tamil", "english", "hindi", "telugu", "malayalam", "kannada"]



