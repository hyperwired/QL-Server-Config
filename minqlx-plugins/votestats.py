# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Created by Thomas Jones on 01/01/2016 - thomas@tomtecsolutions.com
# votestats.py - a minqlx plugin to show who votes yes or no in-game/vote results.

"""
If you want to re-privatise votes, set the following cvar to 1: qlx_privatiseVotes
"""

import minqlx

class votestats(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote", self.process_vote, priority=minqlx.PRI_LOWEST)
        self.add_hook("vote_ended", self.handle_vote_ended, priority=minqlx.PRI_LOWEST)
        
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.set_cvar_once("qlx_privatiseVotes", "0")
        self.plugin_version = "1.5"

        self.has_voted = []

    def process_vote(self, player, yes):
        if (self.get_cvar("qlx_privatiseVotes", bool)):
            return
        
        if player in self.has_voted:
            return
        
        if yes:
            word = "^2yes"
        else:
            word = "^1no"
            
        self.msg("{}^7 voted {}^7.".format(player.name, word))
        self.has_voted.append(player)

    def handle_vote_ended(self, votes, vote, args, passed):
        self.has_voted = []
        self.msg("Vote results: ^2{}^7 - ^1{}^7.".format(*votes))
        
        if passed:
            if vote.lower() == "map":
                changingToMapAndMode = args.lower().split()
                if len(changingToMapAndMode) > 1:
                    theMsg = "The map is changing to ^4{}^7, with new game type ^4{}^7.".format(changingToMapAndMode[0], changingToMapAndMode[1])
                else:
                    theMsg = "The map is changing to ^4{}^7.".format(changingToMapAndMode[0])

                self.msg(theMsg)
    
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4votestats.py^7 - version {}, created by Thomas Jones on 01/01/2016.".format(self.plugin_version))
