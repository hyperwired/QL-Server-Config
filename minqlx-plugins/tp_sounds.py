# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class tp_sounds(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_command("queueq3a", self.cmd_queueSoundPack, 5)
        self.add_command("unqueueq3a", self.cmd_unqueueSoundPack, 5)

        self.set_cvar_once("qlx_queueSoundPack", "0")
        
    def map_load(self, mapname, factory):
        if self.get_cvar("qlx_queueSoundPack") == "1":
            self.game.steamworks_items += [571860199]

    def cmd_queueSoundPack(self, player, msg, channel):
        self.set_cvar("qlx_queueSoundPack", "1")
        channel.reply("^1Quake III Arena^7: Sound pack queued. Reload map to reference steamworks item to clients.")
                        
    def cmd_unqueueSoundPack(self, player, msg, channel):
        self.set_cvar("qlx_queueSoundPack", "0")
        channel.reply("^1Quake III Arena^7: Sound pack unqueued.")
