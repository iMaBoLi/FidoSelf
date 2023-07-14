from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random
import os

__INFO__ = {
    "Category": "Manage",
    "Name": "Echo",
    "Info": {
        "Help": "To Setting Echo Users And Send User Messages!",
        "Commands": {
            "{CMD}AddEcho": {
                "Help": "To Add User On Echo List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelEcho": {
                "Help": "To Delete User From Echo List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}EchoList": {
                "Help": "To Getting Echo List",
            },
            "{CMD}CleanEchoList": {
                "Help": "To Clean Echo List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "where": "**{STR} Select You Want This Echo User To Be Saved For Where:**",
    "notall": "**{STR} e User ( {} ) Is Alredy In Echo List In {} Location!",
    "add": "**{STR} The User** ( {} ) **Is Added To Echo List For ( `{}` ) Location!**",
    "notin": "**{STR} The User** ( {} ) **Not In Echo Lis!**",
    "wheredel": "**{STR} Select You Want This Echo User To Be Deleted From Where:**",
    "del": "**{STR} The User** ( {} ) **From Echo List For Location** ( `{}` ) **Has Been Deleted!**",
    "esleep": "**{STR} The Echo Sleep Was Set To** ( `{}` )",
    "empty": "**{STR} The Echo List Is Empty!**",
    "list": "**{STR} The Echo List:**\n\n",
    "aempty": "**{STR} The Echo List Is Already Empty!**",
    "clean": "**{STR} The Echo List Is Cleaned!**",
    "close": "**{STR} The Echo Panel Successfuly Closed!**"
}
WHERES = ["All", "Groups", "Pvs", "Here"]

@client.Command(command="AddEcho", userid=True)
async def addecho(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"addecho:{chatid}:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="DelEcho", userid=True)
async def delecho(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    Echos = client.DB.get_key("ECHO_USERS") or {}
    if event.userid not in Echos:
        uinfo = await client.get_entity(event.userid)
        mention = client.functions.mention(uinfo)
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))
    res = await client.inline_query(client.bot.me.username, f"delecho:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="EchoList")
async def echolist(event):
    await event.edit(client.STRINGS["wait"])
    Echos = client.DB.get_key("ECHO_USERS") or {}
    if not Echos:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, echo in enumerate(Echos):
        text += f"**{row + 1}-** `{echo}` \n"
    await event.edit(text)

@client.Command(command="CleanEchoList")
async def cleanechos(event):
    await event.edit(client.STRINGS["wait"])
    echos = client.DB.get_key("ECHO_USERS") or []
    if not echos:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("ECHO_USERS")
    await event.edit(client.getstrings(STRINGS)["clean"])

@client.Command(command="SetEchoSleep (\d*)")
async def setechosleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = event.pattern_match.group(1)
    client.DB.set_key("ECHO_SLEEP", sleep)
    await event.edit(client.getstrings(STRINGS)["esleep"].format(client.functions.convert_time(int(sleep))))

@client.Command(onlysudo=False, allowedits=False)
async def echofosh(event):
    if event.is_ch: return
    userid = event.sender_id
    Echos = client.DB.get_key("ECHO_USERS") or {}
    if userid not in Echos: return
    sleep = client.DB.get_key("ECHO_SLEEP") or 0
    if ("All" in Echos[userid]) or ("Groups" in Echos[userid] and event.is_group) or ("Pvs" in Echos[userid] and event.is_private) or (str(event.chat_id) in Echos[userid]):
        await asyncio.sleep(int(sleep))
        getmsg = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(getmsg)

@client.Inline(pattern="addecho\:(.*)\:(.*)")
async def inlineecho(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = client.getstrings(STRINGS)["where"]
    buttons = []
    for where in WHERES:
        swhere = where if where != "Here" else chatid
        buttons.append(Button.inline(f"• {where} •", data=f"addecho:{chatid}:{userid}:{swhere}"))
    buttons = list(client.functions.chunks(buttons, 4))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closeecho")])
    await event.answer([event.builder.article("FidoSelf - Echo", text=text, buttons=buttons)])

@client.Callback(data="addecho\:(.*)\:(.*)\:(.*)")
async def addechos(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    where = event.data_match.group(3).decode('utf-8')
    userinfo = await client.get_entity(userid)
    Echos = client.DB.get_key("ECHO_USERS") or {}
    if userid not in Echos:
        Echos.update({userid: []})
    if where in Echos[userid]:
        text = client.getstrings(STRINGS)["notall"].format(userinfo.first_name, where)
        return await event.answer(text, alert=True)
    Echos[userid].append(where)
    client.DB.set_key("ECHO_USERS", Echos)
    text = client.getstrings(STRINGS)["add"].format(client.functions.mention(userinfo), where)
    await event.edit(text=text)

@client.Inline(pattern="delecho\:(.*)")
async def delechoinline(event):
    userid = int(event.pattern_match.group(1))
    text = client.getstrings(STRINGS)["wheredel"]
    Echos = client.DB.get_key("ECHO_USERS") or {}
    buttons = []
    for where in Echos[userid]:
        buttons.append(Button.inline(f"• {where} •", data=f"delechodel:{userid}:{where}"))
    await event.answer([event.builder.article("FidoSelf - Del Echo", text=text, buttons=buttons)])

@client.Callback(data="delechodel\:(.*)\:(.*)")
async def delechos(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    where = str(event.data_match.group(2).decode('utf-8'))
    Echos = client.DB.get_key("ECHO_USERS") or {}
    uinfo = await client.get_entity(userid)
    mention = client.functions.mention(uinfo)
    Echos[userid].remove(where)
    if not Echos[userid]:
        del Echos[userid]
    client.DB.set_key("ECHO_USERS", Echos)
    text = client.getstrings(STRINGS)["del"].format(mention, where)
    await event.edit(text=text)

@client.Callback(data="closeecho")
async def closeecho(event):
    await event.edit(text=client.getstrings(STRINGS)["close"])