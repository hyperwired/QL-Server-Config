# This has been created by TomTec Solutions

import minqlx

class protection(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote_called", self.handle_vote_called)


    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "kick":
    
            playerName = args.lower()
            
            if playerName == "zeobyte":
                caller.tell("^7Voting to kick the server owner is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL
            
            if playerName == "merozollo":
                caller.tell("^7Voting to kick a server administrator is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL

            if playerName == "0regonn":
                caller.tell("^7Voting to kick a protected player is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL


        if vote.lower() == "clientkick":

            caller.tell("^7Voting from the in-game menu/clientkick is disabled, as it conflicts with the player protection system.")
            caller.tell("^7Please use the ^2/cv^7/^2/callvote^7 console commands.")
            return minqlx.RET_STOP_ALL
            
