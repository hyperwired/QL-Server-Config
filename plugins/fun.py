# This has been created by TomTec Solutions
# This file contains community ideas that may be found to be in bad taste. These views do not represent the views of TomTec Solutions

import minqlx
from random import randint

class fun(minqlx.Plugin):
    def __init__(self):
        self.add_command("penislength", self.cmd_penlen) # Junkyard requested
        self.add_command(("vaginadepth", "vaginaldepth", "vaginialdepth"), self.cmd_vagdep) # Junkyard requested
        self.add_command(("msg", "message"), self.cmd_screenmessage, 1, usage="<text>") # Merozollo requested
        self.add_command(("breastsize", "cupsize", "brasize", "boobsize"), self.cmd_boobsize) # 0regonn requested
        self.add_command("fuckyou", self.cmd_printfu, 1)
 
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

    def cmd_boobsize(self, player, msg, channel):
        playerName = player.clean_name
        if playerName.lower() == "zeobyte":
            channel.reply("^7{}^7's cup size: ^4Stop asking, you're male!".format(playerName))
        else:
            randNum = randint(0,5)
            if randNum == 0:
                cupSize = "A"
            elif randNum == 1:
                cupSize = "B"
            elif randNum == 2:
                cupSize = "C"
            elif randNum == 3:
                cupSize = "D"
            elif randNum == 4:
                cupSize = "DD"
            elif randNum == 5:
                cupSize = "Z (discount wheelbarrow at Bunnings!)"

            channel.reply("^7{}^7's cup size: ^4{}^7".format(playerName, cupSize))
           
    def cmd_screenmessage(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        minqlx.console_command("cp ^7{}^7".format(" ".join(msg[1:])))
        #self.play_sound("sound/world/klaxon2.wav")

    def cmd_printfu(self, player, msg, channel):
        minqlx.send_server_command(None, "cp \"^0FUCK YOU\n^1FUCK YOU\n^2FUCK YOU\n^3FUCK YOU\n^4FUCK YOU\n^5FUCK YOU\n^6FUCK YOU\"\n")

