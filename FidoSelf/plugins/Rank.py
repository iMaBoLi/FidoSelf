from FidoSelf import client

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Rank",
    "Pluginfo": {
        "Help": "To Manage Rank Of Users In Self!",
        "Commands": {
            "{CMD}SetRank <Rank> <Reply>": None,
            "{CMD}DelRank <Reply|Userid|Username>": None,
            "{CMD}GetRank <Reply|Userid|Username>": None,
            "{CMD}RankList": None,
            "{CMD}CleanRankList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setrank": "**The Rank Of User** ( {} ) **Was Set To** ( `{}` )",
    "notrank": "**The Rank For User** ( {} ) **Is Not Saved!**",
    "delrank": "**The Rank Of User** ( {} ) **Has Been Deleted!**",
    "getrank": "**The Rank Of User** ( {} ) **Is** ( `{}` )",
    "empty": "**The Rank List Is Empty!**",
    "ranklist": "**The Ranks List:**\n\n",
    "aempty": "**The Rank List Is Already Empty**",
    "clean": "**The Rank List Has Been Cleaned!**",
}

@client.Command(command="SetRank (.*)")
async def setrank(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid()
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    rank = event.pattern_match.group(1)
    ranks = client.DB.get_key("RANKS") or {}
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    ranks.update({userid: rank})
    client.DB.set_key("RANKS", ranks)
    await event.edit(STRINGS["setrank"].format(mention, rank))
    
@client.Command(command="DelRank ?(.*)?")
async def delrank(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    ranks = client.DB.get_key("RANKS") or {}
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in ranks:
        return await event.edit(STRINGS["notrank"].format(mention))  
    del ranks[userid]
    client.DB.set_key("RANKS", ranks)
    await event.edit(STRINGS["delrank"].format(mention))
    
@client.Command(command="GetRank ?(.*)?")
async def getrank(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    ranks = client.DB.get_key("RANKS") or {}
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in ranks:
        return await event.edit(STRINGS["notrank"].format(mention))  
    rank = ranks[userid]
    await event.edit(STRINGS["getrank"].format(mention, rank))
    
@client.Command(command="RankList")
async def ranklist(event):
    await event.edit(client.STRINGS["wait"])
    ranks = client.DB.get_key("RANKS") or {}
    if not ranks:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["ranklist"]
    row = 1
    for rank in ranks:
        text += f"**{row} -** `{rank}` - `{ranks[rank]}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanRankList")
async def cleanranklist(event):
    await event.edit(client.STRINGS["wait"])
    ranks = client.DB.get_key("RANKS") or {}
    if not ranks:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("RANKS")
    await event.edit(STRINGS["clean"])