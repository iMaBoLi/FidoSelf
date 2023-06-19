from FidoSelf import client
from telethon import events, types
from traceback import format_exc
import re
import time

def Command(
    pattern=None,
    command=None,
    onlysudo=True,
    alowedits=True,
    **kwargs,
):
    if command and not pattern:
        pattern = f"(?i)^\.{command}$"
        
    if pattern and pattern not in client.COMMANDS:
        client.COMMANDS.append(pattern)

    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                chat = await event.get_chat()
                if onlysudo and not event.is_sudo and (event.is_ch and not (chat.creator or chat.admin_rights)): return
                event.reply_message = await event.get_reply_message()
                event.is_bot = False
                sender = await event.get_sender()
                if not isinstance(sender, types.User) or sender.bot:
                    event.is_bot = True
                event.is_black = False
                blacks = client.DB.get_key("BLACKS") or []
                if event.sender_id in blacks:
                    event.is_black = True
                if not event.is_sudo and event.is_black: return
                event.is_white = False
                whites = client.DB.get_key("WHITES") or []
                if event.sender_id in whites:
                    event.is_white = True
                if event.via_bot_id: return
                await func(event)
            except:
                client.LOGS.error(format_exc())
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if alowedits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator