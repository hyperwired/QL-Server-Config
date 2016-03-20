# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# It provides an option to receive a message when you become railable
#

import minqlx
import datetime
import time
import threading
import requests

VERSION = "v0.2"

PLAYER_KEY = "minqlx:players:{}"
RAIL_KEY = PLAYER_KEY + ":railable"
RAIL_MSG_KEY = PLAYER_KEY + ":railmsg"

DEFAULT_MESSAGE = "^1Railable!^7"

class railable(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        self.shown = []
        self.running = False

        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("death", self.handle_death)
        self.add_command("railable", self.cmd_toggle_pref)

    def cmd_toggle_pref(self, player, msg, channel):
        self.set_notif_pref(player.steam_id)

        if self.get_notif_pref(player.steam_id):
            channel.reply("^7{} will now get a hint when ^2!railable^7.".format(player.name))
        else:
            channel.reply("^7{} will stop seeing ^2!railable ^7notifications.".format(player.name))


    def handle_death(self, victim, killer, data):
        if victim.id in self.shown:
            self.shown.remove()

    def handle_round_start(self, n):
        self.running = True
        self.shown = []
        threading.Thread(target=self.looking).start()

    def handle_round_end(self, n):
        self.running = False

    def looking(self):
        while self.game.state == 'in_progress' and self.running:
            teams = self.teams()
            for p in teams['red'] + teams['blue']:
                pid = p.steam_id
                if self.get_notif_pref(pid) and self.railable(p) and not pid in self.shown:
                    p.center_print(DEFAULT_MESSAGE)
                    self.shown.append(pid)
            time.sleep(0.33)

    def railable(self, p):
        if p.is_alive:
            h = p.health
            a = p.armor
            return (h <= 26) or (h+a <= 80)
        return False

    def get_notif_pref(self, sid):
        try:
            return int(self.db[RAIL_KEY.format(sid)])
        except:
            return False

    def set_notif_pref(self, sid):
        self.db[RAIL_KEY.format(sid)] = 0 if self.get_notif_pref(sid) else 1

    def get_rail_msg(self, sid):
        try:
            return self.db[RAIL_MSG_KEY.format(sid)]
        except:
            return False

    def set_rail_msg(self, sid, msg):
        self.db[RAIL_MSG_KEY.format(sid)] = msg
