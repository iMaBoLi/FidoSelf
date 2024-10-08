from FidoSelf import client
from googletrans import Translator, LANGUAGES

__INFO__ = {
    "Category": "Tools",
    "Name": "Translate",
    "Info": {
        "Help": "To Translate Your Texts!",
        "Commands": {
            "{CMD}STr <Lang>": {
                "Help": "To Translate Text",
                "Input": {
                    "<Lang>": "Tranlate Language",
                },
                "Reply": ["Text"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "EN": {
        "notlang": "**{STR} The Language** ( `{}` ) **Is Not Available!**",
        "translate": "**{STR} Translated From** ( `{}` ) **To** ( `{}` ):\n\n`{}`"
    },
    "FA": {
        "notlang": "**{STR} زبان مورد نظر** ( `{}` ) **موجود نمی باشد!**",
        "translate": "**{STR} با موفقیت از** ( `{}` ) **به** ( `{}` ) **ترجمه شد!**\n\n`{}`"
    },
}

@client.Command(command="Str (.*)")
async def translattext(event):
    await event.edit(client.STRINGS["wait"])
    dest = event.pattern_match.group(1).lower()
    if not event.reply_message or not event.reply_message.raw_text:
        return await event.edit(client.STRINGS["replytext"])
    text = event.reply_message.raw_text
    if dest not in LANGUAGES:
        return await event.edit(client.getstring(STRINGS, "notlang").format(dest))
    translator = Translator()
    trjome = translator.translate(text, dest=dest)
    await event.edit(client.getstring(STRINGS, "translate").format(trjome.src, dest, trjome.text))