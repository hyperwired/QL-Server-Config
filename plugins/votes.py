# This has been created by TomTec Solutions

import minqlx

specWasLastVoteCalled = "0"

class votes(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote_called", self.handle_vote_called)

    def handle_vote_called(self, caller, vote, args):
        global specWasLastVoteCalled
        if vote.lower() == "spec":
            specWasLastVoteCalled = "1"
            voteString = ("put {} spec".format(args))
            self.set_cvar("nextmap", voteString)
            caller.tell("Command initialised, you may now run ^2/cv nextmap^7 to start the vote. Any other vote will void this initialisation.")
            return minqlx.RET_STOP_ALL

        elif vote.lower() == "nextmap":
            if specWasLastVoteCalled == "0":
                self.set_cvar("nextmap", "")
                caller.tell("Nextmap is used for the ^2/cv spec^7 command. Issue a ^2/cv spec^7 for ^2/cv nextmap^7 to work.")
                return minqlx.RET_STOP_ALL
            else:
                specWasLastVoteCalled = "0"

        else:
            specWasLastVoteCalled = "0"
            self.set_cvar("nextmap", "")
