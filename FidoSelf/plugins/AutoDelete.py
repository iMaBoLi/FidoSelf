from FidoSelf import client
import aiocron
import time

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Auto Delete",
    "Pluginfo": {
        "Help": "To Setting Auto Delete Messages In Chats!",
        "Commands": {
            "{CMD}AutoDelete <On-Off>": None,
            "{CMD}SetDeleteSleep <1-120min>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Auto Delete Message Has Been {}!**",
    "nosleep": "**The Auto Delete Sleep Must Be Between** ( `{}` ) **And** ( `{}` )",
    "setsleep": "**The Auto Delete Sleep Was Set To** ( `{}` )",
}

@client.Command(command="AutoDelete (On|Off)")
async def delautomode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("AUTODELETE_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))
    
@client.Command(command="SetDeleteSleep (\d*)")
async def setautosleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = int(event.pattern_match.group(1))
    if 1 > sleep > 120:
        return await event.edit(STRINGS["nosleep"].format(1, 60))
    sleep = sleep * 60
    client.DB.set_key("AUTODELETE_SLEEP", sleep)
    await event.edit(STRINGS["setsleep"].format(sleep))

@client.Command(alowedits=False)
async def autodelete(event):
    if event.checkCmd(): return
    automode = client.DB.get_key("AUTODELETE_MODE") or "OFF"
    if automode == "ON":
        MSGS = client.DB.get_key("AUTODELETE_MSGS") or {}
        msginfo = str(event.chat_id) + ":" + str(event.id)
        MSGS.update({msginfo: time.time()})
        client.DB.set_key("AUTODELETE_MSGS", MSGS)

@aiocron.crontab("*/30 * * * * *")
async def autosender():
    MSGS = client.DB.get_key("AUTODELETE_MSGS") or {}
    if not MSGS: return
    for msg in MSGS:
        ltime = MSGS[msg]
        sleep = client.DB.get_key("AUTODELETE_SLEEP") or 600
        if time.time() >= (ltime + int(sleep)):
            info = msg.split(":")
            getmsg = await client.get_messages(int(info[0]), ids=int(info[1]))
            await getmsg.delete()
            del MSGS[msg]
            client.DB.set_key("AUTODELETE_MSGS", MSGS)