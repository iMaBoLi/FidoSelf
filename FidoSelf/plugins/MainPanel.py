from FidoSelf import client
from telethon import Button
from datetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Panel",
    "Pluginfo": {
        "Help": "To Get Inline Panel To Setting Self!",
        "Commands": {
            "{CMD}Panel": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "changeturn":  "**➜ The {} Has Been {}!**",
    "changemode":  "**➜ The {} Has Been Set To:** ( `{}` )",
    "disablemode":  "**➜ The {} Has Been Disabled!**",
    "changeall":  "**➜ The {} For All Chats Has Been {}!**",
    "changechat":  "**➜ The {} For This Chat Has Been {}!**",
    "changechatmode":  "**➜ The {} For This Chat Has Been Set To:** ( `{}` )",
    "disablechatmode":  "**➜ The {} For This Chat Has Been Disabled!**",
    "modepage": "**❃ Select Which Mode You Want Turn On-Off:**",
    "fontpage": "**❃ Select Which Time Font You Want Turn On-Off:**",
    "editpage": "**❃ Select Which edit Mode You Want Turn On-Off:**",
    "actionpage": "**❃ Select Which Action Mode You Want Turn On-Off:**",
    "allpage": "☻︎ You Are Already In This Page!",
    "closepanel":  "**☻︎ The Panel Successfuly Closed!**",
}

def get_modename(mode):
    MODES ={
        "ONLINE_MODE": "Online",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "SIGN_MODE": "Sign",
        "EMOJI_MODE": "Emoji",
        "TIMER_MODE": "Timer Save",
        "ANTISPAM_PV": "AntiSpam Pv",
        "MUTE_PV": "Mute Pv",
        "LOCK_PV": "Lock Pv",
        "ANTIFORWARD_MODE": "Anti Forward",
        "ENEMY_DELETE": "Delete Enemy Pms",
        "READALL_MODE": "Read All",
        "READPV_MODE": "Read Pv",
        "READGP_MODE": "Read Group",
        "READCH_MODE": "Read Channel",
        "TIME_FONT": "Time Font",
        "EDITALL_MODE": "Edit Mode",
        "EDITCHATS_MODE": "Edit Chats Mode",
        "ACTION_ALL": "Send Action Mode",
        "ACTION_CHATS": "Send Action Mode",
        "ACTION_TYPE": "Action Type",
    }
    return MODES[mode]

@client.Command(command="Panel")
async def panel(event):
    await event.edit(client.STRINGS["wait"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"Panel:{chatid}:1")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Panel\:(.*)\:(.*)")
async def inlinepanel(event):
    chatid = event.pattern_match.group(1)
    page = int(event.pattern_match.group(2))
    await event.answer([event.builder.article("FidoSelf - Panel", text=get_text(page), buttons=get_buttons(chatid, page))])

@client.Callback(data="Page\:(.*)\:(.*)")
async def panelpages(event):
    chatid = event.data_match.group(1).decode('utf-8')
    page = int(event.data_match.group(2).decode('utf-8'))
    if page == 0:
        return await event.answer(STRINGS["allpage"], alert=True)
    await event.edit(text=get_text(page), buttons=get_buttons(chatid, page))

def get_text(page):
    if page == 1:
        text = STRINGS["modepage"]
    elif page == 2:
        text = STRINGS["modepage"]
    elif page == 3:
        text = STRINGS["fontpage"]
    elif page == 4:
        text = STRINGS["editpage"]
    elif page == 5:
        text = STRINGS["actionpage"]
    return text + f" **(** `Page {page}` **)**"

def get_pages_button(chatid, opage):
    buttons = []
    PAGES_COUNT = 5
    for page in range(1, PAGES_COUNT + 1):
        font = 4 if page != opage else 5
        data = page if page != opage else 0
        name = client.functions.create_font(page, font)
        buttons.append(Button.inline(f"( {name} )", data=f"Page:{chatid}:{data}"))
    return buttons

def get_buttons(chatid, page):
    buttons = []
    if page == 1:
        MODES = ["ONLINE_MODE", "NAME_MODE", "BIO_MODE", "PHOTO_MODE", "SIGN_MODE", "EMOJI_MODE", "TIMER_MODE", "ANTISPAM_PV", "MUTE_PV", "LOCK_PV"]
        for Mode in MODES:
            getMode = client.DB.get_key(Mode) or "off"
            value = "on" if getMode == "off" else "off"
            svalue = client.STRINGS["inline"]["On"] if getMode == "on" else client.STRINGS["inline"]["Off"]
            smode = get_modename(Mode)
            buttons.append(Button.inline(f"{smode} {svalue}", data=f"Set:{Mode}:{value}:Turn:{chatid}:{page}"))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 2:
        MODES = ["ANTIFORWARD_MODE", "ENEMY_DELETE", "READALL_MODE", "READPV_MODE", "READGP_MODE", "READCH_MODE"]
        for Mode in MODES:
            getMode = client.DB.get_key(Mode) or "off"
            value = "on" if getMode == "off" else "off"
            svalue = client.STRINGS["inline"]["On"] if getMode == "on" else client.STRINGS["inline"]["Off"]
            smode = get_modename(Mode)
            buttons.append(Button.inline(f"{smode} {svalue}", data=f"Set:{Mode}:{value}:Turn:{chatid}:{page}"))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 3:
        newtime = datetime.now().strftime("%H:%M")
        timefont = client.DB.get_key("TIME_FONT") or 1
        for randfont in ["random", "random2"]:
            svalue = client.STRINGS["inline"]["On"] if str(timefont) == randfont else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{randfont.title()} {svalue}", data=f"Set:TIME_FONT:{randfont}:Mode:{chatid}:{page}"))
        for font in client.functions.FONTS:
            smode = client.functions.create_font(newtime, font)
            svalue = client.STRINGS["inline"]["On"] if str(timefont) == str(font) else client.STRINGS["inline"]["Off"]
            buttons.append(Button.inline(f"{smode} {svalue}", data=f"Set:TIME_FONT:{font}:Mode:{chatid}:{page}"))
        buttons = list(client.functions.chunks(buttons, 2))
    elif page == 4:
        emode = client.DB.get_key("EDITALL_MODE")
        echats = client.DB.get_key("EDITCHATS_MODE") or {}
        Chbuttons = []
        Allbuttons = []
        for edit in client.functions.EDITS:
            getMode = "off" if (int(chatid) in echats and echats[int(chatid)] == edit) else "on"
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "off" else client.STRINGS["inline"]["Off"]
            Chbuttons.append(Button.inline(f"{edit} {ShowMode}", data=f"Set:EDITCHATS_MODE:{edit}:ChatModeDel:{chatid}:{page}"))
        for edit in client.functions.EDITS:
            sname = edit + " All"
            svalue = client.STRINGS["inline"]["On"] if str(emode) == str(edit) else client.STRINGS["inline"]["Off"]
            Allbuttons.append(Button.inline(f"{sname} {svalue}", data=f"Set:EDITALL_MODE:{edit}:ModeDel:{chatid}:{page}"))
        OthButton = [[Button.inline(" --------------- ", data="Empty")]]
        buttons = list(client.functions.chunks(Chbuttons, 3)) + OthButton + list(client.functions.chunks(Allbuttons, 3))
    elif page == 5:
        acMode = client.DB.get_key("ACTION_ALL") or "off"
        acChats = client.DB.get_key("ACTION_CHATS") or []
        Mact = client.STRINGS["inline"]["On"] if int(chatid) in acChats else client.STRINGS["inline"]["Off"]
        Cact = "del" if int(chatid) in acChats else "add"
        Mactall = client.STRINGS["inline"]["On"] if acMode == "on" else client.STRINGS["inline"]["Off"]
        Cactall = "on" if acMode == "off" else "off"
        buttons = [[Button.inline(f"Action {Mact}", data=f"Set:ACTION_CHATS:{Cact}:Chat:{chatid}:{page}"), Button.inline(f"Action All {Mactall}", data=f"Set:ACTION_ALL:{Cactall}:Turn:{chatid}:{page}")]]
        actbts = []
        for action in client.functions.ACTIONS:
            acType = client.DB.get_key("ACTION_TYPE") or "random"
            getMode = "on" if action == acType else "off"
            ShowName = action.replace("-", " ").title()
            ShowMode = client.STRINGS["inline"]["On"] if getMode == "on" else client.STRINGS["inline"]["Off"]
            actbts.append(Button.inline(f"{ShowName} {ShowMode}", data=f"Set:ACTION_TYPE:{action}:Mode:{chatid}:{page}"))
        actbts = list(client.functions.chunks(actbts, 3))
        buttons += actbts
    buttons.append(get_pages_button(chatid, page))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="ClosePanel")])
    return buttons
    
@client.Callback(data="Set\:(.*)\:(.*)\:(.*)\:(.*)\:(.*)")
async def setpanel(event):
    key = event.data_match.group(1).decode('utf-8')
    value = event.data_match.group(2).decode('utf-8')
    type = event.data_match.group(3).decode('utf-8')
    chatid = int(event.data_match.group(4).decode('utf-8'))
    page = int(event.data_match.group(5).decode('utf-8'))
    skey = get_modename(key)
    pagetext = get_text(page)
    if type == "Turn":
        client.DB.set_key(key, value)
        cshow = client.STRINGS["On"] if value == "on" else client.STRINGS["Off"]
        settext = STRINGS["changeturn"].format(skey, cshow)
    elif type == "Mode":
        client.DB.set_key(key, value)
        settext = STRINGS["changemode"].format(skey, value)
    elif type == "ModeDel":
        gvalue = client.DB.get_key(key)
        value = value if value != gvalue else None
        client.DB.set_key(key, value)
        if not value:
            settext = STRINGS["disablemode"].format(skey)
        else:
            settext = STRINGS["changemode"].format(skey, value)
    elif type == "ModeAll":
        client.DB.set_key(key, value)
        cshow = client.STRINGS["On"] if value == "on" else client.STRINGS["Off"]
        settext = STRINGS["changeall"].format(skey, cshow)
    elif type == "Chat":
        chats = client.DB.get_key(key) or []
        if value == "add":
            chats.append(chatid)
        elif value == "del":
            chats.remove(chatid)
        client.DB.set_key(key, chats)
        cshow = client.STRINGS["On"] if value == "add" else client.STRINGS["Off"]
        settext = STRINGS["changechat"].format(skey, cshow)
    elif type == "ChatMode":
        chats = client.DB.get_key(key) or {}
        if chatid not in chats:
            chats.update({chatid: None})
        chats[chatid] = value
        client.DB.set_key(key, chats)
        settext = STRINGS["changechatmode"].format(skey, value)
    elif type == "ChatModeDel":
        chats = client.DB.get_key(key) or {}
        if chatid not in chats:
            chats.update({chatid: None})
        value = value if chats[chatid] != value else None
        chats[chatid] = value
        client.DB.set_key(key, chats)
        if not value:
            settext = STRINGS["disablechatmode"].format(skey)
        else:
            settext = STRINGS["changechatmode"].format(skey, value)
    text = settext + "\n\n" + pagetext
    buttons = get_buttons(chatid, page)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="ClosePanel")
async def closepanel(event):
    await event.edit(text=STRINGS["closepanel"])
    
@client.Callback(data="Empty")
async def empty(event):
    await event.answer(client.STRINGS["inline"]["Show"], alert=True)