# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

"""
    This plugin is loaded by quakeupdate.sh. Do not load this plugin otherwise.
"""

import minqlx

class maintenance(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connected)
        self.msg("^1Maintenance plugin has been loaded.^7 Kicking all players...")
        minqlx.console_command("kick all \"TomTec Solutions are going down for maintenance. Try connecting again in 5 minutes.\"")
        minqlx.console_print("All players are kicked and server is unconnectable.")

    def handle_player_connected(self, player):
        return "TomTec Solutions servers are currently going down for maintenance. Try connecting again in 5 minutes."
