from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Name": "Anti Forward",
    "Info": {
        "Help": "To Delete Forwarded Messages And Send Whitout Forward!",
        "Commands": {
            "{CMD}AntiForward <On-Off>": {
                "Help": "To Turn On-Off Anti Forward"
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Anti Forward Mode Has Been {}!**"
}

@client.Command(command="AntiForward (On|Off)")
async def setantiforward(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ANTIFORWARD_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await edit.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(allowedits=False)
async def antiforward(event):
    if event.checkCmd() or not event.fwd_from or event.is_ch: return
    antimode = client.DB.get_key("ANTIFORWARD_MODE") or "OFF"
    if antimode == "ON":
        getmsg = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(getmsg)
        await event.delete()