from FidoSelf import client
from telethon import Button

STRINGS = {
    "menu": "**Please Use The Buttons Below To Control The Filter Medias In Pv:**",
    "types": {
        "FILTERPV_TEXT": "Text",
        "FILTERPV_PHOTO": "Photo",
        "FILTERPV_VIDEO": "Video",
        "FILTERPV_GIF": "Gif",
        "FILTERPV_VOICE": "Voice",
        "FILTERPV_MUSIC": "Music",
        "FILTERPV_STICKER": "Sticker",
        "FILTERPV_ANISTICKER": "Animated Sticker",
        "FILTERPV_FILE": "File",
        "FILTERPV_LINK": "Link",
    },
}

def get_filter_buttons():
    buttons = []
    TYPES = STRINGS["types"]
    for type in TYPES:
        last = client.DB.get_key(type) or "off"
        smode = "( ✔️ )" if last == "on" else "( ✖️ )"
        cmode = "off" if last == "on" else "on"
        buttons.append(Button.inline(f"• {TYPES[type]} - {smode} •", data=f"setfilterpv:{type}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
    return buttons

@client.Command(command="AddPvFilter")
async def filterpvmedia(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "filtermediapv")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="filtermediapv")
async def inlinefilterpanel(event):
    text = STRINGS["menu"]
    buttons = get_filter_buttons()
    await event.answer([event.builder.article("FidoSelf - Filter Media Pv", text=text, buttons=buttons)])

@client.Callback(data="setfilterpv\:(.*)\:(.*)")
async def setfilterpvs(event):
    mode = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(2).decode('utf-8')
    client.DB.set_key(mode, change)
    text = STRINGS["menu"]
    buttons = get_filter_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Command(onlysudo=False, allowedits=False)
async def mediafilter(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    TYPES = STRINGS["types"]
    MODES = {}
    for type in TYPES:
        mode = client.DB.get_key(type) or "off" 
        MODES.update({type: mode})
    if event.text and MODES["FILTERPV_TEXT"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "Photo" and MODES["FILTERPV_PHOTO"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "Video" and MODES["FILTERPV_VIDEO"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "Gif" and MODES["FILTERPV_GIF"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "Voice" and MODES["FILTERPV_VOICE"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "Music" and MODES["FILTERPV_MUSIC"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "Sticker" and MODES["FILTERPV_STICKER"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "ASticker" and MODES["FILTERPV_ANISTICKER"] == "on":
        await event.delete()
    elif client.functions.mediatype(event) == "File" and MODES["FILTERPV_FILE"] == "on":
        await event.delete()
    elif event.text and MODES["FILTERPV_LINK"] == "on":
        if event.entities:
            for entity in event.to_dict()["entities"]:
                if entity["_"] in ["MessageEntityUrl"]:
                    await event.delete()