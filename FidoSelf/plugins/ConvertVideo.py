from FidoSelf import client
from telethon import types
import os

__INFO__ = {
    "Category": "Convert",
    "Name": "Convert Video",
    "Info": {
        "Help": "To Convert Video And Gif Formats!",
        "Commands": {
            "{CMD}ToVideo <Reply(VideoNote)>": None,
            "{CMD}ToVNote <Reply(Video)>": None,
            "{CMD}ToGif <Reply(Video)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "tovideo": "**{STR} The Video Note Converted To Video!**",
    "togif": "**{STR} The Video Converted To Gif!**"
}

@client.Command(command="ToVideo")
async def tovideo(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["VideoNote"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    videonote = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=False, supports_streaming=True)]
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, videonote, caption=client.getstrings(STRINGS)["tovideo"], attributes=attributes, progress_callback=callback)
    os.remove(videonote)
    await event.delete()

@client.Command(command="ToVNote")
async def tovnote(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Video"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=True)]
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
    os.remove(video)
    await event.delete()
    
@client.Command(command="ToGif")
async def togif(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Video", "VideoNote"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    giffile = client.PATH + "VideoGif.gif"
    os.rename(video, giffile)
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, giffile, caption=client.getstrings(STRINGS)["togif"], progress_callback=callback)
    os.remove(giffile)
    await event.delete()
