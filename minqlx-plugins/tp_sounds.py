# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

queue_q3a = False
queue_tp = False

class tp_sounds(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_command("queue_q3a", self.cmd_queueSoundPack_q3a, 5)
        self.add_command("unqueue_q3a", self.cmd_unqueueSoundPack_q3a, 5)

        self.add_command("queue_tp", self.cmd_queueSoundPack_tp, 5)
        self.add_command("unqueue_tp", self.cmd_unqueueSoundPack_tp, 5)

        
    def map_load(self, mapname, factory):
        if queue_tp == True:
            self.game.steamworks_items += [571878211]

        if queue_q3a == True:
            self.game.steamworks_items += [571878681]

    def cmd_queueSoundPack_q3a(self, player, msg, channel):
        queue_q3a = True
        channel.reply("^1Quake III Arena^7: Sound pack queued. Reload map to reference steamworks item to clients.")
                        
    def cmd_unqueueSoundPack_q3a(self, player, msg, channel):
        queue_q3a = False
        channel.reply("^1Quake III Arena^7: Sound pack unqueued.")

    def cmd_queueSoundPack_tp(self, player, msg, channel):
        queue_tp = True
        channel.reply("^1The Purgery - Sound Pack^7: Sound pack queued. Reload map to reference steamworks item to clients.")
                        
    def cmd_unqueueSoundPack_tp(self, player, msg, channel):
        queue_tp = False
        channel.reply("^1The Purgery - Sound Pack^7: Sound pack unqueued.")
