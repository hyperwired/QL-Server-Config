# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Created by Thomas Jones on 17/12/2015 - thomas@tomtecsolutions.com
# voteshow.py - a minqlx plugin to show who votes yes or no in-game.

import minqlx

class voteshow(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote", self.process_vote, priority=minqlx.PRI_LOWEST)
        self.add_command("tomtec_versions", self.cmd_showversion)
        
        self.plugin_version = "1.0"


    def process_vote(self, player, yes):
        if yes:
            word = "^2yes"
        else:
            word = "^1no"
            
        self.msg("{}^7 voted {}^7.".format(player, word))
    
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4voteshow.py^7 - version {}, created by Thomas Jones on 18/12/2015.".format(self.plugin_version))
