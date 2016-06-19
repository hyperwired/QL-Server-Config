# Created by Thomas Jones on 11/02/2016 - thomas@tomtecsolutions.com
# strictvql.py, a plugin to comply with VQL player wishes, see forum: http://www.4seasonsgaming.com/forums/viewtopic.php?p=105895#p105895
# This plugin is released to everyone, for any purpose. It comes with no warranty, no guarantee it works, it's released AS IS.
# You can modify everything, except for lines 1-4 and the !tomtec_versions code. They're there to indicate I whacked this together originally. Please make it better :D

import minqlx


class strictvql(minqlx.Plugin):    
    def __init__(self):
        self.add_command("tomtec_versions", self.cmd_showversion)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("new_game", self.handle_new_game)
        
        self.plugin_version = "1.3"


    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "teamsize":
            if self.game.state != "warmup":
                if args >= self.get_cvar("teamsize", str):
                    caller.tell("You can only vote to lower the teamsize ({}) once the game has begun.".format(self.get_cvar("teamsize")))
                    return minqlx.RET_STOP_ALL
        elif (vote.lower() == "kick" or vote.lower() == "spec"):
            return
        else:
            if self.game.state != "warmup":
                if self.db.has_permission(caller.steam_id, 3):
                    return
                else:
                    caller.tell("All votes barring ^2teamsize^7, ^2kick^7 and ^2spec^7 are disabled during the game.")
                    return minqlx.RET_STOP_ALL

    @minqlx.delay(300)       
    def handle_new_game(self):
        if self.game.state == "warmup":
            self.allready()
            self.msg("5 minutes have passed, the game is starting now.")

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4strictvql.py^7 - version {}, created by Thomas Jones on 11/02/2016.".format(self.plugin_version))
