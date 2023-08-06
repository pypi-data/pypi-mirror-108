
from importlib import resources
from configparser import ConfigParser
import connecty, discord, string
import colorama
colorama.init()

CBLUE = "\33[34m"
CVIOLET = "\33[35m"
CEND = "\033[0m"
CBOLD = "\033[1m"

def wrap(cl):
    def fu(txt):
        return cl + txt + CEND
    return fu

print(wrap(CBLUE)("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"))
print(wrap(CBLUE)("▉") + CVIOLET + CBOLD + " JOIN THE SUPPORT SERVER FOR HELP!! https://discord.gg/fcZBB2v " + wrap(CBLUE)("█"))
print(wrap(CBLUE)("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█"))

args = connecty.parser.parse_args()
config = ConfigParser()
config.read_string(resources.read_text(connecty, "defaults.ini"))
config.read(args.config)
bot = connecty.Bot()
bot_config = dict(config["BOT"])
del config["BOT"]

@bot.configure
async def init():
    for sec in config.sections():
        sec = config[sec]
        connection = await bot.register(list(int(ids) for ids in sec["links"].split()), echo=sec.getboolean("echo"), repeat=sec.getboolean("repeat"))
        @connection.on_message
        async def on_msg(message: discord.Message):
            new_content = message.content
            if sec.getboolean("template"): new_content = string.Template(new_content).safe_substitute(sec)
            payload = connecty.MessageLike.from_message(message)
            payload.content = new_content
            await connection.send(payload)

def start(): bot.run(bot_config["token"])
if __name__ == "__main__": start()
