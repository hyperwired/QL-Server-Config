# This has been created by TomTec Solutions
<<<<<<< HEAD
=======
# This file contains community ideas that may be found to be in bad taste. These views do not represent the views of TomTec Solutions

>>>>>>> origin/master
import minqlx
from random import randint

class fun(minqlx.Plugin):
    def __init__(self):
        self.add_command("penislength", self.cmd_penlen) # Junkyard requested
        self.add_command("poke", self.cmd_poke, usage="<text>") # Merozollo requested
 
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


    def cmd_poke(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        displayText = " ".join(msg[1:])
        
        minqlx.console_command("cp ^7WAKE UP, {}^7!".format(displayText))
        self.play_sound("sound/world/klaxon2.wav")