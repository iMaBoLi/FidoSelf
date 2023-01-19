from . import client, __version__
from telethon import __version__ as telever
from FidoSelf.functions import load_plugins
from FidoSelf.functions import addvars
import platform
import time

async def setup():
    client.LOGS.info("• Adding Coustom Vars To Client ...")
    await addvars()
    client.LOGS.info("• Installing Main Plugins ...")
    plugs, notplugs = load_plugins("FidoSelf/plugins")
    client.LOGS.info(f"• Successfully Installed {len(plugs)} Plugin From Main Plugins!")
    client.LOGS.info(f"• Not Installed {len(notplugs)} Plugin From Main Plugins!")
    try:
        send = await client.bot.send_message(client.realm, f"**👋 Fido Self Has Been Start Now !**\n\n**🧒 UserMode :** {client.mention(client.me)}\n**🤖 Manager :** {client.mention(client.bot.me)}\n\n__Took In: {endtime}__")
        if plugs:
            text = f"**✅ Loaded Plugins :**\n\n"
            for plug in plugs:
                text += f"`{plug}`\n"
            await send.reply(text)
        if notplugs:
            text = f"**❌ Unloaded Plugins :**\n\n"
            for plug in notplugs:
                text += f"`{plug}`\n"
            await send.reply(text)
        res = await client.utils.runcmd('git log --pretty=format:"[%an]: %s" -20')
    except:
        pass
    client.LOGS.info(f"• Python Version: {platform.python_version()}")
    client.LOGS.info(f"• Telethon Version: {telever}")
    client.LOGS.info(f"• FidoSelf Version: {__version__}")
    client.LOGS.info("\n----------------------------------------\n  • Starting FidoSelf Was Successful!\n----------------------------------------")

client.bot.loop.run_until_complete(setup())
client.run_until_disconnected()
