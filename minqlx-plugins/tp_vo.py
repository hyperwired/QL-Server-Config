# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

GAMEMODS = ["infected", "quadhog"]

import minqlx, time
from random import randint
class tp_vo(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.1"

        
    def map_load(self, *args, **kwargs):
        self.game.workshop_items += [572495786]

    @minqlx.delay(2)
    def handle_game_countdown(self, *args, **kwargs):
        @minqlx.thread
        def announceGametype():
            time.sleep(1.6)
            done = False
            for mod in GAMEMODS:
                if mod.lower() in self.game.factory.lower() and not done:
                    self.play_sound("tp_vo/gametypes/mods/{}.ogg".format(mod.lower()))
                    done = True
            if not done:
                self.play_sound("tp_vo/gametypes/{}.ogg".format(self.game.type_short))
        self.play_sound("tp_vo/rulesets/pql.ogg") if self.get_cvar("pmove_aircontrol", bool) else self.play_sound("tp_vo/rulesets/vql.ogg")
        announceGametype()
        
    @minqlx.delay(2)
    def handle_game_end(self, *args, **kwargs):
        rand = randint(0, 9)
        self.play_sound("tp_vo/general/good_game.ogg") if rand else self.play_sound("tp_vo/general/great_game.ogg")
        
    @minqlx.delay(3)
    def handle_player_loaded(self, player):
        self.play_sound("tp_vo/purgery/welcome_to_the_purgery.ogg", player)

    def handle_player_connect(self, player):
        if str(player.steam_id) == str(minqlx.owner()):
            self.play_sound("tp_vo/purgery/purger.ogg")
            
        
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4tp_vo.py^7 - version {}, created by Thomas Jones on 11/12/2015.".format(self.plugin_version))
