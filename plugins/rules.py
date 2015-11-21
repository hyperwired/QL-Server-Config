# This has been created by TomTec Solutions
import minqlx

class rules(minqlx.Plugin):
    def __init__(self):
        self.add_command("rules", self.cmd_showrules)
      
    def cmd_showrules(self, player, msg, channel):
        channel.reply("^4========================================================================================")
        channel.reply("^4The Purgery^7 - ^3Server Rules:")
        channel.reply("^7    1. No racism, neo-nazism, harassment or abuse toward other players via text or voice chat.")
        channel.reply("^7    2. No disruptive behaviour of any kind, including 'spamming' and repetitive call-voting")
        channel.reply("^7    3. No cheating, hacking or abuse of server privileges.")
        channel.reply("^7    4. Lack of common sense is prohibited.")
        channel.reply("^7    5. If you've been muted, you're obviously doing something that one or more server ops don't approve of.")
        channel.reply("^7    6. These servers are being paid for by ^4Zeo^7byte, and the donators that assist with the funding.")
        channel.reply("^1  Failure to comply with these rules will result in a mute, a temporary ban, or a permanent ban.")
        channel.reply("^7  Have ^2fun^7, play, enjoy, don't do anything stupid.")
        channel.reply("^4========================================================================================")
