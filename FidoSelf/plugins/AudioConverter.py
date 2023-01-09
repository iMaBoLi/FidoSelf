from FidoSelf import client
from telethon import types
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Music|Voice)$")
async def audioconverter(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Music", "Voice"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Music"] + " - " + medias["Voice"]
        rtype = medias[mtype]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    if mode == "Music" and mtype in ["Voice"]:
        newtime = time.time()
        file_name = event.reply_message.file.name or "---"
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
        voice = await event.reply_message.download_media(progress_callback=callback)
        newtime = time.time()
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up", file_name))
        await client.send_file(event.chat_id, voice, progress_callback=callback, voice_note=False)
        os.remove(voice)
    elif mode == "Voice" and mtype in ["Music"]:
        newtime = time.time()
        file_name = event.reply_message.file.name or "---"
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
        audio = await event.reply_message.download_media(progress_callback=callback)
        newtime = time.time()
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up", file_name))
        await client.send_file(event.chat_id, audio, progress_callback=callback, voice_note=True)
        os.remove(audio)
    else:
        medias = client.get_string("ReplyMedia")
        media = medias["Voice"] if mode == "Music" else medias["Music"]
        rtype = medias[mtype]
        await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    await event.delete()
