import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import HNDLR, bot, call_py
from MusicAndVideo.helpers.queues import QUEUE, add_to_queue, get_queue

AMBILFOTO = [
    "https://te.legra.ph/file/402c519808f75bd9b1803.jpg",
    "https://te.legra.ph/file/90e3b3aeb77e3e598d66d.jpg",
    "https://te.legra.ph/file/2a726c634dbc3b9e8f451.jpg",
    "https://te.legra.ph/file/466de30ee0f9383c8e09e.jpg",
    "https://te.legra.ph/file/430dcf25456f2bb38109f.jpg",
    "https://te.legra.ph/file/c74686f70a1b918060b8e.jpg",
    "https://te.legra.ph/file/a282c460a7f98aedbe956.jpg",
    "https://te.legra.ph/file/478f9fa85efb2740f2544.jpg",
    "https://te.legra.ph/file/cd5c96a3c7e8ae1913ef3.jpg",
    "https://te.legra.ph/file/1cc6513411578cafda022.jpg",
    "https://te.legra.ph/file/46fa55b49b85c084159ce.jpg",
]

IMAGE_THUMBNAIL = random.choice(AMBILFOTO)

# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(filters.command(["تشغيل"], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**بدور عليها اهو اصبر شويه 🤓.**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "الصوت", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/4ec06efa91ebcc10fef90.jpg",
                    caption=f"""
ضيفتها في قايمة الانتظار اهو متوجعش دماغي بق 👀 {pos}
الاسم: [{songname}]({link})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "اެݪصۅت", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/4ec06efa91ebcc10fef90.jpg",
                    caption=f"""
الحالة: شغال اهو ربنا يكفيني شرك 😂
الاسم: [{songname}]({link})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply(
                "-› ابعت اسم اغنيه وانا اشغلها متوجعش دماغي بق 🤓."
            )
        else:
            await m.delete()
            huehue = await m.reply("ببحث عن الاغنيه اهو اتهد بقا شويه 🤓.")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("مش عارف اجيبهالك ازاي بس ملقيتش حاجه بالاسم دا ابعت كدا اسم المغني كامل 😢")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "الصوت", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**ضيفتهالك في قايمة الانتظار اتهد بق شويه 🤓 {pos}
الاسم: [{songname}]({url})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "الصوت", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**الحالة: شغال اهو ربنا يكفيني شرك 😂
الاسم: [{songname}]({url})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["فيديو"], prefixes=f"{HNDLR}"))
async def vplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**بدورلك على فديو اهو اصبر شويه 🤓.**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "`Hanya 720, 480, 360 Diizinkan` \n`Sekarang Streaming masuk 720p`"
                    )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "الفيديو", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/4ec06efa91ebcc10fef90.jpg",
                    caption=f"""
**ضيفتها في قايمة الانتظار ريح بق 🤓{pos}
الاسم: [{songname}]({link})
ايدي الدردشة: {chat_id}
طلب الكائن دا:{m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "الفيديو", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/4ec06efa91ebcc10fef90.jpg",
                    caption=f"""
**الحالة:  شغال اهو ربنا يكفيني شرك 😂
الاسم: [{songname}]({link})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply(
                "**-› ابعت اسم فديو اشغلهولك ربنا يتوب علينا من الشغلانه دي 🤓.**"
            )
        else:
            await m.delete()
            huehue = await m.reply("**بدور عليه اهو اصبر شويه 🤓.")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit("**مش عارف اجيبهالك ازاي بس ملقيتش حاجه ابعت اسم المغني كامل كدا 🥺**")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "الفيديو", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**ضيفتها في قايمة التشغيل اهو ريح بق 🤓 {pos}
الاسم: [{songname}]({url})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "الفيديو", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**الحالة:شغال اهو ربنا يكفيني شرك 😂
الاسم: [{songname}]({url})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["اغاني"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**الاستخدام:** \n\n`{HNDLR}اغاني [بالايدي/بالمعرف]` \n`{HNDLR}اغاني [بالايدي/بالمعرف]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"  يتم البحث عن {limit} قام بتشغيلها في {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "الصوت", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "الصوت", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_photo(
                        photo="https://telegra.ph/file/4ec06efa91ebcc10fef90.jpg",
                        caption=f"""
**ضيفتها لقايمة الانتظار اهو ريح بق شويه 🤓 {chat}
الاسم: [{songname}]({link})
ايدي الدردشة: {chat_id}
طلب الكائن دا: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"➕ تم اضافة {lmt} اغاني في الانتظار\n• اكتب {HNDLR}الانتظار لروية قائمة الانتظار**"
            )
        except Exception as e:
            await hmm.edit(f"**ERROR** \n`{e}`")


@Client.on_message(filters.command(["الانتظار", "queue"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**شغال دلوقت 🤓:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**لغنيه اللي بعد دي 🤓:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**-›  الانتظار:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**مفيش حاجه شغاله يا اعمى 🤓.**")
