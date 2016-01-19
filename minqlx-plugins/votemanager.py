# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class votemanager(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote", self.handle_vote)
        self.add_hook("vote_ended", self.handle_vote_ended)

        self.add_command("tomtec_versions", self.cmd_showversion)
        
        self.has_voted = []

        self.plugin_version = "1.0"

    def handle_vote_called(self, caller, vote, args):
        self.has_voted.append(caller)
                
    def handle_vote(self, player, yes):
        if not self.is_vote_active():
            return
        
        if player in self.has_voted:
            ident = player.steam_id
            if (player.privileges != None or self.db.has_permission(ident, 3)):
                minqlx.force_vote(yes)
                if yes:
                    word = "passed"
                else:
                    word = "vetoed"
                    
                self.msg("{}^7 {} the vote.".format(player.name, word))

        self.has_voted.append(player)
        
        if (player.privileges != None):
            if yes:
                yes_votes = int(minqlx.get_configstring(10))
                yes_votes += 1
                minqlx.set_configstring(10, str(yes_votes))
            else:
                no_votes = int(minqlx.get_configstring(11))
                no_votes += 1
                minqlx.set_configstring(11, str(no_votes))
            return minqlx.RET_STOP_ALL
                
        #self.msg("self.has_voted == {}".format(str(self.has_voted)))

    def handle_vote_ended(self, votes, vote, args, passed):
        self.has_voted = []

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4votemanager.py^7 - version {}, created by Thomas Jones on 19/01/2016.".format(self.plugin_version))
