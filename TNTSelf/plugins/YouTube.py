from TNTSelf import client
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
    "plistlink": "**{STR} The Entered Youtube PlayList Link** ( `{}` ) **Is Not Supported!**",
    "downvideo": "**{STR} Downloadig Video From Youtube ...**\n\n**{STR} Link:** ( `{}` )",
    "downaudio": "**{STR} Downloadig Audio From Youtube ...**\n\n**{STR} Link:** ( `{}` )",
    "caption": "**{STR} Title:** ( `{}` )\n\n**{STR} Uploader:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )\n**{STR} Size:** ( `{}` )\n**{STR} Duration:** ( `{}` )",
    "description": "**{STR} Description:** ( `{}` )",
    "plistinfo": "**{STR} Title:** ( {} )\n\n**{STR} Views:** ( `{}` )\n**{STR} Type:** ( `{}` )\n**{STR} Videos:** ( `{}` )\n\n**{STR} Uploader:** ( {} )\n**{STR} Followers:** ( `{}` )",
    "soloinfo": "**{STR} Title:** ( {} )\n\n**{STR} Views:** ( `{}` )\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )\n**{STR} Duration:** ( `{}` )\n\n**{STR} Uploader:** ( {} )\n**{STR} Followers:** ( `{}` )",
    "plistlinks": "**{STR} The Videos Link:**\n\n",
    "searchclick": "**{STR} Click To Follow Button To Get Search Results For Query:** ( `{}` )",
    "searchinfo": "**{STR} Link:** ( {} )\n**{STR} Title:** ( `{}` )\n**{STR} Views:** ( `{}` )\n**{STR} Duration:** ( `{}` )",
}
    
@client.Command(command="Yt(Video|Audio) (.*)")
async def ytdownloader(event):
    await event.edit(client.STRINGS["wait"])
    downtype = event.pattern_match.group(1).title()
    link = event.pattern_match.group(2)
    ytinfo, type = client.functions.yt_info(link)
    if not ytinfo:
        return await event.edit(client.getstrings(STRINGS)["linkinv"].format(link))
    if type == "PlayList":
        return await event.edit(client.getstrings(STRINGS)["plistlink"].format(link))
    if downtype == "Video":
        await event.edit(client.getstrings(STRINGS)["downvideo"].format(link))
        file = await client.functions.yt_video(link)
        filename = ytinfo["title"] + ".mp4"
        attributes = [types.DocumentAttributeVideo(duration=ytinfo["duration"], w=ytinfo["width"], h=ytinfo["height"], supports_streaming=True), types.DocumentAttributeFilename(file_name=filename)]
    elif downtype == "Audio":
        await event.edit(client.getstrings(STRINGS)["downaudio"].format(link))
        file = await client.functions.yt_audio(link)
        filename = ytinfo["title"] + ".mp3"
        attributes = [types.DocumentAttributeAudio(duration=ytinfo["duration"], voice=False, title=ytinfo["title"], performer=ytinfo["uploader"]), types.DocumentAttributeFilename(file_name=filename)]
    thumb = await client.functions.yt_thumb(link)
    filesize = os.path.getsize(file)
    filesize = client.functions.convert_bytes(filesize)
    caption = client.getstrings(STRINGS)["caption"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["like_count"], ytinfo["comment_count"], filesize, ytinfo["duration_string"])
    callback = client.progress(event, upload=True, filename=filename)
    uploadfile = await client.fast_upload(file, progress_callback=callback)
    await client.send_file(event.chat_id, uploadfile, thumb=thumb, attributes=attributes, caption=caption)
    os.remove(file)
    os.remove(thumb)
    await event.delete()

@client.Command(command="YtInfo (.*)")
async def ytinfo(event):
    await event.edit(client.STRINGS["wait"])
    link = event.pattern_match.group(1)
    ytinfo, type = client.functions.yt_info(link)
    if not ytinfo:
        return await event.edit(client.getstrings(STRINGS)["linkinv"].format(link))
    thumb = await client.functions.yt_thumb(link)
    if type == "PlayList":
        title = f'[{ytinfo["title"]}]({ytinfo["original_url"]})'
        uploader = f'[{ytinfo["uploader"]}]({ytinfo["channel_url"]})'
        caption = client.getstrings(STRINGS)["plistinfo"].format(title, ytinfo["view_count"], type, ytinfo["playlist_count"], uploader, (ytinfo["channel_follower_count"] or 0))
    elif type == "Solo":
        title = f'[{ytinfo["title"]}]({ytinfo["original_url"]})'
        uploader = f'[{ytinfo["uploader"]}]({ytinfo["channel_url"]})'
        caption = client.getstrings(STRINGS)["soloinfo"].format(title, ytinfo["view_count"], ytinfo["like_count"], ytinfo["comment_count"], ytinfo["duration_string"], uploader, (ytinfo["channel_follower_count"] or 0))
    send = await client.send_file(event.chat_id, thumb, caption=caption)
    description = ytinfo["description"]
    description = client.getstrings(STRINGS)["description"].format(description)
    if len(description) < 4096:
        await send.reply(description)
    if type == "PlayList":
        links = client.getstrings(STRINGS)["plistlinks"]
        for row, video in enumerate(ytinfo["entries"]):
            link = "https://www.youtube.com/watch?v=" + video["id"]
            links += f"**{row + 1} -** `{link}`\n"
        await send.reply(links)
    os.remove(thumb)
    await event.delete()

@client.Command(command="YtSearch (.*)")
async def ytsearch(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)[:20]
    message = "@" + client.bot.me.username + " " + "YTSearch:" + query
    await client(functions.messages.SaveDraftRequest(peer=event.chat_id, message=message))
    await event.delete()

@client.Inline(pattern="YTSearch\\:(.*)")
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
    
