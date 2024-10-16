from TNTSelf import client

__INFO__ = {
    "Category": "Groups",
    "Name": "Delete Msg",
    "Info": {
        "Help": "To Delete Message In Chats!",
        "Commands": {
            "{CMD}Del <Count>": {
                "Help": "To Delete Messages",
                "Input": {
                    "<Count>": "Number Of Messages",
                },
            },
            "{CMD}Del <Count>": {
                "Help": "To Delete Messages Of User",
                "Input": {
                    "<Count>": "Number Of Messages",
                },
                "Getid": "You Must Reply To User",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "chatdel": "**{STR} The** ( `{}` ) **Message In This Chat Was Deleted!**",
    "userdel": "**{STR} The** ( `{}` ) **Message From User** ( {} ) **In This Chat Was Deleted!**"
}

@client.Command(command="Del (\\d*)")
async def deletemsg(event):
    await event.edit(client.STRINGS["wait"])
    limit = int(event.pattern_match.group(1))
    if not limit:
        if event.is_reply:
            await event.reply_message.delete(revoke=True)
        return await event.delete(revoke=True)
    if event.is_reply:
        mention = client.functions.mention(event.reply_message.sender)
        messages = []
        count = 0
        async for message in client.iter_messages(event.chat_id, from_user=event.reply_message.sender_id, limit=limit):
            if message.id == event.id: continue
            messages.append(message.id)
            count += 1
        await client.delete_messages(event.chat_id, messages)
        await event.edit(client.getstrings(STRINGS)["userdel"].format(count, mention))
    else:
        messages = []
        count = 0
        async for message in client.iter_messages(event.chat_id, limit=limit + 1):
            if message.id == event.id: continue
            messages.append(message.id)
            count += 1
        await client.delete_messages(event.chat_id, messages)
        await event.edit(client.getstrings(STRINGS)["chatdel"].format(count))