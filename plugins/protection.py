# This has been created by TomTec Solutions

import minqlx

class protection(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote_called", self.handle_vote_called)


    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "kick":

            if args.lower() == "zeobyte":
                caller.tell("^7Voting to kick the server owner is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL
            
            if args.lower() == "merozollo":
                caller.tell("^7Voting to kick a server administrator is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL


        if vote.lower() == "clientkick":

            caller.tell("^4clientkick^7 is disabled on this server. Use ^4kick^7 instead.")
            return minqlx.RET_STOP_ALL
