from FidoSelf import client
from telethon import functions, Button
import asyncio

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Manage",
    "Pluginfo": {
        "Help": "To Get Inline Manage Panel For User!",
        "Commands": {
            "{CMD}Manage <UserId|Username|Pv>": None,,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "Manages": {
        "INFO": "User Info",
        "BLOCK": "Block",
        "UNBLOCK": "UnBlock",
        "WHITES": "White",
        "BLACKS": "Black",
        "ECHOS": "Echo",
    },
    "menu": "**Please Use The Options Below To Manage User Modes:**",
    "close": "**The Manage Panel Successfuly Closed!**",
    "infouser": "**User Info:**\n\n**Mention:** ( {} )\n**ID:** ( `{}` )\n**First Name:** ( `{}` )\n**Last Name:** ( `{}` )\n**Username :** ( `{}` )\n**Contact:** ( `{}` )\n**Mutual Contact:** ( `{}` )\n**Status:** ( `{}` )\n**Common Chats:** ( `{}` )\n**Bio:** ( `{}` )",
}

async def get_manage_buttons(userid, chatid):
    buttons = []
    MANAGES = STRINGS["Manages"]
    buttons.append([Button.inline(f'• {MANAGES["INFO"]} •', data=f"getinfo:{chatid}:{userid}")])
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    smode = MANAGES["UNBLOCK"] if info.blocked else MANAGES["BLOCK"]
    cmode = "unblock" if info.blocked else "block"
    buttons.append([Button.inline(f"• {smode} •", data=f"{cmode}:{chatid}:{userid}")])
    obuts = []
    for manage in ["BLACKS", "WHITES", "ECHOS"]:
        lists = client.DB.get_key(manage) or []
        smode = "( ✔️ )" if userid in lists else "( ✖️ )"
        cmode = "del" if userid in lists else "add"
        obuts.append(Button.inline(f"• {MANAGES[manage]} - {smode} •", data=f"setuser:{chatid}:{userid}:{manage}:{cmode}"))
    obuts = list(client.functions.chunks(obuts, 2))
    for but in obuts:
        buttons.append(but)
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closemanage")])
    return buttons

@client.Command(command="Manage ?(.*)?")
async def managepanel(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"managepanel:{chatid}:{userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="managepanel\:(.*)\:(.*)")
async def inlinemanagepanel(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = STRINGS["menu"]
    buttons = await get_manage_buttons(userid, chatid)
    await event.answer([event.builder.article("FidoSelf - Manage", text=text, buttons=buttons)])

@client.Callback(data="setuser\:(.*)\:(.*)\:(.*)\:(.*)")
async def setusermanage(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    mode = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    info = await client.get_entity(userid)
    lists = client.DB.get_key(mode) or []
    if change == "add":
        lists.append(userid)
        client.DB.set_key(mode, lists)
    elif change == "del":
        lists.remove(userid)
        client.DB.set_key(mode, lists)
    buttons = await get_manage_buttons(userid, chatid)
    await event.edit(buttons=buttons)

@client.Callback(data="(block|unblock)\:(.*)\:(.*)")
async def closemanagepanel(event):
    change = str(event.data_match.group(1).decode('utf-8'))
    chatid = int(event.data_match.group(2).decode('utf-8'))
    userid = int(event.data_match.group(3).decode('utf-8'))
    if change == "block":
        await client(functions.contacts.BlockRequest(userid))
    elif change == "unblock":
        await client(functions.contacts.UnblockRequest(userid))
    await asyncio.sleep(0.3)
    buttons = await get_manage_buttons(userid, chatid)    
    await event.edit(buttons=buttons)

@client.Callback(data="getinfo\:(.*)\:(.*)")
async def getinfo(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    uinfo = await client.get_entity(userid)
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = STRINGS["infouser"].format(client.mention(uinfo), uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await client.send_file(chatid, info.profile_photo, caption=userinfo)
    else:
        await client.send_message(chatid, userinfo)
    buttons = await get_manage_buttons(userid, chatid)    
    await event.edit(buttons=buttons)

@client.Callback(data="closemanage")
async def closemanagepanel(event):
    text = STRINGS["close"]
    await event.edit(text=text)