# This Repo was not fully owned by me. Some codes are scraped from respected DEVOLEPERS whom where mine friends. 
# check Readme.md For More. 

import logging
logger = logging.getLogger(__name__)
import os
import re
import time
import math
import json
import string
import random
import traceback
import wget
import asyncio
import datetime
import aiofiles
import aiofiles.os
import requests
import youtube_dl
import lyricsgenius
from config import Config
from random import choice 
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch
from database import Database
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid


Bot = Client(
    "Song Downloader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

db = Database()

START_TEXT = """ `Hai {}, 
I'm Cassy sᴏɴɢ ᴘʟᴀʏ ʙᴏᴛ 
  𝙸 𝚊𝚖 𝚊 𝚖𝚞𝚜𝚒𝚌 𝚋𝚘𝚝 𝚊𝚗𝚍 𝚢𝚝 𝚟𝚒𝚍𝚎𝚘 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚛 𝚋𝚘𝚝 𝙸 𝚊𝚖 𝚊 𝚙𝚞𝚋𝚕𝚒𝚌 𝚋𝚘𝚝 𝚢𝚘𝚞 𝚊𝚍𝚍 𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚐𝚛𝚘𝚞𝚙 𝚊𝚗𝚍 𝚖𝚊𝚔𝚎 𝚖𝚎 𝚊𝚗 𝚊𝚍𝚖𝚒𝚗 𝚊𝚗𝚍 𝙸 𝚠𝚒𝚕𝚕 𝚜𝚎𝚗𝚍 𝚖𝚞𝚜𝚒𝚌𝚜 𝚒𝚗 𝚢𝚘𝚞𝚛 𝚐𝚛𝚘𝚞𝚙 𝑀𝑎𝑑𝑒 𝑤𝑖𝑡ℎ ❤️ 𝐵𝑦 @Lallu_tg!"""

CMDS_TEXT = """
`Here It is The List of Commamds and Its usage.`
Click the buttons and know the cmds and usage
"""

SONG_TEXT = """
SONG MODULE
Song Download
Song Download Module, For Those Who Love Music

🎈 Command

• /song or /s (songname) - download song from yt servers.
• /video or /v (songname) - download video from yt servers(video mode now not working sorry)

Usage
- working pm and groups
"""

YT_TEXT = """
🎸YOUTUBE VIDEO🎸
you can also use inline for search YouTube video or song
"""

ABOUT_TEXT = """
- **𝐍𝐚𝐦𝐞 :** Cassy
- **Creator :** [ʟᴀʟʟᴜᵗᵍ](https://Github.com/lallu_tg)
- **Support :** [CLICK HERE](https://telegram.me/Annaben_support)
- **Source :** [CLICK HERE](https://github.com/Lallu-lallus/musicia_bot)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)

"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('😉SUPPORT😉', url=f"https://telegram.me/{Config.SUPPORT}"), 
        InlineKeyboardButton(text="🔎SEARCH🔍", switch_inline_query_current_chat="")
        ],[
        InlineKeyboardButton('➕ADD ME TO YOUR GROUP➕', url='http://t.me/Filevx_bot?startgroup=true') 
        ],[
        InlineKeyboardButton('HELPℹ️', callback_data='cmds'),
        InlineKeyboardButton('🤔ABOUT🤔', callback_data='about')
        ]]
    )
CMDS_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎸SONG', callback_data='song'),
        InlineKeyboardButton('🎶LYRICS', callback_data='lyric')
        ],[
        InlineKeyboardButton('🎥YT VIDEO', callback_data='yt')
        ],[
        InlineKeyboardButton('🏡HOME', callback_data='home'),
        InlineKeyboardButton('⚠️CLOSE', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏡HOME', callback_data='home'),
        InlineKeyboardButton('🚶‍♀️BACK', callback_data='cmds')
        ]]
    )
SONG_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏡HOME', callback_data='home'),
        InlineKeyboardButton('🚶‍♀️BACK', callback_data='cmds')
        ]]
    )
YT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🔎SEARCH🔍', switch_inline_query_current_chat="")
        ],[
        InlineKeyboardButton('🏡 HOME', callback_data='home'),
        InlineKeyboardButton('🚶‍♀️BACK', callback_data='cmds')
        ]]
    )
@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "cmds":
        await update.message.edit_text(
            text=CMDS_TEXT,
            reply_markup=CMDS_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "song":
        await update.message.edit_text(
            text=SONG_TEXT,
            reply_markup=SONG_BUTTONS,
            disable_web_page_preview=True
       )
    elif update.data == "yt":
        await update.message.edit_text(
            text=YT_TEXT,
            reply_markup=YT_BUTTONS,
            disable_web_page_preview=True
      )
    else:
        await update.message.delete()

        
@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)  

    await update.reply_photo(
        photo="https://telegra.ph/file/5649d8111f0a45039e282.jpg",
        caption=START_TEXT.format(update.from_user.mention),
	reply_markup=START_BUTTONS
    )

@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )

broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@Bot.on_message(filters.command(['song', 's']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐬𝐨𝐧𝐠.... 𝐩𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭𝐞.... 𝐈 𝐋𝐔𝐁 𝐘𝐎𝐔[🙂](https://telegra.ph/file/5649d8111f0a45039e282.jpg) `')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 7000:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[MAKRI'S SERVER]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**𝐇𝐞𝐲 𝐦𝐚𝐧𝐡 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐢𝐭 𝐬𝐨𝐫𝐫𝐲🤧🙂!**')
            return
    except Exception as e:
        m.edit(
            "**Enter The Song Name with /song OR /s command.!**"
        )
        print(str(e))
        return
    m.edit("`𝐀𝐦 𝐮𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚 𝐬𝐨𝐧𝐠 𝐟𝐨𝐫 𝐲𝐨𝐮.... 𝐈 𝐋𝐔𝐁 𝐘𝐎𝐔[🙂](https://telegra.ph/file/5649d8111f0a45039e282.jpg)`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'❍📖 <b>Title:</b> <a href="{link}">{title}</a>\n❍⌚ <b>Duration:</b> <code>{duration}</code>\n❍📤 <b>Uploaded By:</b> <a href="https://t.me/Music_wrld_grp">MUSIC WORLD😉</a>\n❍ <b>𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲:</b> {message.from_user.mention()}'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('**Something Went Wrong Report This at @LALLU_TG!!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
	

@Bot.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="Search your query here...🔎",
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        search = VideosSearch(search_query, limit=50)

        for result in search.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description="{}, {} views.".format(
                        result["duration"],
                        result["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "https://www.youtube.com/watch?v={}".format(
                            result["id"]
                        )
                    ),
                    thumb_url=result["thumbnails"][0]["url"]
                )
            )

        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out",
                switch_pm_parameter="",
            )
        
@Bot.on_message(filters.private & filters.command("broadcast") & filters.reply)
async def broadcast_(c, m):
    print("broadcasting......")
    if m.from_user.id not in Config.OWNER_ID:
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.message_id,
            revoke=True
        )
        return
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    
    out = await m.reply_text(
        text = f"Broadcast initiated! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    
    broadcast_ids[broadcast_id] = dict(
        total = total_users,
        current = done,
        failed = failed,
        success = success
    )
    
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            
            sts, msg = await send_msg(
                user_id = int(user['id']),
                message = broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            
            if sts == 200:
                success += 1
            else:
                failed += 1
            
            if sts == 400:
                await db.delete_user(user['id'])
            
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current = done,
                        failed = failed,
                        success = success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    
    await asyncio.sleep(3)
    
    await out.delete()
    
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    
    await aiofiles.os.remove('broadcast.txt')

@Bot.on_message(filters.command("lyrics"))
async def lrsearch(_, message: Message):  
    m = await message.reply_text("𝐀𝐌 𝐒𝐄𝐀𝐑𝐂𝐇𝐈𝐍𝐆 𝐋𝐘𝐑𝐈𝐂𝐒 𝐅𝐎𝐑 𝐘𝐎𝐔.....𝐈 𝐋𝐔𝐁 𝐘𝐎𝐔🙂")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("𝐇𝐞𝐲 𝐀𝐦 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝 𝐘𝐨𝐮𝐫 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐋𝐲𝐫𝐢𝐜𝐬....𝐈 𝐋𝐔𝐁 𝐘𝐎𝐔🙂.")
    xxx = f"""
**Lyrics Search Powered By Music Bot**
**Searched Song:-** __{query}__
**Found Lyrics For:-** __{S.title}__
**Artist:-** {S.artist}
**__Lyrics:__**
{S.lyrics}"""
    await m.edit(xxx)

@Client.on_message(filters.command(["video"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"**🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠..** `{urlissed}`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax Please Check help Menu To Know More!")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**Download Failed** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"""
**🏷️ Video:** [{thum}]({mo})
**🎬 Requested by:** {message.from_user.mention}
"""
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"**📥 Download** `{urlissed}`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
Bot.run()
