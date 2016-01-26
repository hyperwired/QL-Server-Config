# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

"""
    This plugin is loaded by quakeupdate.sh. Do not load this plugin otherwise.
"""

import minqlx

class maintenance(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connected)
        self.msg("^13:00am AEST:^7 Servers are going down for routine maintenance/updates.^7")
        minqlx.unload_plugin("tomtec_logic")
        minqlx.unload_plugin("irc")
        for p in self.players():
            minqlx.client_command(p.id, "disconnect")
        minqlx.console_command("map campgrounds ffa")
        self.counter = 0

    def handle_player_connected(self, player):
        if self.counter == 0:
            self.counter = 1
            return "TomTec Solutions servers are currently down for routine updates."
        elif self.counter == 1:
            self.counter = 2
            return "Routine maintenance/updates occurs at 3:00am AEST daily."
        elif self.counter == 2:
            self.counter = 3
            return "If the servers are down at any other time, please contact Purger as soon as possible."
        elif self.counter == 3:
            self.counter = 0
            return "Please wait patiently, the server will be online again within a few minutes."
