# This has been created by TomTec Solutions

import minqlx
from random import randint

class fun(minqlx.Plugin):
    def __init__(self):
        self.add_command("penislength", self.cmd_penlen) # Junkyard requested


    def cmd_penlen(self, player, msg, channel):
        channel.reply("^7{}^7's penis length: ^4{}^7.".format(player, randint(0,12)))
