from FidoSelf import client
from telethon import types
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SV(Note|Normal)$")
async def videoshot(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    if not event.is_reply or not event.reply_message.video:
        return await event.edit(client.get_string("Reply_V"))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    video = await event.reply_message.download_media(progress_callback=callback)
    if mode == "Normal":
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=False, supports_streaming=True)]
    elif mode == "Note":
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=True)]
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up", file_name))
    await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
    os.remove(video)
    await event.delete()
