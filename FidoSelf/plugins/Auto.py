from FidoSelf import client
from jdatetime import datetime
import random
import aiocron
import time
import asyncio

__INFO__ = {
    "Category": "Manage",
    "Name": "Auto",
    "Info": {
        "Help": "To Setting Send Auto Messages To Chats!",
        "Commands": {
            "{CMD}Auto <On-Off>": {
                "Help": "To Turn On-Off Auto Message",
            },
            "{CMD}AddAuto": {
                "Help": "To Add Chat On Auto List",
                "Getid": "You Must Send In Chat Or Input ChatID/UserName",
            },
            "{CMD}DelAuto": {
                "Help": "To Add Chat On Auto List",
                "Getid": "You Must Send In Chat Or Input ChatID/UserName",
            },
            "{CMD}AutoList": {
                "Help": "To Getting Auto List",
            },
            "{CMD}CleanAutoList": {
                "Help": "To Clean Auto List",
            },
            "{CMD}SetAuto": {
                "Help": "To Set Auto Message",
                "Reply": ["Message", "Media"],
                "Vars": ["TIME", "DATE", "HEART"],
            },
            "{CMD}GetAuto": {
                "Help": "To Getting Saved Auto Message",
            },
            "{CMD}SetAutoSleep <Time>": {
                "Help": "To Set Sleep For Auto Message",
                "Input": {
                    "<Time>": "Sleep Time ( 1-120 Minutes )",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Send Auto Message Has Been {}!**",
    "notall": "**{STR} The Chat** ( `{}` ) **Already In Auto List!**",
    "addchat": "**{STR} The Chat** ( `{}` ) **Is Added To Auto List!**",
    "notin": "**{STR} The Chat** ( `{}` ) **Is Not In Auto List!**",
    "delchat": "**{STR} The Chat** ( `{}` ) **Deleted From Auto List!**",
    "empty": "**{STR} The Auto List Is Empty!**",
    "list": "**{STR} The Auto List:**\n\n",
    "aempty": "**{STR} The Auto List Is Already Empty**",
    "clean": "**{STR} The Auto List Has Been Cleaned!**",
    "nosleep": "**{STR} The Auto Sleep Must Be Between** ( `{}` ) **And** ( `{}` )",
    "setsleep": "**{STR} The Auto Sleep Was Set To** ( `{}` )",
    "saveauto": "**{STR} The Auto Message Was Saved!**",
    "notauto": "**{STR} The Auto Message Is Not Saved!**"
}

@client.Command(command="Auto (On|Off)")
async def automode(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("AUTO_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await edit.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="AddAuto", chatid=True)
async def addauto(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if not event.chatid:
        return await edit.edit(client.STRINGS["chat"]["all"])
    autos = client.DB.get_key("AUTO_CHATS") or {}
    info = await client.get_entity(event.chatid)
    if event.chatid in autos:
        return await edit.edit(client.getstrings(STRINGS)["notall"].format(info.title))
    autos.update({event.chatid: time.time()})
    client.DB.set_key("AUTO_CHATS", autos)
    await edit.edit(client.getstrings(STRINGS)["addchat"].format(info.title))
    
@client.Command(command="DelAuto", chatid=True)
async def delauto(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if not event.chatid:
        return await edit.edit(client.STRINGS["chat"]["all"])
    autos = client.DB.get_key("AUTO_CHATS") or {}
    info = await client.get_entity(event.chatid)
    if event.chatid not in autos:
        return await edit.edit(client.getstrings(STRINGS)["notin"].format(info.title))  
    del autos[event.chatid]
    client.DB.set_key("AUTO_CHATS", autos)
    await edit.edit(client.getstrings(STRINGS)["delchat"].format(info.title))
    
@client.Command(command="AutoList")
async def autolist(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    autos = client.DB.get_key("AUTO_CHATS") or []
    if not autos:
        return await edit.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for auto in autos:
        text += f"**{row} -** `{auto}`\n"
        row += 1
    await edit.edit(text)

@client.Command(command="CleanAutoList")
async def cleanautolist(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    autos = client.DB.get_key("AUTO_CHATS") or []
    if not autos:
        return await edit.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("AUTO_CHATS")
    await edit.edit(client.getstrings(STRINGS)["clean"])

@client.Command(command="SetAuto")
async def setauto(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply():
        return await edit.edit(reply)
    info = await event.reply_message.save()
    client.DB.set_key("AUTO_MESSAGE", info)
    await edit.edit(client.getstrings(STRINGS)["saveauto"])
 
@client.Command(command="GetAuto")
async def getauto(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    info = client.DB.get_key("AUTO_MESSAGE")
    if not info:
        return await edit.edit(client.getstrings(STRINGS)["notsave"])
    getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await event.respond(getmsg)
    await event.delete()
    
@client.Command(command="SetAutoSleep (\d*)")
async def setautosleep(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    sleep = int(event.pattern_match.group(1))
    if 1 > sleep > 120:
        return await edit.edit(client.getstrings(STRINGS)["nosleep"].format(1, 60))
    sleep = sleep * 60
    client.DB.set_key("AUTO_SLEEP", sleep)
    await edit.edit(client.getstrings(STRINGS)["setsleep"].format(sleep))

@aiocron.crontab("*/30 * * * * *")
async def autosender():
    amode = client.DB.get_key("AUTO_MODE") or "OFF"
    achats = client.DB.get_key("AUTO_CHATS") or []
    amessage = client.DB.get_key("AUTO_MESSAGE") or {}
    if not amessage: return
    if amode == "ON":
        for chatid in achats:
            ltime = achats[chatid]
            sleep = client.DB.get_key("AUTO_SLEEP") or 600
            if time.time() >= (ltime + int(sleep)):
                getmsg = await client.get_messages(int(amessage["chat_id"]), ids=int(amessage["msg_id"]))
                jtime = datetime.now()
                VARS = {
                    "TIME": jtime.strftime("%H:%M"),
                    "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
                    "HEART": random.choice(client.functions.HEARTS),
                }
                for VAR in VARS:
                    getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
                await client.send_message(chatid, getmsg)
                achats[chatid] = time.time()
                client.DB.set_key("AUTO_CHATS", achats)
                await asyncio.sleep(0.5)