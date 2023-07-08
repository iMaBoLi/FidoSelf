from FidoSelf import client
from telethon import functions
import aiocron

__INFO__ = {
    "Category": "Setting",
    "Name": "Online",
    "Info": {
        "Help": "To Setting Online Status For Account!",
        "Commands": {
            "{CMD}Online <On-Off>": {
                "Help": "To Turn On-Off Online Mode",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**❁ The Online Has Been {}!**",
}

@client.Command(command="Online (On|Off)")
async def onlinemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ONLINE_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@aiocron.crontab("*/5 * * * * *")
async def autosender():
    onmode = client.DB.get_key("ONLINE_MODE") or "OFF"
    if onmode == "ON":
        await client(functions.account.UpdateStatusRequest(offline=False))
