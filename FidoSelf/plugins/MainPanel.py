from FidoSelf import client
from telethon import Button
from datetime import datetime
from FidoSelf.plugins.ManageTime import FONTS, create_font

PAGES_COUNT = 2

def get_time_buttons(page):
    newtime = datetime.now().strftime("%H:%M")
    last = client.DB.get_key("TIME_FONT")
    buttons = []
    buttons.append([Button.inline("• Random •", data="setfonttime:{page}:random"), Button.inline(("✔️|Active" if last == "random" else "✖️|DeActive"), data="setfonttime:{page}:random")])
    buttons.append([Button.inline("• Random 2 •", data="setfonttime:{page}:random2"), Button.inline(("✔️|Active" if last == "random2" else "✖️|DeActive"), data="setfonttime:{page}:random2")])
    for font in FONTS:
        buttons.append([Button.inline(f"• {create_font(newtime, font)} •", data=f"setfonttime:{page}:{font}"), Button.inline(("✔️|Active" if font == last else "✖️|DeActive"), data=f"setfonttime:{page}:{font}")])
    pgbts = []
    if page > 1:
        pgbts.append(Button.inline("◀️ Back", data=f"panelpage:{page-1}"))
    if page < PAGES_COUNT:
        pgbts.append(Button.inline("Next ▶️", data=f"panelpage:{page+1}"))
    pgbts.append(Button.inline("🚫 Close 🚫", data="closepanel"))
    buttons.append(pgbts)
    return buttons

def get_mode_buttons(page):
    buttons = []
    MODES = {
        "SELF_ALL_MODE": "Self Mode",
        "QUICKS_MODE": "Quicks",
        "NAME_MODE": "Name",
        "BIO_MODE": "Bio",
        "PHOTO_MODE": "Photo",
        "SMART_MONSHI_MODE": "Smart Monshi",
        "OFFLINE_MONSHI_MODE": "Offline Monshi",
        "TIMER_MODE": "Timer Save",
    }
    for mode in MODES: 
        gmode = client.DB.get_key(mode) or "off"
        cmode = "on" if gmode == "off" else "off"
        buttons.append([Button.inline(f"• {MODES[mode]} •", data=f"setmode:{page}:{mode}:{cmode}"), Button.inline(("✔️|Active" if gmode == "on" else "✖️|DeActive"), data=f"setmode:{page}:{mode}:cmode")])
    pgbts = []
    if page > 1:
        pgbts.append(Button.inline("◀️ Back", data=f"panelpage:{page-1}"))
    if page < PAGES_COUNT:
        pgbts.append(Button.inline("Next ▶️", data=f"panelpage:{page+1}"))
    pgbts.append(Button.inline("🚫 Close 🚫", data="closepanel"))
    buttons.append(pgbts)
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}Panel$")
async def addecho(event):
    await event.edit(f"**{client.str} Processing . . .**")
    res = await client.inline_query(client.bot.me.username, "selfmainpanel")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="selfmainpanel")
async def inlinepanel(event):
    text = f"**{client.str} Please Use The Buttons Below To Control The Different Parts:**\n\n"
    buttons = get_mode_buttons(1)
    await event.answer([event.builder.article(f"{client.str} Smart Self - Panel", text=text, buttons=buttons)])

@client.Callback(data="panelpage\:(.*)")
async def panelpages(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    if page == 1:
        text = f"**{client.str} Please Use The Buttons Below To Control The Different Parts:**\n\n"
        buttons = get_mode_buttons(page)
        await event.edit(text=text, buttons=buttons)
    elif page == 2:
        text = f"**{client.str} Please Use The Options Below To Select The Font You Want To Use In Time Name And Bio:**"
        buttons = get_time_buttons(page)
        await event.edit(text=text, buttons=buttons)

@client.Callback(data="setfonttime\:(.*)\:(.*)")
async def setfonttime(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    font = event.data_match.group(2).decode('utf-8')
    client.DB.set_key("TIME_FONT", font)
    buttons = get_time_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="setmode\:(.*)\:(.*)\:(.*)")
async def setmode(event):
    page = int(event.data_match.group(1).decode('utf-8'))
    mode = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    client.DB.set_key(mode, change)
    buttons = get_mode_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="closepanel")
async def closepanel(event):
    await event.edit(text=f"**{client.str} The Panel Successfuly Closed!**")
