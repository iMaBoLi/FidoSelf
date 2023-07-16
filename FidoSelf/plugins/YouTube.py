from FidoSelf import client
from telethon import functions, types, Button
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Youtube",
    "Info": {
        "Help": "To Download And Search On Youtube!",
        "Commands": {
            "{CMD}YtSearch <Text>": {
                "Help": "To Search On Youtube",
                "Input": {
                    "<Text>": "Query For Search",
                },
            },
            "{CMD}YtVideo <Link>": {
                "Help": "To Download Video",
                "Input": {
                    "<Link>": "Link Of Youtube",
                },
            },
            "{CMD}YtAudio <Link>": {
                "Help": "To Download Audio",
                "Input": {
                    "<Link>": "Link Of Youtube",
                },
            },
            "{CMD}YtInfo <Link>": {
                "Help": "To Get Video Info",
                "Input": {
                    "<Link>": "Link Of Youtube",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "linkinv": "**{STR} The Entered Youtube Link** ( `{}` ) **Is Invalid!**",
    "downvideo": "**{STR} Downloadig Video From Youtube ...**\n\n**{STR} Link:** ( `{}` )",
    "downaudio": "**{STR} Downloadig Audio From Youtube ...**\n\n**{STR} Link:** ( `{}` )",
    "caption": "**{STR} Title:** ( `{}` )\n**{STR} Uploader:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )\n**{STR} Size:** ( `{}` )\n**{STR} Duration:** ( `{}` )",
    "description": "**{STR} Description:** ( `{}` )",
    "searchclick": "**{STR} Click To Follow Button To Get Search Results For Query:** ( `{}` )",
    "searchinfo": "**{STR} Link:** ( {} )\n**{STR} Title:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Duration:** ( `{}` )",
}
    
@client.Command(command="Yt(Video|Audio) (.*)")
async def ytdownloader(event):
    await event.edit(client.STRINGS["wait"])
    downtype = event.pattern_match.group(1).title()
    link = event.pattern_match.group(2)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.getstrings(STRINGS)["linkinv"].format(link))
    if downtype == "Video":
        await event.edit(client.getstrings(STRINGS)["downvideo"].format(link))
        file, ytinfo = await client.functions.yt_video(link)
        attributes = [types.DocumentAttributeVideo(duration=ytinfo["duration"], w=720, h=720, supports_streaming=True)]
    if downtype == "Audio":
        await event.edit(client.getstrings(STRINGS)["downaudio"].format(link))
        file, ytinfo = await client.functions.yt_audio(link)
        attributes = [types.DocumentAttributeAudio(duration=ytinfo["duration"], voice=False, title=ytinfo["title"], performer=ytinfo["uploader"])]
    filesize = os.path.getsize(file["OUTFILE"])
    filesize = client.functions.convert_bytes(filesize)
    caption = client.getstrings(STRINGS)["caption"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["like_count"], ytinfo["comment_count"], filesize, ytinfo["duration_string"])
    callback = client.progress(event, upload=True)
    uploadfile = await client.fast_upload(file["OUTFILE"], progress_callback=callback)
    send = await client.send_file(event.chat_id, file=uploadfile, thumb=file["THUMBNAIL"], attributes=attributes, caption=caption)
    description = ytinfo["description"]
    description = client.getstrings(STRINGS)["description"].format(description)
    if len(description) < 4096:
        await send.reply(description)
    os.remove(file["OUTFILE"])
    os.remove(file["THUMBNAIL"])
    await event.delete()

@client.Command(command="YtSearch (.*)")
async def ytsearch(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)[:20]
    message = "@" + client.bot.me.username + " " + "Youtube:" + query
    await client(functions.messages.SaveDraftRequest(peer=event.chat_id, message=message))
    await event.delete()

@client.Inline(pattern="Youtube\:(.*)")
async def ytsearchinline(event):
    query = event.pattern_match.group(1)
    answers = []
    searchs = client.functions.yt_search(query, limit=20)
    for search in searchs:
        link = search["link"]
        text = client.getstrings(STRINGS)["searchinfo"].format(link, search["title"], search["viewCount"]["text"], search["duration"])
        infoshare = f"http://t.me/share/text?text=.YtInfo+{link}"
        vidshare = f"http://t.me/share/text?text=.YtVideo+{link}"
        audshare = f"http://t.me/share/text?text=.YtAudio+{link}"
        buttons = [[Button.url("• Get Info •", url=infoshare)], [Button.url("• Download Video •", url=vidshare)], [Button.url("• Download Audio •", url=audshare)]]
        thumb = types.InputWebDocument(search["thumbnails"][-1]["url"], 0, "image/jpg", [])
        answer = event.builder.article(
            title=search["title"],
            description=search["viewCount"]["text"],
            text=text,
            buttons=buttons,
            thumb=thumb,
        )
        answers.append(answer)
    await event.answer(answers)