# This has been created by TomTec Solutions

import minqlx
from random import randint

class fun(minqlx.Plugin):
    def __init__(self):
        self.add_command("penislength", self.cmd_penlen) # Junkyard requested
 
    def cmd_penlen(self, player, msg, channel):
        if player.clean_name == "Zeobyte":
            channel.reply("^7{}^7's penis length: ^412 inches^7".format(player))
        else:
            channel.reply("^7{}^7's penis length: ^4{} inch(es)^7".format(player, randint(0,11)))
