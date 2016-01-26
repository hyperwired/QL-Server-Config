# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

"""
    This plugin is loaded by quakeupdate.sh. Do not load this plugin otherwise.
"""

import minqlx

class maintenance(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connected)
        self.msg("^1Maintenance plugin has been loaded.^7")
        minqlx.console_command("map campgrounds ffa")
        self.counter = 0

    def handle_player_connected(self, player):
        if self.counter == 0:
            self.counter = 1
            return "TomTec Solutions servers are currently down for maintenance."
        elif self.counter == 1:
            self.counter = 2
            return "You'll be back in the game within a few short minutes."
        elif self.counter == 2:
            self.counter = 0
            return "Please wait patiently."
