# @sahid_malik
from datetime import datetime
import string
import pytz
import os
import logging
import random
import asyncio
from Script import script, SECOND_VERIFY_COMPLETE_TEXT, SECOND_VERIFICATION_TEXT, MALIK7, MALIK2
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message 
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import VERIFY_CLOSE, VERIFY_LOG, GRP_LNK, CHNL_LNK, VERIFY, CHANNELS, MALIK5, MALIK, TUTORIAL_LINK_1, TUTORIAL_LINK_2, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, START_MESSAGE, FORCE_SUB_TEXT, SUPPORT_CHAT
from utils import direct_gen_handler, get_shortlink, get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client:Client, message):
    m = message
    user_id = m.from_user.id  
    if len(m.command) == 2 and m.command[1].startswith('notcopy'):
        user_id = int(m.command[1].split("_")[1])
        verify_id = m.command[1].split("_")[2]

        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("Invalid link... Link has already verified or has wrong hash.. Try Again")
            return

        ist_timezone = pytz.timezone('Asia/Kolkata')

        key = "second_time_verified" if await db.is_user_verified(user_id) else "last_verified"
        current_time = datetime.now(tz=ist_timezone)

        result = await db.update_notcopy_user(user_id, {key:current_time})

        await db.update_verify_id_info(user_id, verify_id, {"verified":True})

        text = f"""User ID : `{user_id}`
Username : {m.from_user.mention}
Time : {datetime.now(tz=ist_timezone).strftime('%Y-%m-%d %H:%M:%S')}
#New_Verified_User_complete"""
        txt = SECOND_VERIFY_COMPLETE_TEXT if key == "second_time_verified" else MALIK7
        await client.send_message(VERIFY_LOG, text)
        dmm = await m.reply_photo(
        photo=(MALIK5), 
        caption=(txt.format(message.from_user.mention)), 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ JOIN THIS CHANNEL ⬅️",url="http://t.me/IMoviesRobot_channel"),]]),parse_mode=enums.ParseMode.HTML)#"You are now verified for next 24 hours. Continue asking movies")
        return
        
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
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
                    InlineKeyboardButton('WATCH ANY ANIME 💮', url='https://t.me/IANIMEHUB'),
                    InlineKeyboardButton('MORE 🤖', url='https://t.me/BESTBOTSTG')
                  ],[
                    InlineKeyboardButton('HOW TO USE THIS BOT ⚙️', url='https://t.me/iMoviesRobot_channel/114')
                  ]]
	    
        await message.reply(START_MESSAGE.format(user=message.from_user.mention if message.from_user else message.chat.title, bot=temp.B_LINK), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)                    
        await asyncio.sleep(2) 
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(a=message.chat.title, b=message.chat.id, c=message.chat.username, d=total, f=temp.B_LINK, e="Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title, message.chat.username)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention, message.from_user.username, temp.U_NAME))
    if len(message.command) != 2:
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
                    InlineKeyboardButton('WATCH ANY ANIME 💮', url='https://t.me/IANIMEHUB'),
                    InlineKeyboardButton('MORE 🤖', url='https://t.me/BESTBOTSTG')
                  ],[
                    InlineKeyboardButton('HOW TO USE THIS BOT ⚙️', url='https://t.me/iMoviesRobot_channel/114')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=START_MESSAGE.format(user=message.from_user.mention, bot=temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🤖 Join Updates Channel", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton(" 🔄 Try Again", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton(" 🔄 Try Again", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text=FORCE_SUB_TEXT,
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.DEFAULT
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
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
                    InlineKeyboardButton('WATCH ANY ANIME 💮', url='https://t.me/IANIMEHUB'),
                    InlineKeyboardButton('MORE 🤖', url='https://t.me/BESTBOTSTG')
                  ],[
                    InlineKeyboardButton('HOW TO USE THIS BOT ⚙️', url='https://t.me/iMoviesRobot_channel/114')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=START_MESSAGE.format(user=message.from_user.mention, bot=temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    data = message.command[1]
    try:
        pre, grp_id, file_id = data.split('_', 2)
    except:
        file_id = data
        pre = ""
	    
    if VERIFY_CLOSE:
        user_id = m.from_user.id
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
Username : {m.from_user.mention}
Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#New_Verify_{num}_User"""
            await client.send_message(VERIFY_LOG, text)
            bin_text = SECOND_VERIFICATION_TEXT if is_second_shortener else MALIK2
            dmb = await m.reply_text(
                #photo=(MALIK), #caption=(MALIK2)),
                text=(bin_text.format(message.from_user.mention)),
                protect_content = True,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(300) 
            await dmb.delete()
            return
        		
    # batch files
    if data.startswith("allfiles"):    
        _, file_ids = data.split("_", 1)
        files = temp.BATCH_FILES.get(file_ids)

        if not files:
            await message.reply_text("⚠️ Batch file not found ⚠️")
            return

        for msg in files:
            title = msg.file_name
            size=get_size(msg.file_size)
            f_caption=msg.caption
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"

            try:
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.file_id,
                    caption=f_caption,
                    protect_content=False,
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.file_id,
                    caption=f_caption,
                    protect_content=False,
                    )
            except Exception as e:
                logger.warning(e, exc_info=True)
            await asyncio.sleep(1)
        return
    # end batch files
	
    elif data.startswith("Urllink"):
        chat_id = int(grp_id)
        user_name = message.from_user.mention 
        user = message.from_user.id
        files_ = await get_file_details(file_id)
        files = files_[0]        
        g = await get_shortlinks(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{user}_{file_id}")
        am = await client.send_message(chat_id=user,text=f"Hay {user_name}. Your file ready\n\n<b>▶️ File Name: <code>{replace_username(files.file_name)}</code> \n\n⌛️ Size: {get_size(files.file_size)}\n\n📂 File Link: {g}\n\n<i>Note: This message is deleted in 5 mins to avoid copyrights. Save the link to Somewhere else</i></b>", protect_content=True, reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                    ], [
                        InlineKeyboardButton("🔸 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 🔸", url="https://t.me/c"),
        
                    ]
                ]
            )
        )
        async def del_func():
            await asyncio.sleep(180)
            await am.delete()
        await asyncio.create_task(del_func())
        return        

	
    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(mention=message.from_user.mention, file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(mention=message.from_user.mention, file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    dm = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("𝙎𝙀𝙀 𝙈𝙊𝙍𝙀 𝙇𝙄𝙆𝙀 𝙏𝙃𝙀𝙎𝙀 🎬", url="https://t.me/iRecommendations")],[InlineKeyboardButton("𝙒𝘼𝙏𝘾𝙃 𝘼𝙉𝙄𝙈𝙀 💮", url="https://t.me/iAnimeHub")],[InlineKeyboardButton("👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}")],]),)
    await asyncio.sleep(300) 
    await dm.delete()

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


@Client.on_message(filters.command('settings')) #& filters.user(ADMINS))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    '𝐅𝐈𝐋𝐓𝐄𝐑 𝐁𝐔𝐓𝐓𝐎𝐍',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '𝐒𝐈𝐍𝐆𝐋𝐄' if settings["button"] else '𝐃𝐎𝐔𝐁𝐋𝐄',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    '𝐁𝐎𝐓 𝐏𝐌',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝐘𝐄𝐒' if settings["botpm"] else '🗑️ 𝐍𝐎',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    '𝐅𝐈𝐋𝐄 𝐒𝐄𝐂𝐔𝐑𝐄',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝐘𝐄𝐒' if settings["file_secure"] else '🗑️ 𝐍𝐎',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    '𝐈𝐌𝐃𝐁',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝐘𝐄𝐒' if settings["imdb"] else '🗑️ 𝐍𝐎',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    '𝐒𝐏𝐄𝐋𝐋 𝐂𝐇𝐄𝐂𝐊',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝐘𝐄𝐒' if settings["spell_check"] else '🗑️ 𝐍𝐎',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    '𝐖𝐄𝐋𝐂𝐎𝐌𝐄',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝐘𝐄𝐒' if settings["welcome"] else '🗑️ 𝐍𝐎',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=f"<b>Change Your Settings for {title} As Your Wish ⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )



@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("Checking template")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("No Input!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"Successfully changed template for {title} to\n\n{template}")


@Client.on_message(filters.command("usend") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text
        command = ["/usend"]
        for cmd in command:
            if cmd in target_id:
                target_id = target_id.replace(cmd, "")
        success = False
        try:
            user = await bot.get_users(int(target_id))
            await message.reply_to_message.copy(int(user.id))
            success = True
        except Exception as e:
            await message.reply_text(f"<b>Eʀʀᴏʀ :- <code>{e}</code></b>")
        if success:
            await message.reply_text(f"<b>Yᴏᴜʀ Mᴇssᴀɢᴇ Hᴀs Bᴇᴇɴ Sᴜᴄᴇssғᴜʟʟʏ Sᴇɴᴅ To {user.mention}.</b>")
        else:
            await message.reply_text("<b>Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ !</b>")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_message(filters.command("gsend") & filters.user(ADMINS))
async def send_chatmsg(bot, message):
    if message.reply_to_message:
        target_id = message.text
        command = ["/gsend"]
        for cmd in command:
            if cmd in target_id:
                target_id = target_id.replace(cmd, "")
        success = False
        try:
            chat = await bot.get_chat(int(target_id))
            await message.reply_to_message.copy(int(chat.id))
            success = True
        except Exception as e:
            await message.reply_text(f"<b>Eʀʀᴏʀ :- <code>{e}</code></b>")
        if success:
            await message.reply_text(f"<b>Yᴏᴜʀ Mᴇssᴀɢᴇ Hᴀs Bᴇᴇɴ Sᴜᴄᴇssғᴜʟʟʏ Sᴇɴᴅ To {chat.id}.</b>")
        else:
            await message.reply_text("<b>Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ !</b>")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command won't work in groups. It only works on my PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    btn = [[
       InlineKeyboardButton("Yes, Continue !", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("No, Abort operation !", callback_data="close_data")
    ]]
    await message.reply_text(
        text="<b>Are you sure? Do you want to continue?\n\nNote:- This could be a destructive action !</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )




