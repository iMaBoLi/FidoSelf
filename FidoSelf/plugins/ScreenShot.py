from FidoSelf import client
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Screen Shot",
    "Info": {
        "Help": "To Take Screen Shot From Sites!",
        "Commands": {
            "{CMD}SShot <URL>": {
                "Help": "To Get Screen Shot",
                "Input": {
                    "<URL>": "Url Of Site",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "invlink": "**{STR} The Site Link** ( `{}` ) **Is Invalid!**",
    "taked": "**{STR} The Screen Shot From Site** ( `{}` ) **Has Been Taked!**"
}

TOKEN = "SY1196W-HN84TCJ-G8J41WK-4B17FNK"

@client.Command(command="SShot (.*)")
async def screenshot(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    sitelink = event.pattern_match.group(1)
    url = f"https://shot.screenshotapi.net/screenshot?token={TOKEN}&url={sitelink}&full_page=true"
    result = await client.functions.request(url, re_json=True)
    if "error" in result:
        return await edit.edit(client.getstrings(STRINGS)["invlink"].format(sitelink))
    content = await client.functions.request(result["screenshot"], re_content=True)
    screenshot = client.PATH + "ScreenShot.png"
    with open(screenshot, "wb") as file:
        file.write(content)
    caption = client.getstrings(STRINGS)["taked"].format(sitelink)
    await client.send_file(event.chat_id, screenshot, caption=caption, force_document=True)
    os.remove(screenshot)
    await edit.delete()