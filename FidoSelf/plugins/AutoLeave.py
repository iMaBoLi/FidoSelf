from FidoSelf import client
from telethon import events, functions

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Auto Leave",
    "Pluginfo": {
        "Help": "To Manage Auto Leave To Joined Chats!",
        "Commands": {
            "{CMD}AutoLeave <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Auto Leave Mode Has Been {}!**",
}

@client.Command(command="AutoLeave (On|Off)")
async def autoleavemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("AUTOLEAVE_MODE", change)
    schange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(schange))
    
@client.on(events.ChatAction())
async def autoleave(event):
    if not event.user_joined and not event.added_by: return
    user = await event.get_user()
    if user.id != client.me.id: return
    aleavemode = client.DB.get_key("AUTOLEAVE_MODE") or "OFF"
    if aleavemode == "ON":
        chat = await event.get_chat()
        await client(functions.channels.LeaveChannelRequest(channel=chat.id))