# Created by Thomas Jones on 26/03/2016 - thomas@tomtecsolutions.com
# This is a gamemode plugin and is utilised to modify some gameplay aspects.
# This plugin is released to everyone, for any purpose. It comes with no warranty, no guarantee it works, it's released AS IS.
# You can modify everything, except for lines 1-4 and the !tomtec_versions code. They're there to indicate I whacked this together originally. Please make it better :D


GAMEMODE_NAME = "Single Weapon CA"
CALLVOTE_STRING = "singleweapon"
SUPPORTED_GAMETYPES = ("ca")


import minqlx
class gamemode_singleweapon(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded, priority=minqlx.PRI_LOW)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("unload", self.handle_plugin_unload)
        self.add_command((self.__class__.__name__), self.cmd_gamemode_switch, 5, usage="on/off")
        self.add_command("tomtec_versions", self.cmd_showversion)
        self.gamemode_active = False

######### define your hooks/commands/stuff below
        self.plugin_version = "1.0"
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("game_end", self.handle_game_end)

    def incrementWeapons(self):
        if self.gamemode_active:
            current_weapons = self.get_cvar("g_startingWeapons", int)
            if (current_weapons >= 8192) or (current_weapons == 0):
                self.set_cvar("g_startingWeapons", str(1))
            else:
                current_weapons += current_weapons
                self.set_cvar("g_startingWeapons", str(current_weapons))

    def resetWeapons(self):
        if self.gamemode_active:
            self.set_cvar("g_startingWeapons", "8447")
            self.set_cvar("g_infiniteAmmo", "0")

    def handle_round_end(self, *args, **kwargs): 
        self.incrementWeapons()

    @minqlx.next_frame
    def handle_game_countdown(self, *args, **kwargs):
        if self.gamemode_active:
            self.set_cvar("g_startingWeapons", "0")
            self.set_cvar("g_infiniteAmmo", "1")
        self.incrementWeapons()

    def handle_game_end(self, *args, **kwargs):
        self.resetWeapons()
            
    def housekeeping_tasks(self): # runs when the plugin unloads and when the mode is call-voted off
        self.resetWeapons()
        return

        
### Don't touch the below, it morphs to your code:
    def handle_plugin_unload(self, plugin):
        if plugin == (self.__class__.__name__):
            self.gamemode_active == False
            self.housekeeping_tasks()
            
    def cmd_gamemode_switch(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        if msg[1].lower() == "on":
            self.gamemode_active = True
        elif msg[1].lower() == "off":
            self.gamemode_active = False
            self.housekeeping_tasks()
        else:
            return minqlx.RET_USAGE
    
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
        channel.reply("^4{}.py^7 - version {}, created by Thomas Jones on 10/08/2016.".format(self.__class__.__name__, self.plugin_version))

        
        
