from FidoSelf import client
from telethon import functions, types
import time
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Video Shot",
    "Info": {
        "Help": "To Take Screen Shot From Your Videos!",
        "Commands": {
            "{CMD}VShot <Time>": {
                 "Help": "To Take Shot From Time",
                "Input": {
                    "<Time>" : "Time For Take",
                },
                "Reply": ["Video"],
            },
            "{CMD}VShot -<Count>": {
                 "Help": "To Take Multi Shots",
                "Input": {
                    "<Count>" : "Count Of Shots",
                },
                "Reply": ["Video"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "taking": "**{STR} Taking** ( `{}` ) **Screen Shot From Your Video ...**",
    "taked": "**{STR} Taked** ( `{}` ) **Screen Shot From Your Video ...**",
    "sending": "**{STR} Sending** ( `{}` ) **Screen Shots ...**",
    "sended": "**{STR} Taked** ( `{}` ) **Screen Shot From Your Video!**",
    "takingdur": "**{STR} Taking Screen Shot From Duration** ( `{}` ) **From Your Video ...**",
    "takeddur": "**{STR} Taked Screen Shot From Duration** ( `{}` ) **From Your Video!**"
}

@client.Command(command="VShot ((\-)?\d*)")
async def videoshot(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    data = event.pattern_match.group(1)
    if reply:= event.checkReply(["Video"]):
        return await edit.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await edit.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    duration = event.reply_message.file.duration
    if str(data).startswith("-"):
        count = int(data.replace("-", ""))
        newdur = duration / count
        if newdur < 1:
            newdur = 1
            count = duration
        files = []
        lastdur = 0
        await edit.edit(client.getstrings(STRINGS)["taking"].format(count))
        for con in range(count):
            out = client.PATH + f"Shot-{con}.jpg"
            cmd = f"ffmpeg -i {file} -ss {lastdur} -vframes 1 {out}"
            await client.functions.runcmd(cmd)
            files.append(out)
            lastdur += newdur
            if con == 0 or ((con + 1) % 3) == 0:
                await edit.edit(client.getstrings(STRINGS)["taked"].format(con + 1))
        await edit.edit(client.getstrings(STRINGS)["sending"].format(count))
        caption = client.getstrings(STRINGS)["sended"].format(count)
        for shots in list(client.functions.chunks(files, 9)):
            await client.send_file(event.chat_id, shots, caption=caption)
        os.remove(file)
        for file in files:
            os.remove(file)
        await event.delete()
    else:
        if int(data) > duration:
            data = duration - 1
        await edit.edit(client.getstrings(STRINGS)["takingdur"].format(data))
        out = client.PATH + f"Shot-{data}.jpg"
        cmd = f"ffmpeg -i {file} -ss {int(data)} -vframes 1 {out}"
        await client.functions.runcmd(cmd)
        caption = client.getstrings(STRINGS)["takeddur"].format(str(data))
        await client.send_file(event.chat_id, out, caption=caption)
        os.remove(file)
        os.remove(out)
        await event.delete()