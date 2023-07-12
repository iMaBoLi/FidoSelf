from FidoSelf import client
from telethon import functions, types, errors

__INFO__ = {
    "Category": "Groups",
    "Name": "Invite VC",
    "Info": {
        "Help": "To Invite Users To Voice Chat!",
        "Commands": {
            "{CMD}InvVc": {
                "Help": "To Invite Users",
            },
            "{CMD}InvVc <Users>": {
                "Help": "To Invite Inputed Users ( Use , To Split Answers )",
                "Input": {
                    "<Users>": "List Of UserIDs/Usernames",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notcall": "**{STR} The Voice Chat Is Not Founded For This Chat!**",
    "notuser": "**{STR} The Users To Invite In To Voice Chat Is Not Founded!**",
    "notflood": "**{STR} The Flood Wait Error Is Coming Please Wait And Try Again!**",
    "inviting": "**{STR} Inviting Users To Voice Chat ...**",
    "invited": "**{STR} Invite Users To Voice Chat Completed!**"
}

@client.Command(command="InvVc ?(.*)?")
async def invitevc(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    users = str(event.pattern_match.group(1) or "")
    if event.chat.megagroup or event.chat.broadcast:
        info = (await client(functions.channels.GetFullChannelRequest(event.chat_id))).full_chat
    else:
        info = (await client(functions.messages.GetFullChatRequest(event.chat_id))).full_chat
    if not info.call:
        return await edit.edit(client.getstrings(STRINGS)["notcall"])
    if users:
        usernames = users.replace("@", "").split(",")[:50]
    else:
        usernames = []
        async for user in client.iter_participants(event.chat_id, filter=types.ChannelParticipantsRecent, limit=50):
            usernames.append(user.id)
    if not usernames:
        return await edit.edit(client.getstrings(STRINGS)["notuser"])
    await edit.edit(client.getstrings(STRINGS)["inviting"])
    try:
        result = await client(functions.phone.InviteToGroupCallRequest(call=info.call, users=usernames))
    except errors.FloodWaitError:
        return await edit.edit(client.getstrings(STRINGS)["notflood"])
    except:
        pass
    await edit.edit(client.getstrings(STRINGS)["invited"])