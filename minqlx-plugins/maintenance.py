# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class maintenance(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connected)
        minqlx.console_command("map eyetoeye ffa")


    def handle_player_connected(self, player):
        return "TomTec Solutions servers are currently down for maintenance. Try connecting again in 5 minutes."
