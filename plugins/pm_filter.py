import asyncio, re, ast, math, logging
import datetime
import time
import string
import random
lock = asyncio.Lock()
from datetime import datetime
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script, INST, M_NT_FND, SECOND_VERIFICATION_TEXT, MALIK2, MQTTTM
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from info import VERIFY_CLOSE, LANGUAGES, VERIFY_LOG, SHORT_URL, SHORT_API, MQTTP, MQTT, INST, ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, SINGLE_BUTTON, PROTECT_CONTENT, \
    SPELL_CHECK_REPLY, IMDB_TEMPLATE, IMDB_DELET_TIME, START_MESSAGE, VERIFY, G_FILTER, BUTTON_LOCK, BUTTON_LOCK_TEXT, TUTORIAL_LINK_1, TUTORIAL_LINK_2, LOG_CHANNEL, GRP_LNK, CHNL_LNK
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import shortlink, direct_gen_handler, get_shortlink, get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import del_all, find_filter, get_filters
from database.gfilters_mdb import find_gfilter, get_gfilters
from plugins.helper.admin_check import admin_fliter

from image.edit_1 import bright, mix, black_white, g_blur, normal_blur, box_blur
from image.edit_2 import circle_with_bg, circle_without_bg, sticker, edge_curved, contrast, sepia_mode, pencil, cartoon                             
from image.edit_3 import green_border, blue_border, black_border, red_border
from image.edit_4 import rotate_90, rotate_180, rotate_270, inverted, round_sticker, removebg_white, removebg_plain, removebg_sticker
from image.edit_5 import normalglitch_1, normalglitch_2, normalglitch_3, normalglitch_4, normalglitch_5, scanlineglitch_1, scanlineglitch_2, scanlineglitch_3, scanlineglitch_4, scanlineglitch_5

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

PM_BUTTONS = {}
BUTTONS = {}
SPELL_CHECK = {}
PM_SPELL_CHECK = {}
FILTER_MODE = {}
G_MODE = {}
USER_SPELL_CHECK = {}


@Client.on_message(filters.command('autofilter') & filters.group & admin_fliter)
async def fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**𝙸𝙽𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴 𝙲𝙾𝙼𝙼𝙰𝙽𝙳...**")
      
      m = await message.reply("**𝚂𝙴𝚃𝚃𝙸𝙽𝙶.../**")

      if args in mode_on:
          FILTER_MODE[str(message.chat.id)] = "True" 
          await m.edit("**𝙰𝚄𝚃𝙾𝙵𝙸𝙻𝚃𝙴𝚁 𝙴𝙽𝙰𝙱𝙻𝙴𝙳**")
      
      elif args in mode_of:
          FILTER_MODE[str(message.chat.id)] = "False"
          await m.edit("**𝙰𝚄𝚃𝙾𝙵𝙸𝙻𝚃𝙴𝚁 𝙳𝙸𝚂𝙰𝙱𝙻𝙴𝙳**")
      else:
          await m.edit("𝚄𝚂𝙴 :- /autofilter on 𝙾𝚁 /autofilter off")


@Client.on_message(filters.command('g_filter') & filters.group & admin_fliter)
async def g_fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**𝙸𝙽𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴 𝙲𝙾𝙼𝙼𝙰𝙽𝙳...**")
      
      m = await message.reply("**𝚂𝙴𝚃𝚃𝙸𝙽𝙶.../**")

      if args in mode_on:
          G_MODE[str(message.chat.id)] = "True" 
          await m.edit("**𝙶𝙻𝙾𝙱𝙰𝙻 𝙴𝙽𝙰𝙱𝙻𝙴𝙳**")
      
      elif args in mode_of:
          G_MODE[str(message.chat.id)] = "False"
          await m.edit("**𝙶𝙻𝙾𝙱𝙰𝙻 𝙳𝙸𝚂𝙰𝙱𝙻𝙴𝙳**")
      else:
          await m.edit("𝚄𝚂𝙴 :- /g_filter on 𝙾𝚁 /g_filter off")


@Client.on_message(filters.private & filters.text & filters.chat(AUTH_USERS) if AUTH_USERS else filters.text & filters.private)
async def pm_filter(client, message):
    if VERIFY_CLOSE:
        if G_FILTER:

            user_id = message.from_user.id
    
            user_verified = await db.is_user_verified(user_id)

            is_second_shortener = await db.use_second_shortener(user_id)

            how_to_download_link = TUTORIAL_LINK_2 if is_second_shortener else TUTORIAL_LINK_1

            if not user_verified or is_second_shortener:
                verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
                await db.create_verify_id(user_id, verify_id)
                buttons = [[InlineKeyboardButton(text="🔹 Click here to Verify 🔹", url=await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}", is_second_shortener, verify_1=not is_second_shortener),),], [InlineKeyboardButton(text="🌀 How to verify 🌀", url=how_to_download_link)]]
                reply_markup=InlineKeyboardMarkup(buttons)
                num = 2 if is_second_shortener else 1
                text = f"""User ID : `{user_id}`

Username : {message.from_user.mention}
Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#New_Verify_{num}_User"""
                await client.send_message(VERIFY_LOG, text)
                bin_text = SECOND_VERIFICATION_TEXT if is_second_shortener else MALIK2
                dmb = await message.reply_text(
                   #photo=(MALIK), #caption=(MALIK2)),
                    text=(bin_text.format(message.from_user.mention)),
                    protect_content = True,
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                await asyncio.sleep(120) 
                await dmb.delete()
                return

            kd = await global_filters(client, message)
            if kd == False:
                await pm_AutoFilter(client, message)
        else:
            await pm_AutoFilter(client, message)
    else:
        await pm_AutoFilter(client, message)   

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    if G_FILTER:
        if G_MODE.get(str(message.chat.id)) == "False":
            return 
        else:

            kd = await global_filters(client, message)
        if kd == False:          
            k = await manual_filters(client, message)
            if k == False:
                if FILTER_MODE.get(str(message.chat.id)) == "False":
                    return
                else:
                    await auto_filter(client, message)   
    else:
        k = await manual_filters(client, message)
        if k == False:
            if FILTER_MODE.get(str(message.chat.id)) == "False":
                return
            else:
                await auto_filter(client, message)   

@Client.on_callback_query(filters.regex(r"^pmnext"))
async def pm_next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    try:
        offset = int(offset)
    except:
        offset = 0
    search = PM_BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    
    
    if VERIFY:          
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'pmfile#{file.file_id}')] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", callback_data=f'pmfile#{file.file_id}'),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'pmfile#{file.file_id}')] for file in files ]
    else:
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=await shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}"))] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", url=await shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}")),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", url=await shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}"))] for file in files ]
        
    if 0 < offset <= temp.multi_buttons:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - temp.multi_buttons
    batch_ids = files
    message = query.message
    temp.BATCH_FILES[f"{message.chat.id}-{message.id}"] = batch_ids
    batch_link = f"batchfiles#{message.chat.id}#{message.id}#{query.from_user.id}"
    
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"pmnext_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / temp.multi_buttons) + 1} / {math.ceil(total / temp.multi_buttons)}", callback_data="pages")]                                  
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / temp.multi_buttons) + 1} / {math.ceil(total / temp.multi_buttons)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"pmnext_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"pmnext_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / temp.multi_buttons) + 1} / {math.ceil(total / temp.multi_buttons)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"pmnext_{req}_{key}_{n_offset}")
            ],
        )

    if VERIFY:
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("Languages", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    else:
        btn.insert(0, [
            InlineKeyboardButton("⚡How to Download⚡", url="https://t.me/+yVQla9ALufU1ZWJl")
        ]) 
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("Languages", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )

    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("😁 𝗛𝗲𝘆 𝗙𝗿𝗶𝗲𝗻𝗱,𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿𝘀𝗲𝗹𝗳. /n/n😁हेलो दोस्त, कृपया खुद से सर्च करें!!!", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    chat_id = query.message.chat.id
    if VERIFY:        
        if settings["button"]:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Files_{chat_id}_{file.file_id}')
                ])	
		
                #btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}')] for file in files ]
        else:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Files_{chat_id}_{file.file_id}')
                ])	
    else:        
        if settings["button"]:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Urllink_{chat_id}_{file.file_id}')
                ])	
        else:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Urllink_{chat_id}_{file.file_id}')
                ])	
    if 0 < offset <= temp.multi_buttons:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - temp.multi_buttons
    batch_ids = files
    message = query.message
    temp.BATCH_FILES[f"{message.chat.id}-{message.id}"] = batch_ids
    batch_link = f"batchfiles#{message.chat.id}#{message.id}#{query.from_user.id}"
    
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / temp.multi_buttons) + 1} / {math.ceil(total / temp.multi_buttons)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / temp.multi_buttons) + 1} / {math.ceil(total / temp.multi_buttons)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / temp.multi_buttons) + 1} / {math.ceil(total / temp.multi_buttons)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    if VERIFY:
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("Languages", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    else:
        btn.insert(0, [
            InlineKeyboardButton("⚡How to Download⚡", url="https://t.me/+yVQla9ALufU1ZWJl")
        ]) 
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("Languages", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )

    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(f"😁 𝗛𝗲𝘆 𝗙𝗿𝗶𝗲𝗻𝗱,𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿𝘀𝗲𝗹𝗳....\n\n😁हेलो दोस्त, कृपया खुद से सर्च करें!!!", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            k = await auto_filter(bot, query, k)
        else:
            k = await query.message.edit( 
               text = (M_NT_FND),
               reply_markup=InlineKeyboardMarkup(
                                      [[
                                        InlineKeyboardButton('💢 Request to admin 💢', url="https://t.me/RequestiMoviesBot"),

                                      ]]
               ),
               parse_mode=enums.ParseMode.HTML
)
            await asyncio.sleep(90)
            await k.delete()


@Client.on_callback_query(filters.regex(r"^pmspolling"))
async def pm_spoll_tester(bot, query):
    _, user, movie_ = query.data.split('#')
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = PM_SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
    if files:
        k = (movie, files, offset, total_results)
        await pm_AutoFilter(bot, query, k)
    else:
        k = await query.message.edit('This Movie Not Found In DataBase')
        await asyncio.sleep(10)
        await k.delete()

 #languages

@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):
    if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )

    _, key = query.data.split("#")
    btn = [
        [
            InlineKeyboardButton(
                text=lang.title(),
                callback_data=f"fl#{lang.lower()}#{key}"
                ),
        ]
        for lang in LANGUAGES
    ]
    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="Select your languages", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="Back to files", callback_data=f"next_{req}_{key}_{offset}")])
    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))
        
@Client.on_callback_query(filters.regex(r"^fl#"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key = query.data.split("#")

    search = BUTTONS.get(key)

    if not search:
        await query.answer("You are clicking on an old button which is expired.", show_alert=True)
        return

    print(search)
    search = search.replace("_", " ")
    req = query.from_user.id

    if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )

    
    files, _, _ = await get_search_results(f"{search} {lang}", max_results=10) 
    files = [file for file in files if re.search(lang, file.file_name, re.IGNORECASE)]
    if not files:
        await query.answer("No files were found", show_alert=1)
        return
    nxreq  = query.from_user.id if query.from_user else 0
    chat_id = query.message.chat.id 
    settings = await get_settings(query.message.chat.id)
    if VERIFY:
        if settings["button"]:	    
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Files_{chat_id}_{file.file_id}')
                ])	
		
                #btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}')] for file in files ]
        else:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Files_{chat_id}_{file.file_id}')
                ])	
    else:        
        if settings["button"]:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Urllink_{chat_id}_{file.file_id}')
                ])	
        else:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Urllink_{chat_id}_{file.file_id}')
                ])	
    offset = 0
    if VERIFY:
        batch_ids = files
        message = query.message
        temp.BATCH_FILES[f"{message.chat.id}-{message.id}"] = batch_ids
        batch_link = f"batchfiles#{message.chat.id}#{message.id}#{query.from_user.id}"         
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    else:
        btn.insert(0, [
             InlineKeyboardButton("⚡How to Download⚡", url="https://t.me/cinemica/71")
        ]) 
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("Languages", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    btn.append(        [
            InlineKeyboardButton(
                text="Back to files",
                callback_data=f"next_{req}_{key}_{offset}"
                ),
        ])
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))

#languages 

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return
        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Buddy Don't Touch Other's Property 😁", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "𝙲𝙾𝙽𝙽𝙴𝙲𝚃"
            cb = "connectcb"
        else:
            stat = "𝙳𝙸𝚂𝙲𝙾𝙽𝙽𝙴𝙲𝚃"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("𝙳𝙴𝙻𝙴𝚃𝙴", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("𝙱𝙰𝙲𝙺", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"𝙶𝚁𝙾𝚄𝙿 𝙽𝙰𝙼𝙴 :- **{title}**\n𝙶𝚁𝙾𝚄𝙿 𝙸𝙳 :- `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))
        
        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN,
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)

    if query.data.startswith("pmfile"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)                                                                                                      
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return            
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "pmfilep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
	                                "𝙎𝙀𝙀 𝙈𝙊𝙍𝙀 𝙇𝙄𝙆𝙀 𝙏𝙃𝙀𝙎𝙀 🎬", url="https://t.me/iRecommendations"
		                        )
	                        ],
	                        [
                                InlineKeyboardButton(
	                                "𝙒𝘼𝙏𝘾𝙃 𝘼𝙉𝙄𝙈𝙀 💮", url="https://t.me/iAnimeHub"
		                        )
	                        ],
	                        [			
                                InlineKeyboardButton(
                                    "👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"
                                )
                            ],
                        ]
                    ),
                )
                                       
        except Exception as e:
            await query.answer(f"⚠️ Error {e}", show_alert=True)
        
    if query.data.startswith("file"):
        ident, req, file_id = query.data.split("#")
        if BUTTON_LOCK:
            if int(req) not in [query.from_user.id, 0]:
                return await query.answer(BUTTON_LOCK_TEXT.format(query=query.from_user.first_name), show_alert=True)             
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)                               
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                dm = await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False,
                    reply_markup=InlineKeyboardMarkup(
                         [
                             [
                                InlineKeyboardButton(
                                    "👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"
                                )
                             ],
                         ]
                    ),
                )
                stream, download = await direct_gen_handler(dm)
                if stream and download:
                    await dm.edit_reply_markup(
                        InlineKeyboardMarkup(
                            [                     
                                [
                                    InlineKeyboardButton(
                                        "⚡️ 𝙁𝙖𝙨𝙩 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙", url=download
                                    ),
                                    InlineKeyboardButton(
                                        "🖥 𝙒𝙖𝙩𝙘𝙝 𝙤𝙣𝙡𝙞𝙣𝙚", url=stream
                                    ),
                                ],
                                [
                                    InlineKeyboardButton(
                                        "👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"
                                    )
                                ],   
                            ] 
                        )
                    )
                
                await query.answer('Check PM, I have sent files in pm', show_alert=True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart Okay", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
               f_caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)  
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        dm = await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False,
            reply_markup=InlineKeyboardMarkup(
                 [
                     [
                        InlineKeyboardButton(
                            "👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"
                        )
                     ],
                 ]
            ),
        )
        stream, download = await direct_gen_handler(dm)
        if stream and download:
            await dm.edit_reply_markup(
                InlineKeyboardMarkup(
                    [                     
                        [
                            InlineKeyboardButton(
                                "⚡️ 𝙁𝙖𝙨𝙩 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙", url=download
                            ),
                            InlineKeyboardButton(
                                "🖥 𝙒𝙖𝙩𝙘𝙝 𝙤𝙣𝙡𝙞𝙣𝙚", url=stream
                            ),
                        ],
                    [
                            InlineKeyboardButton(
                               "👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"
                            )
                        ],   
                    ] 
                )
            )
    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)

    elif query.data == "minfo":
        await query.answer(text=script.MINFO, show_alert=True)

    elif query.data == "sinfo":
        await query.answer(text=script.SINFO, show_alert=True)


    elif query.data == "removebg":
        await query.message.edit_text(
            "**Select required mode**ㅤㅤㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton(text="𝖶𝗂𝗍𝗁 𝖶𝗁𝗂𝗍𝖾 𝖡𝖦", callback_data="rmbgwhite"),
                InlineKeyboardButton(text="𝖶𝗂𝗍𝗁𝗈𝗎𝗍 𝖡𝖦", callback_data="rmbgplain"),
                ],[
                InlineKeyboardButton(text="𝖲𝗍𝗂𝖼𝗄𝖾𝗋", callback_data="rmbgsticker"),
                ],[
                InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')
             ]]
        ),)
    elif query.data == "stick":
        await query.message.edit(
            "**Select a Type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖭𝗈𝗋𝗆𝖺𝗅", callback_data="stkr"),
                        InlineKeyboardButton(
                            text="𝖤𝖽𝗀𝖾 𝖢𝗎𝗋𝗏𝖾𝖽", callback_data="cur_ved"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="𝖢𝗂𝗋𝖼𝗅𝖾", callback_data="circle_sticker"
                        )
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')
                    ],
                ]
            ),
        )
    elif query.data == "rotate":
        await query.message.edit_text(
            "**Select the Degree**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="180", callback_data="180"),
                        InlineKeyboardButton(text="90", callback_data="90"),
                    ],
                    [InlineKeyboardButton(text="270", callback_data="270")],
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')
                ]
            ),
        )
    elif query.data == "glitch":
        await query.message.edit_text(
            "**Select required mode**ㅤㅤㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝖭𝗈𝗋𝗆𝖺𝗅", callback_data="normalglitch"
                        ),
                        InlineKeyboardButton(
                            text="𝖲𝖼𝖺𝗇 𝖫𝖺𝗂𝗇𝗌", callback_data="scanlineglitch"
                        ),
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')
                    ]
                ]
            ),
        )
    elif query.data == "normalglitch":
        await query.message.edit_text(
            "**Select Glitch power level**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data="normalglitch1"),
                        InlineKeyboardButton(text="2", callback_data="normalglitch2"),
                        InlineKeyboardButton(text="3", callback_data="normalglitch3"),
                    ],
                    [
                        InlineKeyboardButton(text="4", callback_data="normalglitch4"),
                        InlineKeyboardButton(text="5", callback_data="normalglitch5"),
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='glitch')
                    ],
                ]
            ),
        )
    elif query.data == "scanlineglitch":
        await query.message.edit_text(
            "**Select Glitch power level**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data="scanlineglitch1"),
                        InlineKeyboardButton(text="2", callback_data="scanlineglitch2"),
                        InlineKeyboardButton(text="3", callback_data="scanlineglitch3"),
                    ],
                    [
                        InlineKeyboardButton(text="4", callback_data="scanlineglitch4"),
                        InlineKeyboardButton(text="5", callback_data="scanlineglitch5"),
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='glitch')
                    ],
                ]
            ),
        )
    elif query.data == "blur":
        await query.message.edit(
            "**Select a Type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖡𝗈𝗑", callback_data="box"),
                        InlineKeyboardButton(text="𝖭𝗈𝗋𝗆𝖺𝗅", callback_data="normal"),
                    ],
                    [InlineKeyboardButton(text="𝖦𝖺𝗎𝗌𝗌𝗂𝖺𝗇", callback_data="gas")],
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')
                ]
            ),
        )
    elif query.data == "circle":
        await query.message.edit_text(
            "**Select required mode**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖶𝗂𝗍𝗁 𝖡𝖦", callback_data="circlewithbg"),
                        InlineKeyboardButton(text="𝖶𝗂𝗍𝗁𝗈𝗎𝗍 𝖡𝖦", callback_data="circlewithoutbg"),
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')
                    ]
                ]
            ),
        )
    elif query.data == "border":
        await query.message.edit(
            "**Select Border**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖱𝖾𝖽", callback_data="red"),
                        InlineKeyboardButton(text="𝖦𝗋𝖾𝖾𝗇", callback_data="green"),
                    ],
                    [
                        InlineKeyboardButton(text="𝖡𝗅𝖺𝖼𝗄", callback_data="black"),
                        InlineKeyboardButton(text="𝖡𝗅𝗎𝖾", callback_data="blue"),
                    ],
                    [
                        InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='photo')   
                    ],
                ]
            ),
        )
    elif query.data == "bright":
        await bright(client, query.message)
    elif query.data == "mix":
        await mix(client, query.message)
    elif query.data == "b|w":
        await black_white(client, query.message)
    elif query.data == "circlewithbg":
        await circle_with_bg(client, query.message)
    elif query.data == "circlewithoutbg":
        await circle_without_bg(client, query.message)
    elif query.data == "green":
        await green_border(client, query.message)
    elif query.data == "blue":
        await blue_border(client, query.message)
    elif query.data == "red":
        await red_border(client, query.message)
    elif query.data == "black":
        await black_border(client, query.message)
    elif query.data == "circle_sticker":
        await round_sticker(client, query.message)
    elif query.data == "inverted":
        await inverted(client, query.message)
    elif query.data == "stkr":
        await sticker(client, query.message)
    elif query.data == "cur_ved":
        await edge_curved(client, query.message)
    elif query.data == "90":
        await rotate_90(client, query.message)
    elif query.data == "180":
        await rotate_180(client, query.message)
    elif query.data == "270":
        await rotate_270(client, query.message)
    elif query.data == "contrast":
        await contrast(client, query.message)
    elif query.data == "box":
        await box_blur(client, query.message)
    elif query.data == "gas":
        await g_blur(client, query.message)
    elif query.data == "normal":
        await normal_blur(client, query.message)
    elif query.data == "sepia":
        await sepia_mode(client, query.message)
    elif query.data == "pencil":
        await pencil(client, query.message)
    elif query.data == "cartoon":
        await cartoon(client, query.message)
    elif query.data == "normalglitch1":
        await normalglitch_1(client, query.message)
    elif query.data == "normalglitch2":
        await normalglitch_2(client, query.message)
    elif query.data == "normalglitch3":
        await normalglitch_3(client, query.message)
    elif query.data == "normalglitch4":
        await normalglitch_4(client, query.message)
    elif query.data == "normalglitch5":
        await normalglitch_5(client, query.message)
    elif query.data == "scanlineglitch1":
        await scanlineglitch_1(client, query.message)
    elif query.data == "scanlineglitch2":
        await scanlineglitch_2(client, query.message)
    elif query.data == "scanlineglitch3":
        await scanlineglitch_3(client, query.message)
    elif query.data == "scanlineglitch4":
        await scanlineglitch_4(client, query.message)
    elif query.data == "scanlineglitch5":
        await scanlineglitch_5(client, query.message)
    elif query.data == "rmbgwhite":
        await removebg_white(client, query.message)
    elif query.data == "rmbgplain":
        await removebg_plain(client, query.message)
    elif query.data == "rmbgsticker":
        await removebg_sticker(client, query.message)
    elif query.data == "pages":
        await query.answer("🤨 Curiosity is a little more, isn't it? 😁", show_alert=True)
    elif query.data == "start":                        
        buttons = [[
                    InlineKeyboardButton('ADD ME TO YOUR GROUP', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('CHANNEL', url=CHNL_LNK),
                    InlineKeyboardButton('GROUP', url=GRP_LNK)
                ],[
                    InlineKeyboardButton('REQUEST', url='https://t.me/RequestiMoviesBot'),
                    InlineKeyboardButton('SEARCH INLINE', switch_inline_query_current_chat='')
                ],[
                    InlineKeyboardButton('⚠️ JOIN OUR BACKUP CHANNEL ⚠️', url='https://t.me/IMoviesRobot_backup'),
                ],[
                    InlineKeyboardButton('HOW TO USE THIS BOT ⚙️', url='https://t.me/iMoviesRobot_channel/11')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=START_MESSAGE.format(user=query.from_user.mention, bot=temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "photo":
        buttons = [[
            InlineKeyboardButton(text="𝖡𝗋𝗂𝗀𝗍𝗁", callback_data="bright"),
            InlineKeyboardButton(text="𝖬𝗂𝗑𝖾𝖽", callback_data="mix"),
            InlineKeyboardButton(text="𝖡 & 𝖶", callback_data="b|w"),
            ],[
            InlineKeyboardButton(text="𝖢𝗂𝗋𝖼𝗅𝖾", callback_data="circle"),
            InlineKeyboardButton(text="𝖡𝗅𝗎𝗋", callback_data="blur"),
            InlineKeyboardButton(text="𝖡𝗈𝗋𝖽𝖾𝗋", callback_data="border"),
            ],[
            InlineKeyboardButton(text="𝖲𝗍𝗂𝖼𝗄𝖾𝗋", callback_data="stick"),
            InlineKeyboardButton(text="𝖱𝗈𝗍𝖺𝗍𝖾", callback_data="rotate"),
            InlineKeyboardButton(text="𝖢𝗈𝗇𝗍𝗋𝖺𝗌𝗍", callback_data="contrast"),
            ],[
            InlineKeyboardButton(text="𝖲𝖾𝗉𝗂𝖺", callback_data="sepia"),
            InlineKeyboardButton(text="𝖯𝖾𝗇𝖼𝗂𝗅", callback_data="pencil"),
            InlineKeyboardButton(text="𝖢𝖺𝗋𝗍𝗈𝗈𝗇", callback_data="cartoon"),
            ],[
            InlineKeyboardButton(text="𝖨𝗇𝗏𝖾𝗋𝗍", callback_data="inverted"),
            InlineKeyboardButton(text="𝖦𝗅𝗂𝗍𝖼𝗁", callback_data="glitch"),
            InlineKeyboardButton(text="𝖱𝖾𝗆𝗈𝗏𝖾 𝖡𝖦", callback_data="removebg")
            ],[
            InlineKeyboardButton(text="𝖢𝗅𝗈𝗌𝖾", callback_data="close_data")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )      
        await query.message.edit_text(        
            text="Select your required mode from below!",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('🔋 𝙴𝚇𝚃𝚁𝙰 𝙼𝙾𝙳𝚂 🔋', callback_data='extra'),            
            ],[
            InlineKeyboardButton('𝙼𝙰𝙽𝚄𝙴𝙻 𝙵𝙸𝙻𝚃𝙴𝚁', callback_data='manuelfilter'),
            InlineKeyboardButton('𝙰𝚄𝚃𝙾 𝙵𝙸𝙻𝚃𝙴𝚁', callback_data='autofilter'),
            InlineKeyboardButton('𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙸𝙾𝙽𝚂', callback_data='coct')
            ],[                       
            InlineKeyboardButton('𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙿𝙷', callback_data='tele'),
            InlineKeyboardButton('𝚂𝙷𝙰𝚁𝙴-𝚃𝙴𝚇𝚃', callback_data='sharetxt'),
            InlineKeyboardButton('𝙵𝙸𝙻𝙴-𝚂𝚃𝙾𝚁𝙴', callback_data='newdata')
            ],[           
            InlineKeyboardButton('𝙹𝚂𝙾𝙽𝙴', callback_data='son'),
            InlineKeyboardButton('𝚃𝚃𝚂', callback_data='ttss'),           
            InlineKeyboardButton('𝙿𝚄𝚁𝙶𝙴', callback_data='purges')
            ],[
            InlineKeyboardButton('𝙿𝙰𝚂𝚃𝙴', callback_data='pastes'),
            InlineKeyboardButton("𝙸𝙼𝙰𝙶𝙴", callback_data='image'),
            InlineKeyboardButton('𝙿𝙸𝙽𝙶', callback_data='pings')                                   
            ],[                               
            InlineKeyboardButton('𝙼𝚄𝚃𝙴', callback_data='restric'),
            InlineKeyboardButton('𝙺𝙸𝙲𝙺', callback_data='zombies'),
            InlineKeyboardButton('𝙿𝙸𝙽', callback_data='pin')
            ],[
            InlineKeyboardButton('𝙲𝙰𝚁𝙱𝙾𝙽', callback_data='carb'),
            InlineKeyboardButton('𝙵𝙾𝙽𝙳', callback_data='fond'),
            InlineKeyboardButton('𝚉𝙾𝙼𝙱𝙸𝙴', callback_data='zombies')
            ],[
            InlineKeyboardButton('🔮 𝚂𝚃𝙰𝚃𝚄𝚂 🔮', callback_data='stats')
            ],[
            InlineKeyboardButton('🚫 𝙲𝙻𝙾𝚂𝙴', callback_data='close_data'),
            InlineKeyboardButton('🏠 𝙷𝙾𝙼𝙴 🏠', callback_data='start')           
        ]] 
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(                     
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons= [[
            InlineKeyboardButton('❣️ 𝚂𝙾𝚄𝚁𝙲𝙴 𝙲𝙾𝙳𝙴 ❣️', callback_data='source')
            ],[
            InlineKeyboardButton('🏠 𝙷𝙾𝙼𝙴 🏠', callback_data='start'),
            InlineKeyboardButton('🔐 𝙲𝙻𝙾𝚂𝙴 🔐', callback_data='close_data')
        ]]  
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "restric":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.RESTRIC_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "image":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.IMAGE_TXT.format(temp.B_NAME),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )  
    elif query.data == "sharetxt":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SHARE_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      
    elif query.data == "zombies":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ZOMBIES_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )    
    elif query.data == "pin":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "son":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.JSON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "pastes":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PASTE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "inst":
        await query.answer(INST, show_alert=True)
        return
    elif query.data == "pings":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PINGS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "ttss":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.TTS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "purges":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PURGE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "tele":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.TELE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )             
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help'),
            InlineKeyboardButton('𝙱𝚄𝚃𝚃𝙾𝙽𝚂', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )    
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('⚙️ 𝙰𝙳𝙼𝙸𝙽 𝙾𝙽𝙻𝚈 ⚙️', callback_data='admin')
            ],[
            InlineKeyboardButton('🔙 𝙱𝙰𝙲𝙺', callback_data='help'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "inst":
        await query.answer(INST, show_alert=True)
        return
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('𝙶𝙻𝙾𝙱𝙰𝙻 𝙵𝙸𝙻𝚃𝙴𝚁', callback_data='gfill'),
            InlineKeyboardButton('𝚄𝚂𝙴𝚁 & 𝙲𝙷𝙰𝚃', callback_data='uschat')
            ],[
            InlineKeyboardButton('🔙 𝙱𝙰𝙲𝙺', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(text=script.ADMIN_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        else:
            await query.answer("You'r Not Authorizer ⚠️", show_alert=True)

    elif query.data == "gfill":
        buttons = [[            
            InlineKeyboardButton('🔙 𝙱𝙰𝙲𝙺', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(text=script.G_FIL_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        
    elif query.data == "uschat":
        buttons = [[            
            InlineKeyboardButton('🔙 𝙱𝙰𝙲𝙺', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(text=script.US_CHAT_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        
    elif query.data == "carb":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CARB_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      
    elif query.data == "fond":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FOND_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )  
    elif query.data == "owner_info":
            btn = [[
                    InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="start"),
                    InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ", url="t.me/akshatsg")
                  ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.OWNER_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )     
    elif query.data == "newdata":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FILE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help'),
            InlineKeyboardButton('𝚁𝙴𝙵𝚁𝙴𝚂𝙷', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('𝙱𝙰𝙲𝙺', callback_data='help'),
            InlineKeyboardButton('𝚁𝙴𝙵𝚁𝙴𝚂𝙷', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
      )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return 

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('𝐅𝐈𝐋𝐓𝐄𝐑 𝐁𝐔𝐓𝐓𝐎𝐍',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('𝐒𝐈𝐍𝐆𝐋𝐄' if settings["button"] else '𝐃𝐎𝐔𝐁𝐋𝐄',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('𝐁𝐎𝐓 𝐏𝐌', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ 𝐘𝐄𝐒' if settings["botpm"] else '🗑️ 𝐍𝐎',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('𝐅𝐈𝐋𝐄 𝐒𝐄𝐂𝐔𝐑𝐄',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ 𝐘𝐄𝐒' if settings["file_secure"] else '🗑️ 𝐍𝐎',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('𝐈𝐌𝐃𝐁', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ 𝐘𝐄𝐒' if settings["imdb"] else '🗑️ 𝐍𝐎',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('𝐒𝐏𝐄𝐋𝐋 𝐂𝐇𝐄𝐂𝐊',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ 𝐘𝐄𝐒' if settings["spell_check"] else '🗑️ 𝐍𝐎',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('𝐖𝐄𝐋𝐂𝐎𝐌𝐄', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ 𝐘𝐄𝐒' if settings["welcome"] else '🗑️ 𝐍𝐎',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("killfilesdq"):
        ident, keyword = query.data.split("#")
        await query.message.edit_text(f"<b>Fetching Files for your query {keyword} on DB... Please wait...</b>")
        files, total = await get_bad_files(keyword)
        await query.message.edit_text(f"<b>Found {total} files for your query {keyword} !\n\nFile deletion process will start in 5 seconds !</b>")
        await asyncio.sleep(5)
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if result.deleted_count:
                        logger.info(f'File Found for your query {keyword}! Successfully deleted {file_name} from database.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>Process started for deleting files from DB. Successfully deleted {str(deleted)} files from DB for your query {keyword} !\n\nPlease wait...</b>")
            except Exception as e:
                logger.exception(e)
                await query.message.edit_text(f'Error: {e}')
            else:
                await query.message.edit_text(f"<b>Process Completed for file deletion !\n\nSuccessfully deleted {str(deleted)} files from database for your query {keyword}.</b>")

    elif query.data.startswith("batchfiles"):
        ident, group_id, message_id, user = query.data.split("#")
        group_id = int(group_id)
        message_id = int(message_id)
        user = int(user)
        #if query.message.chat.type == enums.ChatType.PRIVATE:
            #return await query.answer('ᴛʜɪs ʙᴜᴛᴛᴏɴ ᴏɴʟʏ ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘ',show_alert=True)
        if user != query.from_user.id:
            await query.answer("Sorry You Cant Access This Batch Link",show_alert=True)
            return
        link = f"https://telegram.me/{temp.U_NAME}?start=allfiles_{group_id}-{message_id}"
        await query.answer(url=link)
        return

    await query.answer('Piracy Is Crime')




async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text.replace('movie', '').replace('gujarati', '').replace('webseries', '').replace('punjabi', '').replace('marathi', '').replace('english', '').replace('season', '').replace('web', '').replace('series', '').replace('movies', '').replace('episode', '').replace('Episodes', '').replace('dubb', '').replace('dubbed', '').replace('session', '').replace('good', '').replace('quality', '').replace('movie', '').replace('send', '').replace('link', '').replace('!', '').replace('(', '').replace(')', '').replace(':', '')
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    chat_id = msg.message.chat.id 
    req = message.from_user.id if message.from_user else 0
    if VERIFY:        
        if settings["button"]:	    
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Files_{chat_id}_{file.file_id}')
                ])	
		
                #btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}')] for file in files ]
        else:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Files_{chat_id}_{file.file_id}')
                ])	
    else:        
        if settings["button"]:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Urllink_{chat_id}_{file.file_id}')
                ])	
        else:
	    btn = []
	    for file in files:
                btn.append([
                    InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=f'https://telegram.dog/{temp.U_NAME}?start=Urllink_{chat_id}_{file.file_id}')
                ])	
    batch_ids = files
    temp.BATCH_FILES[f"{message.chat.id}-{message.id}"] = batch_ids
    batch_link = f"batchfiles#{message.chat.id}#{message.id}#{message.from_user.id}"            
                     
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"📄 𝗣𝗮𝗴𝗲 1/{math.ceil(int(total_results) / temp.multi_buttons)}", callback_data="pages"),
             InlineKeyboardButton(text="𝗡𝗲𝘅𝘁 ➡️", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="📄 𝗣𝗮𝗴𝗲 1/1", callback_data="pages")]
        )
    if VERIFY:
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link), 
                InlineKeyboardButton("ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    else:
        btn.insert(0, [
            InlineKeyboardButton("⚡How to Download⚡", url="https://t.me/+yVQla9ALufU1ZWJl")
        ]) 
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            group = message.chat.title,
            requested = message.from_user.mention,
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        cap = f"🏷 Tɪᴛʟᴇ :- {search}\n📣 Gʀᴏᴜᴘ :- {message.chat.title}\n✍️ Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :-{message.from_user.mention}💜💫"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await hehe.delete()            
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo="https://telegra.ph/file/9a86852df9e70951217cd.png", caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))           
            await asyncio.sleep(IMDB_DELET_TIME)
            await hmm.delete()            
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_photo(photo="https://telegra.ph/file/9a86852df9e70951217cd.png", caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await fek.delete()
    else:
        fuk = await message.reply_photo(photo="https://telegra.ph/file/9a86852df9e70951217cd.png", caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(IMDB_DELET_TIME)
        await fuk.delete()        
    if spoll:
        await msg.message.delete()


async def pm_AutoFilter(client, msg, pmspoll=False):
    if not pmspoll:
        message = msg   
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:               
                return await pm_spoll_choker(msg)              
        else:
            return 
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = pmspoll
    pre = 'pmfilep' if PROTECT_CONTENT else 'pmfile'
    if VERIFY:       
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}')] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", callback_data=f'{pre}#{req}#{file.file_id}'),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'{pre}#{file.file_id}')] for file in files ]    
    else:
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=await shortlink(f"https://telegram.dog/{temp.U_NAME}?start=pre_{file.file_id}"))] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", url=await shortlink(f"https://telegram.dog/{temp.U_NAME}?start=pre_{file.file_id}")),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", url=await shortlink(f"https://telegram.dog/{temp.U_NAME}?start=pre_{file.file_id}"))] for file in files ]
    batch_ids = files
    temp.BATCH_FILES[f"{message.chat.id}-{message.id}"] = batch_ids
    batch_link = f"batchfiles#{message.chat.id}#{message.id}#{message.from_user.id}"            
                     
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        PM_BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"📄 𝗣𝗮𝗴𝗲 1/{math.ceil(int(total_results) / temp.multi_buttons)}", callback_data="pages"),
            InlineKeyboardButton(text="𝗡𝗲𝘅𝘁 ➡️", callback_data=f"pmnext_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="📄 𝗣𝗮𝗴𝗲 1/1", callback_data="pages")]
        )
    if VERIFY:
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search        
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )
    else:
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        btn.insert(0, [
            InlineKeyboardButton("⚡How to Download⚡", url="https://t.me/+yVQla9ALufU1ZWJl")
        ]) 
        btn.insert(0, 
            [
                InlineKeyboardButton("📂 sᴇɴᴅ ᴀʟʟ", callback_data=batch_link),
                InlineKeyboardButton("ʟᴀɴɢᴜᴀɢᴇs", callback_data=f"languages#{key}"),
                InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'sinfo')
            ]
        )

    imdb = await get_poster(search) if IMDB else None
    TEMPLATE = IMDB_TEMPLATE
    if imdb:
        cap = TEMPLATE.format(
            group = message.chat.title,
            requested = message.from_user.mention,
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        cap = f"Here is what i found for your query {search}"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await hehe.delete()            
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo="https://telegra.ph/file/9a86852df9e70951217cd.png", caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))           
            await asyncio.sleep(IMDB_DELET_TIME)
            await hmm.delete()            
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_photo(photo="https://telegra.ph/file/9a86852df9e70951217cd.png", caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await fek.delete()
    else:
        fuk = await message.reply_photo(photo="https://telegra.ph/file/9a86852df9e70951217cd.png", caption=cap, quote=1, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(IMDB_DELET_TIME)
        await fuk.delete()        
    if pmspoll:
        await msg.message.delete()

async def pm_spoll_choker(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(90)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    PM_SPELL_CHECK[msg.id] = movielist
    btn = [[InlineKeyboardButton(text=movie.strip(), callback_data=f"pmspolling#{user}#{k}")] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'pmspolling#{user}#close_spellcheck')])
    await msg.reply("I couldn't find anything related to that\nDid you mean any one of these?", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)


async def advantage_spell_chok(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    malik = query.strip() + " movie"
    reply = malik.replace(" ", '+')
    reply_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton("ɪɴsᴛʀᴜᴄᴛɪᴏɴs", callback_data='inst'),
    InlineKeyboardButton("ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴀᴅᴍɪɴ", url="https://t.me/RequestiMoviesBot")
    ],[
    InlineKeyboardButton("🔍 ᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ sᴘɪʟʟɪɴɢ ✅", url=f"https://www.google.com/search?q={reply}+movie")
    ],[
    InlineKeyboardButton("🔍 ᴄʟɪᴄᴋ  ᴛᴏ ᴄʜᴇᴄᴋ ʀᴇʟᴇᴀsᴇ ᴅᴀᴛᴇ 📅", url=f"https://www.google.com/search?q={reply}+release+date")
    ]]  
    )    
    dl = await msg.reply_photo(
        photo=(MQTTP),
        caption=(MQTT.format(msg.from_user.mention, query)),
        reply_markup=reply_markup 
    ) 
    await asyncio.sleep(180)
    await dl.delete()

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True, reply_to_message_id=reply_id)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False


async def global_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            knd3 = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(IMDB_DELET_TIME)
                            await knd3.delete()
                            await message.delete()

                        else:
                            button = eval(btn)
                            knd2 = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(IMDB_DELET_TIME)
                            await knd2.delete()
                            await message.delete()

                    elif btn == "[]":
                        knd1 = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(IMDB_DELET_TIME)
                        await knd1.delete()
                        await message.delete()

                    else:
                        button = eval(btn)
                        knd = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(IMDB_DELET_TIME)
                        await knd.delete()
                        await message.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False





