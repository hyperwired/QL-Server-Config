# Created by Thomas Jones on 14/12/2015 - thomas@tomtecsolutions.com
# ratinglimiter.py, a plugin for minqlx to limit a server to players within certain ratings.
# This plugin is released to everyone, for any purpose. It comes with no warranty, no guarantee it works, it's released AS IS.
# You can modify everything, except for lines 1-4 and the !tomtec_versions code. They're there to indicate I whacked this together originally. Please make it better :D

import minqlx
import requests
import time

class ratinglimiter(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded)
        
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.set_cvar_once("qlx_minRating", "0")
        self.set_cvar_once("qlx_maxRating", "1600")
        self.set_cvar_once("qlx_kickPlayersOutOfRatingBounds", "1")
        
        self.plugin_version = "1.0"


    @minqlx.thread
    def handle_player_loaded(self, player):
        try:
            url = "http://qlstats.net:8080/{elo}/{}".format(player.steam_id, elo=self.get_cvar('qlx_balanceApi'))
            res = requests.get(url)
            if res.status_code != requests.codes.ok: raise
            js = res.json()
            gt = self.game.type_short
            if "players" not in js: raise
            for p in js["players"]:
                if int(p["steamid"]) == player.steam_id and gt in p:
                    self.msg("^1Debug:^7 " + player, p[gt]['elo'], p[gt]['games'])
                    
        except Exception as e:
            self.msg("^1Error: ^7{}".format(e))
            pass



    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4ratinglimiter.py^7 - version {}, created by Thomas Jones on 27/02/2016.".format(self.plugin_version))
