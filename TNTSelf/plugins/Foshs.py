from TNTSelf import client
import os

__INFO__ = {
    "Category": "Manage",
    "Name": "Foshs",
    "Info": {
        "Help": "To Manage Fosh File For Enemies!",
        "Commands": {
            "{CMD}SetFosh <Reply(File)>": {
                "Help": "To Save Fosh File",
                "Reply": ["TXT File"]
            },
            "{CMD}DelFosh": {
                "Help": "To Delete Fosh File",
            },
            "{CMD}GetFosh": {
                "Help": "To Getting Fosh File",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**{STR} The Enemy Foshs File Has Been Saved!**",
    "del": "**{STR} The Enemy Foshs File Has Been Deleted!**",
    "nsave": "**{STR} The Enemy Foshs File Is Not Saved!**",
    "file": "**{STR} The Foshs File!**\n**Count:** ( `{}` )"
}

@client.Command(command="SetFosh")
async def savefoshfile(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["TXT File"]):
        return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "FOSHS.txt")
    client.DB.set_key("FOSHS_FILE", info)
    await event.edit(client.getstrings(STRINGS)["save"])

@client.Command(command="DelFosh")
async def delfoshfile(event):
    await event.edit(client.STRINGS["wait"])
    if os.path.exists(client.PATH + "FOSHS.txt"):
        os.remove(client.PATH + "FOSHS.txt")
    client.DB.del_key("FOSHS_FILE")
    await event.edit(client.getstrings(STRINGS)["del"])

@client.Command(command="GetFosh")
async def getfoshfile(event):
    await event.edit(client.STRINGS["wait"])
    foshs = client.DB.get_key("FOSHS_FILE")
    if not foshs:
        return await event.edit(client.getstrings(STRINGS)["nsave"])
    file = client.PATH + "FOSHS.txt"
    lines = len(open(file, "r").readlines())
    await event.respond(client.getstrings(STRINGS)["file"].format(lines), file=file)