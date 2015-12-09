# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class tp_sounds(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        
    def map_load(self, mapname, factory):
        # Download the purgery sound pack for all new players, and ref to old
        self.game.steamworks_items += [572198990] # 571878681, quake 3 sounds
