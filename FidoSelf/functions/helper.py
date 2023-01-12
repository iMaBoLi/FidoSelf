from FidoSelf import client
from traceback import format_exc
from telethon.types import Message
import asyncio
import time
import math

def progress(event, download=False, upload=False):
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(
        create_progress(
            event,
            start,
            end,
            newtime,
            download,
            upload,
         )
    )
    return callback

setattr(Message, "progress", progress)

async def create_progress(event, current, total, start, download=False, upload=False):
    if download:
        type = client.get_string("Progress_2")
    elif upload:
        type = client.get_string("Progress_3")
    else:
        type = "-----"
    now = time.time()
    diff = time.time() - start
    if round(diff % 7.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) * 1000
        strs = "".join("●" for i in range(math.floor(perc / 7)))
        text = client.get_string("Progress_1").format(type, strs, round(perc, 2), client.utils.convert_bytes(current), client.utils.convert_bytes(total), client.utils.convert_bytes(speed), client.utils.convert_time(eta))
        await event.edit(text)

async def getuserid(event, group=1):
    userid = None
    inputid = event.pattern_match.group(group)
    if inputid:
        try:
            gpeer =  await client.get_peer_id(eval(inputid))
            userid = gpeer
        except:
            userid = None
    elif event.reply_message:
        userid = event.reply_message.sender_id
    elif event.is_private:
        userid = event.chat_id
    return event

setattr(Message, "userid", getuserid)

def mention(info, coustom=None):
    if coustom:
        name = coustom
    else:
        name = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    if info.username:
        return f"[{name}](@{info.username})"
    return f"[{name}](tg://user?id={info.id})"

def mediatype(event):
    type = "Empty"
    if not event:
        return type
    elif event.photo:
        type = "Photo"
    elif event.video:
        if event.video_note:
            type = "VideoNote"
        elif event.gif or event.file.mime_type == "image/gif":
            type = "Gif"
        else:
            type = "Video"
    elif event.voice:
        type = "Voice"
    elif event.audio:
        type = "Music"
    elif event.sticker:
        if event.file.mime_type == "image/webp":
            type = "Sticker"
        elif event.file.mime_type == "application/x-tgsticker":
            type = "ASticker"
    elif event.document:
        type = "File"
    elif event.text:
        type = "Text"
    return type

setattr(Message, "mediatype", mediatype)

def convert_date(gy, gm, gd):
   g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
   if (gm > 2):
       gy2 = gy + 1
   else:
       gy2 = gy
   days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
   jy = -1595 + (33 * (days // 12053))
   days %= 12053
   jy += 4 * (days // 1461)
   days %= 1461
   if (days > 365):
       jy += (days - 1) // 365
       days = (days - 1) % 365
   if (days < 186):
       jm = 1 + (days // 31)
       jd = 1 + (days % 31)
   else:
      jm = 7 + ((days - 186) // 30)
      jd = 1 + ((days - 186) % 30)
   return [jy, jm, jd]
