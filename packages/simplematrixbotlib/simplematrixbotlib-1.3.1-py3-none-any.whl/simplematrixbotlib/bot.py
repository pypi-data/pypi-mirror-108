import asyncio
import simplematrixbotlib as botlib


class Bot:
    """
    A class for the bot library user to interact with
    Example Usage:

    import simplematrixbotlib as bl
    
    creds = bl.Creds("home.server", "user", "pass")
    bot = bl.Bot(creds)
    bot.run()
    """
    def __init__(self, creds):
        self.creds = creds
        self.api = botlib.API(self.creds)
        self.message_actions = []

    async def main(self):
        await self.api.login()
        self.async_client = self.api.async_client

        await self.async_client.sync(timeout=65536, full_state=False) #Ignore prior messages

        self.callbacks = botlib.Callbacks(self.async_client, self)
        await self.callbacks.setup_callbacks()

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def add_message_listener(self, action_func):
        self.message_actions.append(action_func)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.main())
