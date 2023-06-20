from FidoSelf import client
from FidoSelf.functions import convert_date
from datetime import datetime
import random

FONTS = {
    1: "0,1,2,3,4,5,6,7,8,9",
    2: "۰,۱,۲,۳,۴,۵,۶,۷,۸,۹",
    3: "０,１,２,３,４,５,６,７,８,９",
    4: "⓿,➊,➋,➌,➍,➎,➏,➐,➑,➒",
    5: "⓪,①,②,③,④,⑤,⑥,⑦,⑧,⑨",
    6: "𝟘,𝟙,𝟚,𝟛,𝟜,𝟝,𝟞,𝟟,𝟠,𝟡",
    7: "𝟬,𝟭,𝟮,𝟯,𝟰,𝟱,𝟲,𝟳,𝟴,𝟵",
    8: "𝟎,𝟏,𝟐,𝟑,𝟒,𝟓,𝟔,𝟕,𝟖,𝟗",
    9: "𝟢,𝟣,𝟤,𝟥,𝟦,𝟧,𝟨,𝟩,𝟪,𝟫",
    10: "₀,₁,₂,₃,₄,₅,₆,₇,₈,₉",
    11: "⁰,¹,²,³,⁴,⁵,⁶,⁷,⁸,⁹",
    12: "𝟶,𝟷,𝟸,𝟹,𝟺,𝟻,𝟼,𝟽,𝟾,𝟿",
    13: "⒪,⑴,⑵,⑶,⑷,⑸,⑹,⑺,⑻,⑼",
    14: "0҉,1҉,2҉,3҉,4҉,5҉,6҉,7҉,8҉,9҉",
}

HEARTS = ["❤️", "🩷", "🩵", "🩶", "💙", "💛", "💚", "🧡", "💜", "🖤", "🤍"]
COLORS = ["black", "white", "blue", "red", "yellow", "green", "purple", "orange", "brown", "pink", "gold", "fuchsia", "lime", "aqua", "skyblue", "gray"]

def create_font(newtime, timefont):
    newtime = str(newtime)
    if str(timefont) == "random2":
        for par in newtime:
            fonts = [1,3,4,5,6,7,8,9,10,11,12]
            rfont = random.choice(fonts)
            if par not in [":", "/"]:
                nfont = FONTS[int(rfont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
            fonts.remove(rfont)
    else:
        if str(timefont) == "random":
            fonts = list(range(1, len(FONTS)+2))
            timefont = random.choice(fonts)
        for par in newtime:
            if par not in [":", "/"]:
                nfont = FONTS[int(timefont)].split(",")[int(par)]
                newtime = newtime.replace(par, nfont)
    return newtime

async def get_vars(event):
    time = datetime.now()
    cdate = convert_date(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")))
    Vars = {
        "TIME": time.strftime("%H:%M"),
        "DATE": str(cdate[0]) + "/" + str(cdate[1]) + "/" + str(cdate[2]),
        "DAY": cdate[2],
        "MONTH": cdate[1],
        "YEAR": cdate[0],
        "HOUR": time.strftime("%H"),
        "MIN": time.strftime("%M"),
        "SEC": time.strftime("%S"),
     }
    timefont = client.DB.get_key("TIME_FONT") or 1
    NewVars = {}
    for Var in Vars:
        NewVars.update({"F" + str(Var): create_font(str(Vars[Var]), str(timefont))})
    Vars.update(NewVars)
    Vars.update({
        "STRDAY": time.strftime("%A"),
        "STRMONTH": time.strftime("%B"),
        })
    Vars.update({"HEART": random.choice(HEARTS)})
    if event:
        sender = await event.get_sender()
        if sender.to_dict()["_"] == "User":
            Vars.update({"FIRSTNAME": sender.first_name})
            Vars.update({"LASTNAME": sender.last_name})
            Vars.update({"USERNAME": sender.username})
        elif sender.to_dict()["_"] in ["Channel", "Group"]:
            Vars.update({"FIRSTNAME": sender.title})
            Vars.update({"USERNAME": sender.username})
        me = await event.client.get_me()
        Vars.update({"MYFIRSTNAME": me.first_name})
        Vars.update({"MYLASTNAME": me.last_name})
        Vars.update({"MYUSERNAME": me.username})
        if event.is_group:
            chat = await event.get_chat()
            Vars.update({"CHATTITLE": chat.title})
            Vars.update({"CHATUSERNAME": chat.username})
    return Vars

async def add_vars(text, event=None):
    Vars = await get_vars(event)
    for Var in Vars:
        text = text.replace("{" + str(Var) + "}", str(Vars[Var]))
    return text

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Variebels",
    "Pluginfo": {
        "Help": "To Use From This Variebels In Messages And Medias!",
        "Commands": {
            "{TIME}": None,
            "{DATE}": None,
            "{DAY}": None,
            "{MONTH}": None,
            "{YEAR}": None,
            "{HOUR}": None,
            "{MIN}": None,
            "{SEC}": None,
            "{FTIME}": None,
            "{FDATE}": None,
            "{FDAY}": None,
            "{FMONTH}": None,
            "{FYEAR}": None,
            "{FHOUR}": None,
            "{FMIN}": None,
            "{FSEC}": None,
            "{STRDAY}": None,
            "{STRMONTH}": None,
            "{HEART}": None,
            "{FIRSTNAME}": None,
            "{LASTNAME}": None,
            "{USERNAME}": None,
            "{MYFIRSTNAME}": None,
            "{MYLASTNAME}": None,
            "{MYUSERNAME}": None,
            "{CHATTITLE}": None,
            "{CHATUSERNAME}": None
        },
    },
}
client.functions.AddInfo(__INFO__)