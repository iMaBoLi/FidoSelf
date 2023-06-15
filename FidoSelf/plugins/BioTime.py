from FidoSelf import client

__INFO__ = {
    "Category": "Time",
    "Plugname": "Bio Time",
    "Pluginfo": {
        "Help": "To Save Your Bios For Time In Bio And Turn On-Off!",
        "Commands": {
            "{CMD}NewBio <Text>": None,
            "{CMD}DelBio <Text>": None,
            "{CMD}BioList": None,
            "{CMD}CleanBioList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "newnot": "**The Bio** ( `{}` ) **Already In Bio List!**",
    "newadd": "**The Bio** ( `{}` ) **Added To Bio List!**",
    "delnot": "**The Bio** ( `{}` ) **Not In Bio List!**",
    "del": "**The Bio** ( `{}` ) **Deleted From Bio List!**",
    "empty": "**The Bio List Is Empty!**",
    "list": "**The Bio List:**\n\n",
    "aempty": "**The Bio List Is Already Empty!**",
    "clean": "**The Bio List Is Cleaned!**",
}

@client.Command(command="NewBio (.*)")
async def addbio(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIOS") or []
    newbio = str(event.pattern_match.group(1))
    if newbio in bios:
        return await event.edit(STRINGS["newnot"].format(newbio))  
    bios.append(newbio)
    client.DB.set_key("BIOS", bios)
    await event.edit(STRINGS["newadd"].format(newbio))
    
@client.Command(command="DelBio (.*)")
async def delbio(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIOS") or []
    newbio = str(event.pattern_match.group(1))
    if newbio not in bios:
        return await event.edit(STRINGS["delnot"].format(newbio))  
    bios.remove(newbio)
    client.DB.set_key("BIOS", bios)
    await event.edit(STRINGS["del"].format(newbio))

@client.Command(command="BioList")
async def biolist(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIOS") or []
    if not bios:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for bio in bios:
        text += f"**{row} -** `{bio}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanBioList")
async def cleanbios(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIOS") or []
    if not bios:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("BIOS")
    await event.edit(STRINGS["clean"])