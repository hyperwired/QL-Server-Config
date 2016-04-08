# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

QUOTES = [
    "Sit Ubu, sit! Good dog!",
    "Time is an illusion, lunchtime doubly so.",
    "Don't whizz on the electric fence!"
]


import minqlx
from random import randint
class connect_quotes(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_loaded", self.handle_player_loaded)

        self.add_command("tomtec_versions", self.cmd_showversion)
        
        self.plugin_version = "1.0"

        self.playerConnectedYetList = []
        self.counter = 0
        
    def handle_player_connect(self, player):
        if player not in self.playerConnectedYetList:
            self.playerConnectedYetList.append(player)
            randomNumber = randint(0, (len(QUOTES) - 1))
            randomQuote = QUOTES[randomNumber]
            return randomQuote

    def handle_player_loaded(self, player):
        try:
            self.playerConnectedYetList.remove(player)
        except:
            return

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4connect_quotes.py^7 - version {}, created by Thomas Jones on 08/04/2016.".format(self.plugin_version))
