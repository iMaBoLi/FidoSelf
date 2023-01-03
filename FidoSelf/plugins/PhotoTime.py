from FidoSelf import client
from telethon import Button
from FidoSelf.functions.vars import COLORS
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}Photo (On|Off)$")
async def photo(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("PHOTO_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(f"**{client.str} The Photo Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddPhoto (.*)$")
async def addphoto(event):
    await event.edit(client.get_string("Wait"))
    if not event.reply_message or not event.reply_message.photo:
        return await event.edit(f"**{client.str} Please Reply To Photo!**")
    phname = str(event.pattern_match.group(1))
    phname = phname + ".png"
    photos = client.DB.get_key("PHOTOS") or {}
    if phname in photos:
        return await event.edit(f"**{client.str} The Photo Name** ( `{phname}` ) **Already In Photo List!**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    photos.update({phname: {"chat_id": client.backch, "msg_id": forward.id}})
    client.DB.set_key("PHOTOS", photos)
    res = await client.inline_query(client.bot.me.username, f"addphoto:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelPhoto (.*)$")
async def delphoto(event):
    await event.edit(client.get_string("Wait"))
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(f"**{client.str} The Photo** ( `{phname}` ) **Not In Photo List!**")
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(f"**{client.str} The Photo** ( `{phname}` ) **Deleted From Photo List!**")  

@client.Cmd(pattern=f"(?i)^\{client.cmd}GetPhoto (.*)$")
async def getphoto(event):
    await event.edit(client.get_string("Wait"))
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(f"**{client.str} The Photo** ( `{phname}` ) **Not In Photo List!**")
    photo = photos[phname]
    get = await client.get_messages(photo["chat_id"], ids=int(photo["msg_id"]))
    fphoto = await get.download_media()
    await event.respond(f"""**{client.str} Photo Name:** ( `{phname}` )\n**{client.str} Where:** ( `{photo["where"]}` )\n**{client.str} Size:** ( `{photo["size"].title()}` )\n**{client.str} Color:** ( `{photo["color"].title()}` )\n**{client.str} Font:** ( `{photo["font"].title()}` )\n**{client.str} Align:** ( `{photo["align"].title()}` )""", file=fphoto)
    await event.delete()
    os.remove(fphoto)

@client.Cmd(pattern=f"(?i)^\{client.cmd}PhotoList$")
async def photolist(event):
    await event.edit(client.get_string("Wait"))
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(f"**{client.str} The Photo List Is Empty!**")
    text = f"**{client.str} The Photo List:**\n\n"
    row = 1
    for photo in photos:
        text += f"**{row} -** `{photo}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanPhotoList$")
async def cleanphotos(event):
    await event.edit(client.get_string("Wait"))
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(f"**{client.str} The Photo List Is Already Empty!**")
    client.DB.del_key("PHOTOS")
    await event.edit(f"**{client.str} The Photo List Is Cleared!**")

@client.Inline(pattern="addphoto\:(.*)")
async def addphoto(event):
    phname = str(event.pattern_match.group(1))
    text = f"**{client.str} Please Choose Where Should Be Write Text On Photo:**"
    buttons = []
    for where in ["↖️", "⬆️", "↗️", "⬅️", "⏺", "➡️", "↙️", "⬇️", "↘️"]:
        buttons.append(Button.inline(f"• {where} •", data=f"sizephoto:{phname}:{where}"))
    buttons = list(client.utils.chunks(buttons, 3))
    buttons.append([Button.inline("🚫 Close 🚫", data=f"photoclose:{phname}")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Photo", text=text, buttons=buttons)])

@client.Callback(data="(.*)photo\:(.*)")
async def photo(event):
    work = str(event.data_match.group(1).decode('utf-8'))
    data = (str(event.data_match.group(2).decode('utf-8'))).split(":")
    photos = client.DB.get_key("PHOTOS") or {}
    phname = data[0]
    where = data[1]
    if work == "size":
        text = f"**{client.str} Please Choose Size Of The Text Time:**"
        buttons = [[Button.inline("• Very Small •", data=f"colorphoto:{phname}:{where}:vsmall"), Button.inline("• Small •", data=f"colorphoto:{phname}:{where}:small")], [Button.inline("• Medium •", data=f"colorphoto:{phname}:{where}:medium")], [Button.inline("• Big •", data=f"colorphoto:{phname}:{where}:big"), Button.inline("• Very Big •", data=f"colorphoto:{phname}:{where}:vbig")]]
        buttons.append([Button.inline("🚫 Close 🚫", data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "color":
        size = data[2]
        text = f"**{client.str} Please Choose Color For Your Time Text:**"
        buttons = [[Button.inline("Random ♻️", data=f"fontphoto:{phname}:{where}:{size}:random")]]
        for color in COLORS:
            buttons.append(Button.inline(f"• {color.title()} •", data=f"fontphoto:{phname}:{where}:{size}:{color}"))
        buttons = [buttons[0]] + list(client.utils.chunks(buttons[1:], 4))
        buttons.append([Button.inline("🚫 Close 🚫", data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "font":
        size = data[2]
        color = data[3]
        text = f"**{client.str} Please Choose Font For Your Time Text:**"
        fonts = client.DB.get_key("FONTS")
        if len(fonts) == 0:
            return await event.answer(f"{client.str} Please Save A Font File First!", alert=True)
        buttons = [[Button.inline("Random ♻️", data=f"alignphoto:{phname}:{where}:{size}:{color}:random")]]
        for font in fonts:
            buttons.append(Button.inline(f"• {font.title()} •", data=f"alignphoto:{phname}:{where}:{size}:{color}:{font}"))
        buttons = [buttons[0]] + list(client.utils.chunks(buttons[1:], 2))
        buttons.append([Button.inline("🚫 Close 🚫", data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "align":
        size = data[2]
        color = data[3]
        font = data[4]
        text = f"**{client.str} Please Specify How To Align The Time Text On This Image:**"
        buttons = [[Button.inline("• Left •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}:left"), Button.inline("• Center •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}:center"), Button.inline("• Right •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}:right")]]
        buttons.append([Button.inline("🚫 Close 🚫", data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "complete":
        size = data[2]
        color = data[3]
        font = data[4]
        align = data[5]
        data = client.DB.get_key("PHOTOS")[phname]
        photos.update({phname: {"chat_id": data["chat_id"], "msg_id": data["msg_id"], "where": where,"size": size,"color": color,"font": font,"align": align}})
        client.DB.set_key("PHOTOS", photos)
        await event.edit(text=f"**{client.str} The New Photo Was Saved!**\n\n**{client.str} Photo Name:** ( `{phname}` )\n**{client.str} Where:** ( `{where}` )\n**{client.str} Size:** ( `{size.title()}` )\n**{client.str} Color:** ( `{color.title()}` )\n**{client.str} Font:** ( `{font.title()}` )\n**{client.str} Align:** ( `{align.title()}` )")

@client.Callback(data="photoclose\:(.*)")
async def closephoto(event):
    phname = str(event.data_match.group(1).decode('utf-8'))
    photos = client.DB.get_key("PHOTOS") or {}
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(text=f"**{client.str} The Photo Panel Successfuly Closed!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddFont (.*)$")
async def savefontfile(event):
    await event.edit(client.get_string("Wait"))
    fname = str(event.pattern_match.group(1))
    fonts = client.DB.get_key("FONTS") or {}
    if len(fonts) > 10:
        return await event.edit(f"**{client.str} Sorry, You Cannot Save More Than 10 Fonts!**")
    if not event.reply_message:
        return await event.edit(f"**{client.str} Please Reply To Font File!**")
    format = str(event.reply_message.media.document.attributes[0].file_name).split(".")[-1]
    if format != "ttf":
        return await event.edit(f"**{client.str} Please Reply To A Font File With .TTF Format!**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    fonts.update({fname + ".ttf": {"chat_id": client.backch, "msg_id": forward.id}})
    client.DB.set_key("FONTS", fonts)
    await event.edit(f"**{client.str} The Font File** ( `{fname}.ttf` ) **Has Been Saved!**")  

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelFont (.*)$")
async def delfontfile(event):
    await event.edit(client.get_string("Wait"))
    fname = str(event.pattern_match.group(1))
    fonts = client.DB.get_key("FONTS") or {}
    if fname not in fonts:
        return await event.edit(f"**{client.str} The Font** ( `{fname}` ) **Not In Fonts List!**")
    del fonts[fname]
    client.DB.set_key("FONTS", fonts)
    await event.edit(f"**{client.str} The Font File** ( `{fname}` ) **Has Been Deleted!**")  

@client.Cmd(pattern=f"(?i)^\{client.cmd}FontList$")
async def fontlist(event):
    await event.edit(client.get_string("Wait"))
    fonts = client.DB.get_key("FONTS") or {}
    if not fonts:
        return await event.edit(f"**{client.str} The Font File List Is Empty!**")
    text = f"**{client.str} The Font File List:**\n\n"
    row = 1
    for font in fonts:
        text += f"**{row} -** `{font}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanFontList$")
async def cleanfonts(event):
    await event.edit(client.get_string("Wait"))
    fonts = client.DB.get_key("FONTS") or {}
    if not fonts:
        return await event.edit(f"**{client.str} The Font File List Is Already Empty!**")
    client.DB.del_key("FONTS")
    await event.edit(f"**{client.str} The Font File List Is Cleared!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddTextTime ([\s\S]*)$")
async def addtexttime(event):
    await event.edit(client.get_string("Wait"))
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    newtexttime = str(event.pattern_match.group(1))
    if newtexttime in texttimes:
        return await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Already In Text Time List!**")  
    texttimes.append(newtexttime)
    client.DB.set_key("TEXT_TIMES", texttimes)
    await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Added To Text Time List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}DelTextTime ([\s\S]*)$")
async def deltexttime(event):
    await event.edit(client.get_string("Wait"))
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    newtexttime = str(event.pattern_match.group(1))
    if newtexttime not in texttimes:
        return await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Not In Text Time List!**")  
    texttimes.remove(newtexttime)
    client.DB.set_key("TEXT_TIMES", texttimes)
    await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Deleted From Text Time List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}TextTimeList$")
async def texttimelist(event):
    await event.edit(client.get_string("Wait"))
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    if not texttimes:
        return await event.edit(f"**{client.str} The Text Time List Is Empty!**")
    text = f"**{client.str} The Text Time List:**\n\n"
    row = 1
    for texttime in texttimes:
        text += f"**{row} -** `{texttime}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanTextTimeList$")
async def cleantexttimes(event):
    await event.edit(client.get_string("Wait"))
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    if not texttimes:
        return await event.edit(f"**{client.str} The Text Time List Is Already Empty!**")
    client.DB.del_key("TEXT_TIMES")
    await event.edit(f"**{client.str} The Text Time List Is Cleared!**")
