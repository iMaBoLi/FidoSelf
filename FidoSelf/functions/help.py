from FidoSelf import client

def AddInfo(info):
    category = info["Category"]
    pluginname = info["Plugname"]
    plugininfo = info["Pluginfo"]
    if category not in client.HELP:
        client.HELP.update({category: {}})
    client.HELP[category][pluginname] = plugininfo