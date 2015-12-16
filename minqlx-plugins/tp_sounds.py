# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class tp_sounds(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.0"
        
    def map_load(self, mapname, factory):
        # Download the purgery sound pack for all new players, and ref to old
        self.game.workshop_items += [572495786] # 571878681, quake 3 sounds

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4tp_sounds.py^7 - version {}, created by Thomas Jones on 11/12/2015.".format(self.plugin_version))
