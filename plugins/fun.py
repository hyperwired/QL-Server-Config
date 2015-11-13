# This has been created by TomTec Solutions
# This file contains community ideas that may be found to be in bad taste. These views do not represent the views of TomTec Solutions

import minqlx
from random import randint

class fun(minqlx.Plugin):
    def __init__(self):
        self.add_command("penislength", self.cmd_penlen) # Junkyard requested
        self.add_command(("vaginadepth", "vaginaldepth", "vaginialdepth"), self.cmd_vagdep) # Junkyard requested
        self.add_command(("msg", "message"), self.cmd_screenmessage, 1, usage="<text>") # Merozollo requested
 
    def cmd_penlen(self, player, msg, channel):
        playerName = player.clean_name
        if playerName.lower() == "zeobyte":
            channel.reply("^7{}^7's penis length: ^412 inches^7".format(player))
        else:
            randNum = randint(0,11)
            if randNum == 0:
                channel.reply("^7{}^7's penis length: ^40 inches (inverted!)^7".format(player))
            else:
                channel.reply("^7{}^7's penis length: ^4{} inch(es)^7".format(player, randNum))

    def cmd_vagdep(self, player, msg, channel):
        playerName = player.clean_name
        if playerName.lower() == "zeobyte":
            channel.reply("^7{}^7's vaginial depth: ^4-12 inches^7".format(player))
        else:
            randNum = randint(0,11)
            if randNum == 0:
                channel.reply("^7{}^7's vaginial depth: ^40 inches (are you trans?)^7".format(player))
            else:
                channel.reply("^7{}^7's vaginial depth: ^4{} inch(es)^7".format(player, randNum))

    def cmd_screenmessage(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        minqlx.console_command("cp ^7{}^7".format(" ".join(msg[1:])))
        #self.play_sound("sound/world/klaxon2.wav")
