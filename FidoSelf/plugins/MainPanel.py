from FidoSelf import client
from telethon import Button
from datetime import datetime
from FidoSelf.functions import FONTS, create_font
import time

STRINGS = {
    "modepage": "**Please Use The Buttons Below To Control The Different Parts:**",
    "fontpage": "**Please Use The Options Below To Select The Font You Want To Use In Time Name And Bio:**",
    "editpage": "**Please Use The Options Below To Manage Edit Texts Mode:**",
    "close": "**The Panel Successfuly Closed!**",
    "Modes": {
        "AUTO_DELETE_MODE": "Auto Delete",
        "AUTO_REPLACE_MODE": "Auto Replace",
        "AUTO_SAY_MODE": "Auto Say",
        "MONSHI_MODE": "Monshi",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "TIMER_MODE": "Timer Save",
        "MUTE_PV": "Mute Pv",
        "LOCK_PV": "Lock Pv",
        "ANTISPAM_PV": "AntiSpam Pv",
        "READALL_MODE": "Mark All",
        "READPV_MODE": "Mark Pv",
        "READGP_MODE": "Mark Group",
        "READCH_MODE": "Mark Channel",
    },
    "Edits": {
        "Bold": "Bold",
        "Mono": "Mono",
        "Italic": "Italic",
        "Underline": "Underline",
        "Strike": "Strike",
        "Spoiler": "Spoiler",
        "Hashtag": "Hashtag",
    },
    "Random1": "Random",
    "Random2": "Random V2",
}

def get_pages_button():
    buttons = []
    PAGES_COUNT = 5 + 1
    for page in range(1, PAGES_COUNT):
        name = client.functions.create_font(page, 3)
        buttons.append(Button.inline(f"( {name} )", data=f"panelpage:{page}"))
    return buttons

def get_mode_buttons():
    buttons = []
    MODES = STRINGS["Modes"]
    for mode in MODES:
        gmode = client.DB.get_key(mode) or "off"
        cmode = "on" if gmode == "off" else "off"
        name = MODES[mode]
        nmode = client.STRINGS["inline"]["On"] if gmode == "on" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"setmode:{mode}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
    pgbts = get_pages_button()
    buttons.append(pgbts)
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_time_buttons():
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT") or 1
    buttons = []
    buttons.append([Button.inline(f'• {STRINGS["Random1"]} •', data=f"setfonttime:random"), Button.inline((client.STRINGS["inline"]["On"] if str(last) == "random" else client.STRINGS["inline"]["Off"]), data=f"setfonttime:random")])
    buttons.append([Button.inline(f'• {STRINGS["Random2"]} •', data=f"setfonttime:random2"), Button.inline((client.STRINGS["inline"]["On"] if str(last) == "random2" else client.STRINGS["inline"]["Off"]), data=f"setfonttime:random2")])
    for font in FONTS:
        buttons.append([Button.inline(f"• {create_font(newtime, font)} •", data=f"setfonttime:{font}"), Button.inline((client.STRINGS["inline"]["On"] if str(last) == str(font) else client.STRINGS["inline"]["Off"]), data=f"setfonttime:{font}")])
    pgbts = get_pages_button()
    buttons.append(pgbts)
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_edit_buttons():
    last = client.DB.get_key("EDIT_MODE")
    buttons = []
    EDITS = STRINGS["Edits"]
    for edit in EDITS:
        buttons.append([Button.inline(f"• {EDITS[edit]} •", data=f"seteditmode:{edit}"), Button.inline((client.STRINGS["inline"]["On"] if str(last) == str(edit) else client.STRINGS["inline"]["Off"]), data=f"seteditmode:{edit}")])
    pgbts = get_pages_button()
    buttons.append(pgbts)
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

@client.Command(command="Panel")
async def addecho(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "selfmainpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="selfmainpanel")
async def inlinepanel(event):
    text = STRINGS["modepage"]
    buttons = get_mode_buttons()
    await event.answer([event.builder.article("FidoSelf - Panel", text=text, buttons=buttons)])

@client.Callback(data="panelpage\:(.*)")
async def panelpages(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    if page == 1:
        text = STRINGS["modepage"]
        buttons = get_mode_buttons()
        await event.edit(text=text, buttons=buttons)
    elif page == 2:
        text = STRINGS["fontpage"]
        buttons = get_time_buttons()
        await event.edit(text=text, buttons=buttons)
    elif page == 3:
        text = STRINGS["editpage"]
        buttons = get_edit_buttons()
        await event.edit(text=text, buttons=buttons)

@client.Callback(data="setmode\:(.*)\:(.*)")
async def setmode(event):
    mode = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(2).decode('utf-8')
    client.DB.set_key(mode, change)
    text = STRINGS["modepage"]
    buttons = get_mode_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="setfonttime\:(.*)")
async def setfonttime(event):
    font = event.data_match.group(1).decode('utf-8')
    client.DB.set_key("TIME_FONT", str(font))
    buttons = get_time_buttons()
    await event.edit(buttons=buttons)

@client.Callback(data="seteditmode\:(.*)\:(.*)")
async def seteditmode(event):
    edit = event.data_match.group(1).decode('utf-8')
    last = client.DB.get_key("EDIT_MODE")
    if str(last) == str(edit):
        client.DB.set_key("EDIT_MODE", False)
    else:
        client.DB.set_key("EDIT_MODE", str(edit))
    buttons = get_edit_buttons()
    await event.edit(buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    text = STRINGS["close"]
    await event.edit(text=text)