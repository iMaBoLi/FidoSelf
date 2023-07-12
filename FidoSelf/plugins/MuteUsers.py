from FidoSelf import client
from datetime import timedelta

__INFO__ = {
    "Category": "Groups",
    "Name": "Mute",
    "Info": {
        "Help": "To Mute/UnMute Users In Chats!",
        "Commands": {
            "{CMD}Mute": {
                "Help": "To Mute User",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}UnMute": {
                "Help": "To UnMute User",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}TMute <Time>": {
                "Help": "To Mute User For Minutes",
                "Getid": "You Must Reply To User",
                "Input": {
                    "<Time>": "Time For Mute (Minutes)",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notacs": "**{STR} You Do Not Have Access To Mute/UnMute Users!**",
    "muteuser": "**{STR} The User** ( {} ) **Was Muted In This Chat!**",
    "errormute": "**{STR} The User** ( {} ) **Is Not Muted!**\n**Error:** ( `{}` )",
    "tmuteuser": "**{STR} The User** ( {} ) **Was Muted For** ( `{}` ) **In This Chat!**",
    "unmuteuser": "**{STR} The User** ( {} ) **Was UnMuted In This Chat!**",
    "errorunabn": "**{STR} The User** ( {} ) **Is Not UnMuted!**\n**Error:** ( `{}` )"
}

@client.Command(command="Mute", userid=True)
async def muteuser(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(client.getstrings(STRINGS)["notacs"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, send_messages=False)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errormute"].format(mention, error))
    text = client.getstrings(STRINGS)["muteuser"].format(mention)
    await event.edit(text)

@client.Command(command="TMute (\d*)")
async def timermuteuser(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    timer = int(event.pattern_match.group(1))
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["user"]["reply"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(client.getstrings(STRINGS)["notacs"])
    userid = event.reply_message.sender_id
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, timedelta(seconds=timer), send_messages=False)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errormute"].format(mention, error))
    stimer = client.functions.convert_time(timer)
    text = client.getstrings(STRINGS)["tmuteuser"].format(mention, stimer)
    await event.edit(text)
    
@client.Command(command="UnMute", userid=True)
async def unmuteuser(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(client.getstrings(STRINGS)["notacs"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errorunmute"].format(mention, error))
    text = client.getstrings(STRINGS)["unmuteuser"].format(mention)
    await event.edit(text)