# This has been created by TomTec Solutions

import minqlx

class branding(minqlx.Plugin):
    def __init__(self):
        self.add_hook("new_game", self.brand_map)
        self.add_hook("game_countdown", self.sponsor_message)
      
    def brand_map(self):
        minqlx.set_configstring(3, "^4The Purgery^7")
        minqlx.set_configstring(678, "Sponsored by TomTec Solutions")
        minqlx.set_configstring(679, "Visit our IRC channel on QuakeNet, ^4#thepurgery^7.")

    def sponsor_message(self):
        minqlx.send_server_command(None, "cp \"^4The Purgery\n^7Sponsored by TomTec Solutions^7\"\n")
