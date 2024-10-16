from TNTSelf import client
from telethon import functions
import aiocron

__INFO__ = {
    "Category": "Account",
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
    "change": "**{STR} The Online Mode Has Been {}!**"
}

@client.Command(command="Online (On|Off)")
async def onlinemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ONLINE_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@aiocron.crontab("*/30 * * * * *")
async def autoonliner():
    onmode = client.DB.get_key("ONLINE_MODE") or "OFF"
    if onmode == "ON":
        await client(functions.account.UpdateStatusRequest(offline=False))