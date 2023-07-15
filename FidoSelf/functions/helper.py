from FidoSelf import client
from traceback import format_exc
from telethon.types import Message
import asyncio
import time
import math
import random
import os

def progress(event, download=False, upload=False):
    newtime = time.time()
    callback = lambda current, total: client.loop.create_task(create_progress(event, current, total, newtime, download, upload))
    return callback

setattr(Message, "progress", progress)
setattr(client, "progress", progress)

async def fileprogress(event, file, total, download=False, upload=False):
    newtime = time.time()
    current = os.path.getsize(file) if os.path.exists(file) else 0
    while (total >= current):
        callback = await create_progress(event, current, total, newtime, download, upload)
        current = os.path.getsize(file)

setattr(Message, "fileprogress", fileprogress)
setattr(client, "fileprogress", fileprogress)

async def create_progress(event, current, total, start, download=False, upload=False):
    if download:
        type = client.STRINGS["progress"]["Down"]
    elif upload:
        type = client.STRINGS["progress"]["Up"]
    else:
        type = "-----"
    diff = time.time() - start
    if round(diff % 5.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) * 1000
        pstrs = "".join("■" for i in range(math.floor(perc / 5)))
        fstrs = "".join("□" for i in range(20-len(pstrs)))
        strs = pstrs + fstrs
        text = client.STRINGS["progress"]["Text"].format(type, strs, round(perc, 2), client.functions.convert_bytes(current), client.functions.convert_bytes(total), client.functions.convert_bytes(speed), client.functions.convert_time(eta))
        await event.edit(text)

async def getuserid(event, number=1):
    userid = 0
    inputs = event.text.split(" ")
    if len(inputs) > number:
        match = inputs[number]
        inputid = int(match) if match.isdigit() else str(match)
        try:
            userinfo = await client.get_entity(inputid)
            if userinfo.to_dict()["_"] == "User":
                userid = userinfo.id
        except:
            pass
    elif event.reply_message:
        userid = event.reply_message.sender_id
    elif event.is_private:
        userid = event.chat_id
    return int(userid)

async def getchatid(event, number=1):
    chatid = 0
    inputs = event.text.split(" ")
    if len(inputs) > number:
        match = inputs[number]
        inputid = int(match) if match.isdigit() else str(match)
        try:
            chatinfo = await client.get_entity(inputid)
            if chatinfo.to_dict()["_"] in ["Channel", "Group"]:
                chatid = chatinfo.id
        except:
            pass
    elif not event.is_private:
        chatid = event.chat_id
    return int(chatid)

def mention(info, coustom=None):
    if not coustom:
        coustom = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    return f"[{coustom}](tg://user?id={info.id})"

def mediatype(event):
    if not event or not event.file: return None
    if event.photo:
        filetype = "JPG Photo"
    elif event.video:
        if event.video_note:
            filetype = "VideoNote"
        elif event.gif or event.file.mime_type == "image/gif":
            filetype = "Gif"
        elif event.file.mime_type == "video/webm":
            filetype = "VSticker"
        else:
            filetype = "Video"
    elif event.voice:
        filetype = "Voice"
    elif event.audio:
        filetype = "Music"
    elif event.sticker:
        if event.file.mime_type == "image/webp":
            filetype = "Sticker"
        elif event.file.mime_type == "application/x-tgsticker":
            filetype = "ASticker"
    elif event.document:
        mimetype = event.file.mime_type
        TYPES = {
            "image/jpeg": "JPG Photo",
            "image/png": "PNG Photo",
            "font/ttf": "TTF File",
            "text/plain": "TXT File",
            "application/vnd.android.package-archive": "APP File",
        }
        filetype = TYPES[mimetype] if mimetype in TYPES else "File"
    return filetype

setattr(Message, "mediatype", mediatype)

async def save(event):
    if client.BACKUP:
        forward = await event.forward_to(client.BACKUP)
        info = {"chat_id": client.BACKUP, "msg_id": forward.id}
    else:
        forward = await event.forward_to(client.me.id)
        info = {"chat_id": client.me.id, "msg_id": forward.id}
    return info

setattr(Message, "save", save)

def AddInfo(info):
    plugcat = info["Category"]
    plugname = info["Name"]
    pluginfo = info["Info"]
    pluginfo.update({"Category": plugcat})
    client.HELP.update({plugname: pluginfo})

def create_font(newtime, timefont):
    newtime = str(newtime)
    if str(timefont) == "random2":
        for par in newtime:
            fonts = [1,3,4,5,6,7,8,9,10,11,12]
            rfont = random.choice(fonts)
            if par.isdigit():
                nfont = client.functions.FONTS[int(rfont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
            fonts.remove(rfont)
    else:
        if str(timefont) == "random":
            fonts = list(range(1, len(client.functions.FONTS)+2))
            timefont = random.choice(fonts)
        for par in newtime:
            if par.isdigit():
                nfont = client.functions.FONTS[int(timefont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
    return newtime