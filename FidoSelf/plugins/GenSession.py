from FidoSelf import client
from telethon import TelegramClient, Button, events
from telethon.sessions import StringSession
from telethon.errors import (
    PhoneNumberInvalidError,
    PhoneNumberFloodError,
    PhoneNumberBannedError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)
import random
import re
import os
import time
import requests
import glob

bot = client.bot

@bot.on(events.NewMessage(pattern="(?i)\/GenerateSession", incoming=True, from_users=[client.me.id]))
async def createsession(event):
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**📱 Ok, Send Your Phone Number:**\n\n__• Ex: +19307777777 __")
        response = await conv.get_response(send.id)
        phone = response.text
    edit = await event.reply("`♻️ Please Wait . . .`")
    client = TelegramClient(StringSession(), 13367220, "52cdad8b941c04c0c85d28ed6b765825")
    await client.connect()
    try:
        scode = await client.send_code_request(phone, force_sms=False)
        async with bot.conversation(event.chat_id) as conv:
            send = await event.edit(f"**💠 Ok, Send Your Telegram Code For Your Phone:** ( `{phone}` )")
            response = await conv.get_response(send.id)
            phone_code = response.text
    except (PhoneNumberInvalidError, TypeError):
        return await event.edit("**❌ Your Phone Number Is Invalid!**")
    except PhoneNumberFloodError:
        return await event.edit("**❓ Your Phone Number Is Flooded!**")
    except PhoneNumberBannedError:
        return await event.edit("**🚫 Your Phone Number Is Banned!**")
    edit = await event.reply("`♻️ Please Wait . . .`")
    phone_code = phone_code.replace(" ", "")
    try:
        await client.sign_in(phone=phone, code=phone_code, password=None)
        session = client.session.save()
        await event.edit(f"**• String Session:**\n\n`{session}`")
        return await client.disconnect()
    except (PhoneCodeInvalidError, TypeError):
        return await event.edit("**❌ Your Code Is Invalid, Try Again!**")
    except PhoneCodeExpiredError:
        return await event.edit("**🚫 Your Code Is Expired, Try Again!**")
    except SessionPasswordNeededError:
        async with bot.conversation(event.chat_id) as conv:
            send = await event.edit(f"**🔐 Ok, Send Your Account 2Fa Password For Your Phone:** ( `{phone}` )")
            response = await conv.get_response(send.id)
            password = response.text
        edit = await event.reply("`♻️ Please Wait . . .`")
        try:
            await client.sign_in(password=password)
            session = client.session.save()
            await event.edit(f"**• String Session:**\n\n`{session}`")
            return await client.disconnect()
        except PasswordHashInvalidError:
            return await event.edit("**❌ Your Account Password Is Invalid, Try Again!**")
        except Exception as error:
            return await event.edit(error)
    except Exception as error:
        return await event.edit(error)
        
@bot.on(events.NewMessage(pattern="(?i)\/GenSession", incoming=True, from_users=[client.me.id]))
async def gensession(event):
    file = "Session.session"
    if os.path.exists(file):
        os.remove(file)
    async with bot.conversation(event.chat_id) as conv:
        send = await event.reply("**📱 Ok, Send Your Phone Number:**\n\n__• Ex: +19307777777 __")
        response = await conv.get_response(send.id)
        phone = response.text
    edit = await event.reply("`♻️ Please Wait . . .`")
    client = TelegramClient("Session", 13367220, "52cdad8b941c04c0c85d28ed6b765825")
    await client.connect()
    try:
        scode = await client.send_code_request(phone, force_sms=False)
        async with bot.conversation(event.chat_id) as conv:
            send = await event.edit(f"**💠 Ok, Send Your Telegram Code For Your Phone:** ( `{phone}` )")
            response = await conv.get_response(send.id)
            phone_code = response.text
    except (PhoneNumberInvalidError, TypeError):
        return await event.edit("**❌ Your Phone Number Is Invalid!**")
    except PhoneNumberFloodError:
        return await event.edit("**❓ Your Phone Number Is Flooded!**")
    except PhoneNumberBannedError:
        return await event.edit("**🚫 Your Phone Number Is Banned!**")
    edit = await event.reply("`♻️ Please Wait . . .`")
    phone_code = phone_code.replace(" ", "")
    try:
        await client.sign_in(phone=phone, code=phone_code, password=None)
        file = "Session.session"
        await edit.respond(file=file)
        return await client.disconnect()
    except (PhoneCodeInvalidError, TypeError):
        return await event.edit("**❌ Your Code Is Invalid, Try Again!**")
    except PhoneCodeExpiredError:
        return await event.edit("**🚫 Your Code Is Expired, Try Again!**")
    except SessionPasswordNeededError:
        async with bot.conversation(event.chat_id) as conv:
            send = await event.edit(f"**🔐 Ok, Send Your Account 2Fa Password For Your Phone:** ( `{phone}` )")
            response = await conv.get_response(send.id)
            password = response.text
        edit = await event.reply("`♻️ Please Wait . . .`")
        try:
            await client.sign_in(password=password)
            file = "Session.session"
            await edit.respond(file=file)
            return await client.disconnect()
        except PasswordHashInvalidError:
            return await event.edit("**❌ Your Account Password Is Invalid, Try Again!**")
        except Exception as error:
            return await event.edit(error)
    except Exception as error:
        return await event.edit(error)