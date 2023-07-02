from FidoSelf import client
from telethon import events, functions
from jdatetime import datetime
import aiocron
import random

__INFO__ = {
    "Category": "Practical",
    "Plugname": "GoodBy",
    "Pluginfo": {
        "Help": "To Manage Auto GoodBy In The Chats!",
        "Commands": {
            "{CMD}GoodBy <On-Off>": None,
            "{CMD}SetGoodBy <Reply>": None,
            "{CMD}DelGoodBy": None,
            "{CMD}GetGoodBy": None,
            "{CMD}GoodByList": None,
            "{CMD}CleanGoodByList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The GoodBy Mode Has Been {}!**",
    "setgoodby": "**The GoodBy Message For This Chat Has Been Saved!**",
    "notsave": "**The GoodBy Message For This Chat Is Not Saved!**",
    "delgoodby": "**The GoodBy Message For This Chat Has Been Removed!**",
    "empty": "**The GoodBy List Is Empty!**",
    "list": "**The GoodBy List:**\n\n",
    "aempty": "**The GoodBy List Is Already Empty**",
    "clean": "**The GoodBy List Has Been Cleaned!**",
}

@client.Command(command="GoodBy (On|Off)")
async def goodbymode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("GOODBY_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="SetGoodBy")
async def setgoodby(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if reply:= event.checkReply():
        return await event.edit(reply)
    goodbys = client.DB.get_key("GOODBY_CHATS") or {}
    info = await event.reply_message.save()
    goodbys.update({event.chat_id: info})
    client.DB.set_key("GOODBY_CHATS", goodbys)
    await event.edit(STRINGS["setgoodby"])
    
@client.Command(command="DelGoodBy")
async def delgoodby(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    goodbys = client.DB.get_key("GOODBY_CHATS") or {}
    if event.chat_id not in goodbys:
        return await event.edit(STRINGS["notsave"])  
    del goodbys[event.chat_id]
    client.DB.set_key("GOODBY_CHATS", goodbys)
    await event.edit(STRINGS["delgoodby"])
 
@client.Command(command="GetGoodby")
async def getgoodby(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    comments = client.DB.get_key("GOODBY_CHATS") or {}
    if event.chat_id not in comments:
        return await event.edit(STRINGS["notsave"])
    info = comments[event.chat_id]
    getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await event.respond(getmsg)
    await event.delete()
    
@client.Command(command="GoodByList")
async def goodbylist(event):
    await event.edit(client.STRINGS["wait"])
    goodbys = client.DB.get_key("GOODBY_CHATS") or {}
    if not goodbys:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for goodby in goodbys:
        text += f"**{row} -** `{goodby}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanGoodByList")
async def cleangoodbylist(event):
    await event.edit(client.STRINGS["wait"])
    goodbys = client.DB.get_key("GOODBY_CHATS") or {}
    if not goodbys:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("GOODBY_CHATS")
    await event.edit(STRINGS["clean"])
    
@client.on(events.ChatAction())
async def autogoodby(event):
    if event.user_left or event.user_kicked:
        goodbymode = client.DB.get_key("GOODBY_MODE") or "OFF"
        chats = client.DB.get_key("GOODBY_CHATS") or {}
        if event.chat_id not in chats: return
        if goodbymode == "ON":
            info = chats[event.chat_id]
            getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
            chat = await event.get_chat()
            user = await event.get_user()
            jtime = datetime.now()
            VARS = {
                "TIME": jtime.strftime("%H:%M"),
                "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
                "HEART": random.choice(client.functions.HEARTS),
                "FIRSTNAME": user.first_name,
                "MENTION": client.functions.mention(user),
                "USERNAME": user.username or "---",
                "TITLE": chat.title,
                "CHATUSERNAME": chat.username or "---",
                "COUNT": chat.participants_count or "---",
            }
            for VAR in VARS:
                getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
            await event.reply(getmsg)