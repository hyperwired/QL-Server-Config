# This has been created by TomTec Solutions

import minqlx

class branding(minqlx.Plugin):
    def __init__(self):
        self.add_hook("new_game", self.brand_map)
      
    def brand_map(self):
      minqlx.set_configstring(3, "^4The Purgery^7")
      minqlx.set_configstring(678, "Sponsored by TomTec Solutions")
      minqlx.set_configstring(679, "Visit our IRC channel on QuakeNet, ^4#thepurgery^7.")
