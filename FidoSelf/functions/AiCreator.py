from FidoSelf import client

def AiCreate(Chats, filename):
    FIRST = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="icon" href="https://chat.openai.com/apple-touch-icon.png" type="image/x-icon"><title>ChatGPT</title><style>@media only screen and (max-width: 600px) {body {font-size: 9px !important;} .a{padding-left: 10%;} .q{padding-left: 10%;}} body{background-color: #444654;margin: 0;padding: 0;overflow-x: hidden;}.q{  border-top: 2px solid rgba(32,33,35,.5);  border-bottom: 2px solid rgba(32,33,35,.5);			width: 100%;			height: fit-content;  background-color: #343541;  padding: 20px 20%;  text-align: left;  color: #ECECF1;margin: 20px 0px;}.a{			width: 100%;			height: fit-content;  padding: 10px;  padding-left: 20%;  text-align: left;  margin: 20px 0px;  color: #ECECF1;}img{  width: 30px;  height: 30px;  border-radius: 10px;  padding-right: 10px;}.name{  font-size:small !important;  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}.lang{font-size:small !important; padding: 5px 10px ;background-color: #343541; border-top-right-radius: 5px;border-top-left-radius: 5px; color: #00a67d; display: block;  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}.code{border-bottom-right-radius: 5px;border-bottom-left-radius: 5px; margin-top:-21px; padding: 10px 10px ;background-color: black; color: #00a67d; display: block;  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}div{  padding-left: 5%;width: 50%;font-family: Söhne,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif,Helvetica Neue,Arial,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;}</style></head><body>"""
    LAST = """</body></html>"""
    MATN = """<section  class="q"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Telegram_2019_Logo.svg/121px-Telegram_2019_Logo.svg.png" type="image/x-icon"><span class="name">User: </span><div>{YOURINPUT}</div></section><section class="a"><img src="https://chat.openai.com/apple-touch-icon.png" type="image/x-icon"><span class="name">ChatGPT: </span><div>{CHATGPTRESULT}</div></section>"""
    LASTMATN = ""
    Chats = list(client.functions.chunks(Chats, 2))
    for chat in Chats:
        NEWMATN = MATN
        me = con[0]["content"]
        gpt = con[1]["content"]
        NEWMATN = NEWMATN.replace("{YOURINPUT}", me)
        NEWMATN = NEWMATN.replace("{CHATGPTRESULT}", gpt)
        LASTMATN += NEWMATN
    result = FIRST + LASTMATN + LAST
    open(filename, "w").write(result)
    return filename