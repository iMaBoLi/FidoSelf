from FidoSelf import client
from telethon import events
from traceback import format_exc

def Inline(
    pattern=None,
    onlysudo=True,
    **kwargs,
):
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                sudolist = client.DB.get_key("SUDO_USERS") or []
                if onlysudo and not (event.is_sudo or event.sender_id in sudolist):
                    text = client.STRINGS["OtherInline"]
                    return await event.answer([event.builder.article("FidoSelf - NotForYou", text=text)])
                await func(event)
            except:
                client.LOGS.error(format_exc())
        client.bot.add_event_handler(wrapper, events.InlineQuery(pattern=pattern, **kwargs))
        return wrapper
    return decorator
