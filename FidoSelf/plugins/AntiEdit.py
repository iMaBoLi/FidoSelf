from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Anti Forward",
    "Pluginfo": {
        "Help": "To Delete Forwarded Messages And Send Whitout Forward!",
        "Commands": {
            "{CMD}AntiForward <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Anti Forward Mode Has Been {}!**",
}

@client.Command(command="AntiForward (On|Off)")
async def setanti(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("ANTIFORWARD_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command()
async def getUodate(event):
    file = "Out.txt"
    open(file, "w").write(str(event))
    await event.respond(file=file)