from FidoSelf import client

class TestClass:
    def __init__(self):
        self.client = client
    def ping(self):
        @self.client.Cmd(pattern="Kosk")
        async def ping(self):
            await self.client.send_message(event.chat_id, 'online')
