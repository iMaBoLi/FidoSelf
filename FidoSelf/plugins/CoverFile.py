from FidoSelf import client
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Cover File",
    "Info": {
        "Help": "To Setting Cover Photo Of Files!",
        "Commands": {
            "{CMD}SetCover": {
                "Help": "To Set Cover Photo",
                "Reply": ["Photo"],
            },
            "{CMD}AddCover":  {
                "Help": "To Add Cover To Files",
                "Reply": ["File", "Music"],
            },
            "{CMD}GetCover":  {
                "Help": "To Get Cover Of File",
                "Reply": ["File", "Video", "Music"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**{STR} The Cover Photo For Files Has Been Saved!**",
    "notsave": "**{STR} The Cover Photo Is Not Saved!**",
    "adding": "**{STR} Adding Cover To Your File ...**",
    "added": "**{STR} The Cover Photo Is Added To Your File!**",
    "notcover": "**{STR} The File Has No Cover Photo!**",
    "getcover": "**{STR} The Cover Photo For File!**"
}

@client.Command(command="SetCover")
async def setcover(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Cover.png")
    client.DB.set_key("FILE_COVER", info)
    await event.edit(client.getstrings(STRINGS)["save"])  

@client.Command(command="AddCover")
async def addcover(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["File", "Music"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    cover = client.PATH + "Cover.png"
    if not os.path.exists(cover):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    await event.edit(client.getstrings(STRINGS)["adding"])
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, file, thumb=cover, caption=client.getstrings(STRINGS)["added"], progress_callback=callback)
    os.remove(file)
    await edit.delete()
    
@client.Command(command="GetCover")
async def getcover(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["File", "Video", "Music"]):
        return await event.edit(reply)
    if not event.reply_message.document.thumbs:
        return await event.edit(client.getstrings(STRINGS)["notcover"])
    cover = await event.reply_message.download_media(client.PATH, thumb=-1)
    await event.respond(client.getstrings(STRINGS)["getcover"], file=cover)
    os.remove(cover)
    await edit.delete()