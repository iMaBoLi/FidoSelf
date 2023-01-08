from FidoSelf import client
from traceback import format_exc
import asyncio
import time
import math

async def progress(event, current, total, start, type, file_name="---"):
    type = client.get_string("Progress_2") if type == "down" else client.get_string("Progress_3")
    now = time.time()
    diff = time.time() - start
    if round(diff % 8.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) * 1000
        strs = "●".join("●" for i in range(math.floor(perc / 8)))
        text = client.get_string("Progress_1").format(type, strs, round(perc, 2), file_name, client.utils.convert_bytes(current), client.utils.convert_bytes(total), client.utils.convert_bytes(speed), client.utils.convert_time(eta))
        await event.edit(text)

async def get_ids(event):
    event.userid, event.chatid = None, None
    if len(event.text.split()) > 1:
        try:
            gpeer =  await client.get_peer_id(eval(event.text.split()[1]))
            event.userid, event.chatid = gpeer, gpeer
        except:
            event.errorid = format_exc()
    elif event.reply_message:
        event.userid, event.chatid = event.reply_message.sender_id, event.chat_id
    elif event.is_private:
        event.userid, event.chatid = event.chat_id, event.chat_id
    return event

def mention(info):
    if info.username:
        return f"[{info.first_name}](@{info.username})"
    return f"[{info.first_name}](tg://user?id={info.id})"

def convert_date(gy, gm, gd):
   g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
   if (gm > 2):
       gy2 = gy + 1
   else:
       gy2 = gy
   days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
   jy = -1595 + (33 * (days // 12053))
   days %= 12053
   jy += 4 * (days // 1461)
   days %= 1461
   if (days > 365):
       jy += (days - 1) // 365
       days = (days - 1) % 365
   if (days < 186):
       jm = 1 + (days // 31)
       jd = 1 + (days % 31)
   else:
      jm = 7 + ((days - 186) // 30)
      jd = 1 + ((days - 186) % 30)
   return [jy, jm, jd]
