import asyncio


class MCommand:
    def __init__(self, value):
        self.bot = value
        self.message = None

    async def test(self):
        print_message = "Calculating messages..."
        mes = await self.bot.send_message(self.message.channel, print_message)
        await asyncio.sleep(5)
        await self.bot.delete_message(mes)

    async def sleep(self):
        await self.bot.send_message(self.message.channel, 'Done sleeping')

    async def callsomeone(self):
        print('Testing call someone')

    async def getchannel(self):
        for server in self.bot.servers:
            for channel in server.channels:
                await self.bot.send_message(self.message.channel, channel.name)

    async def join(self):
        print('Testing Join')

    async def default_action(self):
        return

    async def command(self, value, message):
        if self.bot.user.id == message.author.id:
            return

        await self.bot.delete_message(message)

        await asyncio.sleep(1)
        self.message = message

        possibles = globals().copy()
        possibles.update(locals())

        method_name = value.replace("!", "")

        method = getattr(self, method_name, self.default_action)

        await method()
