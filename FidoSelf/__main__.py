from . import client, START_TIME
from FidoSelf.functions.utils import load_plugins, LOADED_PLUGS, NOT_LOADED_PLUGS
from FidoSelf.functions.misc import stimezone, addvars
import time

async def setup():
    await addvars()
    stimezone()
    load_plugins("FidoSelf/plugins")
    try:
        endtime = client.utils.convert_time(time.time() - START_TIME)
        send = await client.bot.send_message((client.realm or "TheaBoLi"), f"**👋 Fido Self Has Been Start Now !**\n\n**🧒 UserMode :** {client.mention(client.me)}\n**🤖 Manager :** {client.mention(client.bot.me)}\n\n__Took: {endtime}__")
        if LOADED_PLUGS:
            text = f"**✅ Loaded Plugins :**\n\n"
            for plug in LOADED_PLUGS:
                text += f"{client.str} `{plug}`\n"
            await send.reply(text)
        if NOT_LOADED_PLUGS:
            for plug in NOT_LOADED_PLUGS:
                text = f"**❌ Unloaded Plugin :**\n\n"
                text += f"{client.str} `{plug}` - ( `{NOT_LOADED_PLUGS[plug]}` )\n"
                await send.reply(text)
    except:
        pass

client.run_until_complete(setup())
client.bot.run_until_disconnected()
