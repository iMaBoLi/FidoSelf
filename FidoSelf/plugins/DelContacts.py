from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Name": "Del Contacts",
    "Info": {
        "Help": "To Delete Your Account Contacts!",
        "Commands": {
            "{CMD}DelC <Name>": {
                "Help": "To Delete Contacts With Name",
                "Input": {
                    "<Name>": "Name Of Contact",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notdel": "**{STR} The Contact With Name** ( `{}` ) **Is Not Founded!**",
    "delcon": "**{STR} The** ( `{}` ) **Contact By Name** ( `{}` ) **From Contacts Was Deleted!**"
}

@client.Command(command="DelC (.*)")
async def delcontacts(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    contacts = await client(functions.contacts.GetContactsRequest(hash=0))
    count = 0
    for contact in contacts.users:
        if contact.first_name == name:
            await client(functions.contacts.DeleteContactsRequest(id=[contact.id]))
            count += 1
    if not count:
        return await event.edit(client.getstrings(STRINGS)["notdel"].format(name))
    await event.edit(client.getstrings(STRINGS)["delcon"].format(count, name))
