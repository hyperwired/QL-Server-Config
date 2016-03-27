# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Player selection system for short-mid-long range weapon distribution created by zlr.

GAMEMODE_NAME = "Tri-Weapon CA"
CALLVOTE_STRING = "triweapon"
SUPPORTED_GAMETYPES = ("ca")


import minqlx, random
class gamemode_triweapon(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded, priority=minqlx.PRI_LOW)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("unload", self.handle_plugin_unload)
        self.add_command((self.__class__.__name__), self.cmd_gametype_switch, 5, usage="on/off")
        self.add_command("tomtec_versions", self.cmd_showversion)
        self.gamemode_active = False

######### define your hooks/commands/stuff below
        self.plugin_version = "1.1"
        self.add_hook("round_countdown", self.handle_round_countdown)
    

    def handle_round_countdown(self, *args, **kwargs): 
        if self.gamemode_active == True:
            for team in self.teams():
                if (team != "spectator") or (team != "free"):
                    teams = self.teams()
                    close_range_counter = 0
                    toggle = 1
                    for player in teams[team]:
                        if close_range_counter <= 2: # close-range
                            player.weapons(reset=True, g=True, rl=True, gl=True, mg=True)
                            close_range_counter += 1
                        else:
                            if toggle == 1: # mid-range
                                player.weapons(reset=True, g=True, lg=True, sg=True, hmg=True)
                                toggle = 0
                            else: # long-range
                                player.weapons(reset=True, g=True, rg=True, sg=True, pg=True)
                                toggle = 1
                
            
    def housekeeping_tasks(self): # runs when the plugin unloads and when the mode is call-voted off
        return

        
### Don't touch the below, it morphs to your code:
    def handle_plugin_unload(self, plugin):
        if plugin == (self.__class__.__name__):
            self.gamemode_active == False
            self.housekeeping_tasks()
            
    def cmd_gametype_switch(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        if msg[1].lower() == "on":
            self.gamemode_active = True
        elif msg[1].lower() == "off":
            self.gamemode_active = False
            self.housekeeping_tasks()
        else:
            return minqlx.RET_USAGE

        return minqlx.RET_STOP_ALL
    
    def handle_vote_called(self, caller, vote, args):
        if not (self.get_cvar("g_allowSpecVote", bool)) and caller.team == "spectator":
            if caller.privileges == None:
                caller.tell("You are not allowed to call a vote as spectator.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "gamemode":
            if args.split()[0].lower() == CALLVOTE_STRING:
                if len(args.split()) <= 1:
                    caller.tell("^2/cv gamemode {} [on/off]^7 is the usage for this callvote gamemode command.".format(CALLVOTE_STRING))
                elif (args.split()[1].lower() == "on") or (args.split()[1].lower() == "off"):
                    if self.game.type_short in SUPPORTED_GAMETYPES:
                        self.callvote("qlx !{} {}".format(self.__class__.__name__, args.split()[1].lower()), "gamemode {}: {}".format(GAMEMODE_NAME, args.split()[1].lower()))
                        self.msg("{}^7 called a vote.".format(caller.name))
                    else:
                        caller.tell("The ^4{}^7 gamemode is not supported on this gametype.".format(GAMEMODE_NAME))
                else:
                    caller.tell("^2/cv gamemode {} [on/off]^7 is the usage for this callvote gamemode command.".format(CALLVOTE_STRING))

                return minqlx.RET_STOP_ALL
            
    @minqlx.delay(3)
    def handle_player_loaded(self, player):
        if self.gamemode_active == True:
            player.tell("This server has ^4{}^7 mode enabled. To disable it, use ^2/cv gamemode {} off^7.".format(GAMEMODE_NAME, CALLVOTE_STRING))

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4{}.py^7 - version {}, created by Thomas Jones on 26/03/2016.".format(self.__class__.__name__, self.plugin_version))

        
        
