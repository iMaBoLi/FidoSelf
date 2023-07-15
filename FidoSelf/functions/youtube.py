from FidoSelf import client
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from PIL import Image
import random
import re
import os

YOUTUBE_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})")

MAIN = "yt-dlp -o '{outfile}' -f {format} {link}"
THUMB = "yt-dlp -o '{outfile}' --write-thumbnail --skip-download {link}"

def yt_info(link):
    info = YoutubeDL().extract_info(link, download=False)
    return info

async def yt_downloader(link, format, ext):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + filename + "." + ext
    cmd = MAIN.format(outfile=outfile, format=format, link=link)
    await client.functions.runcmd(cmd)
    info = {}
    info["OUTFILE"] = outfile
    thumb = await yt_thumb(link)
    info["THUMBNAIL"] = thumb
    return info

async def yt_video(link):
    filename = str(random.randint(11111, 99999))
    outfile = client.PATH + "youtube/" + filename + ".mp4" 
    OPTS = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
            {"key": "FFmpegMetadata"},
        ],
        "outtmpl": outfile,
        "logtostderr": False,
        "quiet": True,
    }
    YoutubeDL(OPTS).download([link])
    info = {}
    info["OUTFILE"] = outfile
    thumb = await yt_thumb(link)
    info["THUMBNAIL"] = thumb
    return info

async def yt_thumb(link):
    filename = get_videoid(link) + str(random.randint(11111, 99999))
    thumb = client.PATH + "youtube/" + filename
    cmd = THUMB.format(outfile=thumb, link=link)
    await client.functions.runcmd(cmd)
    thumb = convert_thumb(thumb + ".webp")
    return thumb

def convert_thumb(file):
    thumb = file + ".jpg"
    try:
        img = Image.open(file)
        img.save(thumb, format="jpeg")
        os.remove(file)
    except:
        os.rename(file, thumb)
    return thumb
    
def yt_search(query, limit=50):
    results = VideosSearch(query, limit=limit)
    return results.result()["result"]