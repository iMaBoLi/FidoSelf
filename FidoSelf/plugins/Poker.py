from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Poker",
    "Pluginfo": {
        "Help": "To Setting Send Poker Sticker To Pokers!",
        "Commands": {
            "{CMD}Poker <On-Off>": None,
            "{CMD}PokerAll <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "pokerall": "**The Poker Mode Has Been {}!**",
    "pokerchat": "**The Poker Mode For This Chat Has Been {}!**",
}

@client.Command(command="Poker (On|Off)")
async def pokerchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    acChats = client.DB.get_key("POKER_CHATS") or []
    chatid = event.chat_id
    if change == "on":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("POKER_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("POKER_CHATS", acChats)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["pokerchat"].format(ShowChange))

@client.Command(command="PokerAll (On|Off)")
async def pokerall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("POKER_ALL", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["pokerall"].format(ShowChange))
 
@client.Command(onlysudo=False, alowedits=False)
async def poker(event):
    if event.is_sudo or event.is_bot or not event.text or "😐" not in event.text: return
    pomode = client.DB.get_key("POKER_ALL") or "off"
    pochats = client.DB.get_key("POKER_CHATS") or []
    if pomode == "on" or event.chat_id in pochats:
        await event.reply("😐")