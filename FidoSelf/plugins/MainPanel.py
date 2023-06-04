from FidoSelf import client
from telethon import Button
from datetime import datetime
from .Action import ACTIONS
from .EditModes import EDITS

STRINGS = {
    "modepage": "**Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**Select Which Edit Mode You Want Turn On-Off:**",
    "actionpage": "**Select Which Action Mode You Want Turn On-Off:**",
    "readpage": "**Select Which Reader Mode You Want Turn On-Off:**",
    "close": "**The Panel Successfuly Closed!**",
    "Modes": {
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "TIMER_MODE": "Timer Save",
        "MUTE_PV": "Mute Pv",
        "LOCK_PV": "Lock Pv",
        "ANTISPAM_PV": "AntiSpam Pv",
        "READALL_MODE": "Read All",
        "READPV_MODE": "Read Pv",
        "READGP_MODE": "Read Group",
        "READCH_MODE": "Read Channel",
    "Random1": "Random",
    "Random2": "Random V2",
}

def get_pages_button(opage):
    buttons = []
    PAGES_COUNT = 8 + 1
    for page in range(1, PAGES_COUNT):
        name = client.functions.create_font(page, 5)
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
    buttons.append(get_pages_button())
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_time_buttons():
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT") or 1
    buttons = []
    rname = STRINGS["Random1"]
    rmode = client.STRINGS["inline"]["On"] if str(last) == "random" else client.STRINGS["inline"]["Off"]
    r2name = STRINGS["Random2"]
    r2mode = client.STRINGS["inline"]["On"] if str(last) == "random2" else client.STRINGS["inline"]["Off"]
    buttons.append(Button.inline(f"{rname} {rmode}", data=f"setfonttime:random"))
    buttons.append(Button.inline(f"{r2name} {r2mode}", data=f"setfonttime:random2"))
    for font in client.functions.FONTS:
        name = client.functions.create_font(newtime, font)
        mode = client.STRINGS["inline"]["On"] if str(last) == str(font) else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {mode}", data=f"setfonttime:{font}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button())
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_edit_buttons(chatid):
    lastall = client.DB.get_key("EDITALL_MODE")
    lastchat = client.DB.get_key("EDITCHATS_MODE") or {}
    buttons = []
    for edit in EDITS:
        gmode = "off" if chatid in lastchat and lastchat[chatid] == edit else "on"
        nmode = client.STRINGS["inline"]["On"] if gmode == "off" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{edit} {nmode}", data=f"seteditchat:{edit}:{chatid}"))
        name = edit + "All"        
        mode = client.STRINGS["inline"]["On"] if str(lastall) == str(edit) else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {mode}", data=f"seteditall:{edit}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button())
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closepanel")])
    return buttons

def get_action_buttons(chatid):
    buttons = []
    for action in ACTIONS:
        chats = client.DB.get_key(action.upper() + "_CHATS") or []
        gmode = "del" if chatid in chats else "add"
        name = action.replace("-", " ").title()
        nmode = client.STRINGS["inline"]["On"] if gmode == "del" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"actionchat:{action}:{chatid}:{gmode}"))
        gmode = client.DB.get_key(action.upper() + "_ALL") or "off"
        cmode = "on" if gmode == "off" else "off"
        name = action.replace("-", " ").title() + " All"
        nmode = client.STRINGS["inline"]["On"] if gmode == "on" else client.STRINGS["inline"]["Off"]
        buttons.append(Button.inline(f"{name} {nmode}", data=f"actionall:{action}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append(get_pages_button())
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
    client.LOGS.error(event.chat_id)
    page = int(event.data_match.group(1).decode('utf-8'))
    if page == 1:
        text = STRINGS["modepage"]
        buttons = get_mode_buttons()
    elif page == 2:
        text = STRINGS["fontpage"]
        buttons = get_time_buttons()
    elif page == 3:
        text = STRINGS["editpage"]
        buttons = get_edit_buttons(event.chat_id)
    elif page == 4:
        text = STRINGS["actionpage"]
        buttons = get_action_buttons(event.chat_id)
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

@client.Callback(data="seteditall\:(.*)")
async def seteditmode(event):
    edit = event.data_match.group(1).decode('utf-8')
    last = client.DB.get_key("EDITALL_MODE")
    if str(last) == str(edit):
        client.DB.set_key("EDITALL_MODE", False)
    else:
        client.DB.set_key("EDITALL_MODE", str(edit))
    buttons = get_edit_buttons(event.chat_id)
    await event.edit(buttons=buttons)
    
@client.Callback(data="seteditchat\:(.*)\:(.*)")
async def seteditmode(event):
    edit = event.data_match.group(1).decode('utf-8')
    chatid = int(event.data_match.group(2).decode('utf-8'))
    last = client.DB.get_key("EDITCHATS_MODE") or {}
    last[chatid] = edit
    client.DB.set_key("EDITALL_MODE", last)
    buttons = get_edit_buttons()
    await event.edit(buttons=buttons)
    
@client.Callback(data="actionall\:(.*)\:(.*)")
async def actionall(event):
    action = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(2).decode('utf-8')
    action = action.upper() + "_ALL"
    client.DB.set_key(action, change)
    text = STRINGS["actionpage"]
    buttons = get_action_buttons(event.chat_id)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="actionchat\:(.*)\:(.*)\:(.*)")
async def actionschats(event):
    client.LOGS.error(event.chat_instance)
    action = event.data_match.group(1).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    action = action.upper() + "_CHATS"
    last = client.DB.get_key(action) or []
    if change == "del":
        new = last.remove(chatid)
        client.DB.set_key(action, new)
    elif change == "add":
        new = last + [chatid]
        client.DB.set_key(action, new)
    text = STRINGS["actionpage"]
    buttons = get_action_buttons(event.chat_id)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    text = STRINGS["close"]
    await event.edit(text=text)