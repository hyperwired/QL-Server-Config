# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class quiet(minqlx.Plugin):
    def __init__(self):
        self.add_hook("client_command", self.handle_client_command)
        self.add_hook("game_countdown", self.game_countdown)
        
        self.add_command("tomtec_versions", self.cmd_showversion)
        
        self.plugin_version = "1.0"


    def handle_client_command(self, player, cmd):
        if self.game.state != "warmup":
            if (cmd.lower().startswith("say ") or cmd.lower().startswith("say_team ") or cmd.lower().startswith("tell ")):
                ident = player.steam_id
                if not (player.privileges in ["admin", "mod"] or self.db.has_permission(ident, 4)):
                    player.tell("Chat is disabled during the match.")
                    return minqlx.RET_STOP_ALL

    def game_countdown(self):
        self.msg("Chat is now disabled during the match.")
                
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4quiet.py^7 - version {}, created by Thomas Jones on 10/01/2016.".format(self.plugin_version))
