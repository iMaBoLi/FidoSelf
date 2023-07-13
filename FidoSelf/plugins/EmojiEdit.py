from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Name": "Emoji",
    "Info": {
        "Help": "To Add Emoji On Your Text Messages!",
        "Commands": {
            "{CMD}Emoji <On-Off>": None,
            "{CMD}SetEmoji <Emoji>-<Emoji>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Emoji Mode Has Been {}!**",
    "setemoji": "**{STR} The Edit Emojis Was Set To** ( `{}` )"
}

@client.Command(command="Emoji (On|Off)")
async def emojimode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("EMOJI_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="SetEmoji (.*)\-(.*)")
async def setemoji(event):
    await event.edit(client.STRINGS["wait"])
    emoji1 = event.pattern_match.group(1)
    emoji2 = event.pattern_match.group(2)
    emojis = emoji1 + "-" + emoji2
    client.DB.set_key("EDIT_EMOJIS", emojis)
    text = client.getstrings(STRINGS)["setemoji"].format(emojis)
    await event.edit(text)

@client.Command(allowedits=False, checkCmd=True)
async def emoji(event):
    if not event.text: return
    mode = client.DB.get_key("EMOJI_MODE") or "OFF"
    emojis = client.DB.get_key("EDIT_EMOJIS") or ""
    if mode == "OFF" or not emojis: return
    emoji1 = emojis.split("-")[0]
    emoji2 = emojis.split("-")[1]
    ntext = emoji1 + " " + event.text + " " + emoji2
    await event.edit(ntext)