from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Name": "Anti Forward",
    "Info": {
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
async def setantiforward(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ANTIFORWARD_MODE", change)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(allowedits=False)
async def antiforward(event):
    if event.checkCmd() or not event.fwd_from or event.is_ch: return
    antimode = client.DB.get_key("ANTIFORWARD_MODE") or "OFF"
    if antimode == "ON":
        getmsg = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(getmsg)
        await event.delete()