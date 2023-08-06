import discord, types, typing


class MessageLike:
    """
    Children of this class may be passed to Link.send for complete control over the message sent by the webhook
    """
    content: str
    tts: bool
    id: int
    author: types.SimpleNamespace

    # https://i.imgur.com/DTJuzsi.png
    def __init__(self, content, author_name="unset", author_avatar_url="unset", tts=False, id=None):
        self.content = content
        self.tts = tts
        self.id = id
        self.author = types.SimpleNamespace(name=author_name, avatar_url=author_avatar_url)

    @classmethod
    def from_message(cls, msg: discord.Message):
        new_msg = cls(
            content=msg.content,
            author_name=msg.author.name,
            author_avatar_url=msg.author.avatar_url,
            tts=msg.tts,
            id=msg.id
        )
        new_msg.channel = msg.channel
        return new_msg


class Link:
    hook: discord.Webhook
    channel: discord.TextChannel
    bot: discord.Client
    his: set
    handler: typing.Callable

    @classmethod
    async def new(cls, channel: discord.TextChannel, bot: discord.Client, chain):
        self = cls()
        self.chain = chain
        self.his = set()
        self.handler = None
        self.bot = bot
        self.channel = channel
        hooks = await channel.webhooks()
        name = bot.user.name
        for hook in hooks:
            if hook.name == name:
                self.hook = hook
                break
        else:
            self.hook = await channel.create_webhook(name=name)
        return self

    async def send(self, msg: typing.Union[discord.Message, MessageLike, str]):
        """
        Send a message to the channel.
        If a string is passed, the bot will not use the webhook to send the message.
        If a discord message is passed, the bot will try to imitate the message and author using a webhook.
        A MessageLike can be passed for finer control.
        """

        if isinstance(msg, str):
            await self.channel.send(msg)
        else:
            if msg.id:
                if msg.id in self.his:
                    return
                else:
                    self.his.add(msg.id)
            if hasattr(msg, "channel"):
                if msg.channel == self.channel:
                    return
            await self.hook.send(content=msg.content, avatar_url=str(msg.author.avatar_url), username=msg.author.name, tts=msg.tts)

        """
        elif isinstance(msg, MessageLike):
            await self.hook.send(content=msg.content, avatar_url=str(msg.avatar_url), username=msg.name, tts=msg.tts)
        elif isinstance(msg, discord.Message):
            if not self.chain.echo:
                if msg.channel == self.channel:
                    return
            if not self.chain.repeat:
                if msg.id in self.his:
                    return
                else:
                    self.his.add(msg.id)
            await self.hook.send(content=msg.content, avatar_url=str(msg.author.avatar_url), username=msg.author.name, tts=msg.tts)
        """
    async def check(self, message: discord.Message):
        if message.channel.id == self.channel.id:
            if self.handler:
                await self.handler(message)

    def on_message(self, func: typing.Callable):
        """
        Decorator that is called whenever this channel receives a new message.
        """
        self.handler = func


class Chain:
    links: list[Link]
    bot: discord.Client
    handler: typing.Callable
    echo: bool
    repeat: bool

    @classmethod
    async def new(cls, channels: list[discord.TextChannel], bot: discord.Client, echo, repeat):
        self = cls()
        self.echo = echo
        self.repeat = repeat
        self.bot = bot
        self.handler = None
        self.links = list()
        for channel in channels:
            self.links.append(await Link.new(channel, bot, self))
        return self

    async def check(self, message: discord.Message):
        if message.channel.id in (link.channel.id for link in self.links):
            if self.handler:
                await self.handler(message)
            for link in self.links:
                await link.check(message)

    async def send(self, message: MessageLike):
        """
        Send a message to each and every channel contained within the chain.
        If a string is passed, the bot will not use the webhook to send the message.
        If a discord message is passed, the bot will try to imitate the message and author using a webhook.
        A MessageLike can be passed for finer control.
        """
        for link in self.links:
            await link.send(message)

    def on_message(self, func: typing.Callable):
        """
        Decorator that is called whenever any channel contained within this chain receives a message.
        """
        self.handler = func


class Bot(discord.Client):

    def __init__(self, defaults=None):
        super().__init__()
        self.chains = []
        self.init = None
        self.defaults = {"echo": False, "repeat": False}
        if defaults is not None: self.defaults.update(defaults)

    async def on_ready(self):
        await self.init()
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        if message.author == self.user or (int(message.author.discriminator) == 0):
            return

        for chain in self.chains:
            await chain.check(message)

    async def register(self, channels: list[int], **options):
        """
        Pass a list of channel IDs.
        A newly created chain (connection) will be returned.
        """
        new_defaults = self.defaults.copy()
        new_defaults.update(options)
        channels = [self.get_channel(id) for id in channels]
        chain = await Chain.new(channels, self, **new_defaults)
        self.chains.append(chain)
        return chain

    def configure(self, func: typing.Callable):
        """
        All custom code should be placed within an async function wrapped by this decorator
        """
        self.init = func