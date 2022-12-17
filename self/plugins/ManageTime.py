from self import client
from telethon import functions, types
from PIL import Image, ImageDraw, ImageFont, ImageColor
from datetime import datetime
import aiocron
import random
import os
import requests

FONTS = {
     1: "0123456789",
     2: "０１２３４５６７８９",
     3: "⓿➊➋➌➍➎➏➐➑➒",
     4: "⓪①②③④⑤⑥⑦⑧⑨",
     5: "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
     6: "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
     7: "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
     8: "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
     9: "₀₁₂₃₄₅₆₇₈₉",
     10: "⁰¹²³⁴⁵⁶⁷⁸⁹",
     11: "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
}
TIMER = {
    1:{
        1: "🕐",
        2: "🕑",
        3: "🕒",
        4: "🕓",
        5: "🕔",
        6: "🕕",
        7: "🕖",
        8: "🕗",
        9: "🕘",
        10: "🕙",
        11: "🕚",
        12: "🕛"
    },
    2:{
        1: "🕜",
        2: "🕝",
        3: "🕞",
        4: "🕟",
        5: "🕠",
        6: "🕡",
        7: "🕢",
        8: "🕣",
        9: "🕤",
        10: "🕥",
        11: "🕦",
        12: "🕧"
    }
}
HEARTS = ["❤️", "💙", "💛", "💚", "🧡", "💜", "🖤", "🤍", "❣", "💕", "💞", "💔", "💗", "💖"]

COLORS = ["black", "white", "blue", "red", "yellow", "green", "purple", "orange", "brown", "pink", "gold", "fuchsia", "lime", "aqua", "skyblue", "gray"]

def create_font(newtime, font):
    for par in newtime:
        if par != ":":
            newtime = newtime.replace(par, FONTS[int(font)][int(par)])
    return newtime

@aiocron.crontab("*/1 * * * *")
async def changer():
    NAMES = client.DB.get_key("NAMES") or []
    BIOS = client.DB.get_key("BIOS") or []
    timefont = client.DB.get_key("TIME_FONT") or 1
    if str(timefont) == "random":
        timefont = random.randint(1, len(FONTS))
    newtime = datetime.now().strftime("%H:%M")
    hours = newtime.split(":")[0]
    mins = newtime.split(":")[1]
    gtimer = hours
    if int(hours) > 12:
        gtimer = int(hours) - 12
    elif hours.startswith("0"):
        gtimer = hours[1:]
    if int(hours) == 0:
        gtimer = 12
    timer = TIMER[2][int(gtimer)] if int(mins) > 29 else TIMER[1][int(gtimer)]
    time = create_font(newtime, timefont)
    hours = create_font(hours, timefont)
    mins = create_font(mins, timefont)
    dateen = datetime.now().strftime("%F").replace("-", "/")
    datefa = client.DB.get_key("DATE_FA") or "-"
    if datefa == "-" or newtime == "00:00":
        datefa = (requests.get("http://api.codebazan.ir/time-date/?json=en").json())["result"]["date"]
        client.DB.set_key("DATE_FA", datefa)
    wname = datetime.now().strftime("%A")
    if client.DB.get_key("NAME_MODE") and client.DB.get_key("NAME_MODE") == "on" and NAMES:
        chname = random.choice(NAMES)
        chname = chname.format(TIME=time, HEART=random.choice(HEARTS), TIMER=timer, HOURS=hours, MINS=mins, DATEEN=dateen, DATEFA=datefa, WEEK=wname)
        try:
            await client(functions.account.UpdateProfileRequest(first_name=str(chname)))
        except:
            await client(functions.account.UpdateProfileRequest(first_name="‌", last_name=str(chname)))
    if client.DB.get_key("BIO_MODE") and client.DB.get_key("BIO_MODE") == "on" and BIOS:
        chbio = random.choice(BIOS)
        chbio = chbio.format(TIME=time, HEART=random.choice(HEARTS), TIMER=timer, HOURS=hours, MINS=mins, DATEEN=dateen, DATEFA=datefa, WEEK=wname)
        await client(functions.account.UpdateProfileRequest(about=str(chbio)))
    PHOTOS = client.DB.get_key("PHOTOS") or {}
    TEXTS = client.DB.get_key("TEXT_TIMES") or []
    if client.DB.get_key("PHOTO_MODE") and client.DB.get_key("PHOTO_MODE") == "on" and PHOTOS and TEXTS:
        phname, _ = random.choice(list(PHOTOS.items()))
        info = PHOTOS[phname] 
        photo = client.path + "pics/" + phname
        TEXT = random.choice(TEXTS)
        TEXT = TEXT.format(TIME=newtime, HOURS=hours, MINS=mins, DATEEN=dateen, DATEFA=datefa, WEEK=wname)
        sizes = {"vsmall":20, "small":35, "medium":50, "big":70, "vbig":90}
        size = sizes[info["size"]]
        color = info["color"]
        if color == "random":
            color = random.choice(COLORS)
        color = ImageColor.getrgb(color)
        img = Image.open(photo)
        width, height = img.size
        img.resize((640,640))
        ffont = info["font"]
        if ffont == "random":
            ffont = random.choice(os.listdir(client.path + "fonts/"))
        font = ImageFont.truetype(client.path + "fonts/" + ffont, size)
        draw = ImageDraw.Draw(img)
        twidth, theight = draw.textsize(TEXT, font=font)
        newwidth, newheight = (width - twidth) / 2, (height - theight) /2
        if info["where"] == "↖️":
            newwidth, newheight = 20, 20
        elif info["where"] == "⬆️":
            newwidth, newheight = (width - twidth) / 2, 20
        elif info["where"] == "↗️":
            newwidth, newheight = (width - twidth) - 20, 20
        elif info["where"] == "⬅️":
            newwidth, newheight = 20, (height - theight) /2
        elif info["where"] == "➡️":
            newwidth, newheight = (width - twidth) - 20, (height - theight) /2
        elif info["where"] == "↙️":
            newwidth, newheight = 20, (height - theight) - 20
        elif info["where"] == "⬇️":
            newwidth, newheight = (width - twidth) / 2, (height - theight) - 20
        elif info["where"] == "↘️":
            newwidth, newheight = (width - twidth) - 20, (height - theight) - 20
        draw.text((newwidth, newheight), TEXT, color, font=font)
        img.save(client.path + "NEWPROFILE.png")
        file = await client.upload_file(client.path + "NEWPROFILE.png")
        pphoto = (await client.get_profile_photos("me"))[0]
        await client(functions.photos.DeletePhotosRequest(id=[types.InputPhoto(id=pphoto.id, access_hash=pphoto.access_hash, file_reference=pphoto.file_reference)]))
        await client(functions.photos.UploadProfilePhotoRequest(file=file))
        os.remove(client.path + "NEWPROFILE.png")

changer.start()
