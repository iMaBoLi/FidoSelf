from self import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetStr (.*)$")
async def messagesstarter(event):
    await event.edit(f"**{client.str} Processing . . .**")
    string = event.pattern_match.group(1)
    client.DB.set_key("MESSAGES_STARTER", str(string))
    client.str = str(string)
    await event.edit(f"**{client.str} The Messages Starter String Has Been Set To {string}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetCmd (.*)$")
async def cmdmessage(event):
    await event.edit(f"**{client.str} Processing . . .**")
    cmd = event.pattern_match.group(1)
    client.DB.set_key("SELF_CMD", str(cmd))
    client.cmd = str(cmd)
    await event.edit(f"**{client.str} The Self Commands Starter Has Been Set To {cmd}!**")

@client.Cmd(pattern=f"(?i)^.DelCmd$")
async def dcmdmessage(event):
    await event.edit(f"**{client.str} Processing . . .**")
    client.DB.del_key("SELF_CMD")
    client.cmd = "."
    await event.edit(f"**{client.str} The Self Commands Starter Has Been Deleted!**")
