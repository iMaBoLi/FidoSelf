from FidoSelf import client
import shutil, glob, os

STRINGS = {
    "complete": "**Successfuly Updated And Restarting ...**",
}

@client.Command(command="Update")
async def update(event):
    await event.edit(client.STRINGS["wait"])
    git = client.functions.Git()
    link = git.repo.get_archive_link("zipball", "scal")
    await client.functions.runcmd(f"curl {link} -o Fido.zip")
    await client.functions.runcmd("unzip Fido.zip")
    shutil.rmtree("/app/FidoSelf/")
    shutil.rmtree("/app/downloads/")
    path = glob.glob("iMaBoLi*")[0]
    newpath = "/app/" + path + "/FidoSelf/"
    shutil.copytree(newpath, "/app/FidoSelf/")
    await event.edit(STRINGS["complete"])
    shutil.rmtree(path)
    os.remove("Fido.zip")
    await client.functions.runcmd("python3 -m FidoSelf")