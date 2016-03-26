# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

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
        self.plugin_version = "1.0"
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("game_end", self.handle_game_end)
        self.original_startingweapons = self.get_cvar("g_startingWeapons") # is usually 8447 in CA
        self.weapons_bitfield_values = [2, 4, 8, 16, 32, 64, 128, 256, 1024, 4096, 8192] # mg, sg, gl, rl, lg, rg, pg, bfg, cg, ng, hmg

    def selectWeapons(self):
        _weapons_bitfield_values = self.weapons_bitfield_values
        randomWeapons = random.sample(range(0, len(_weapons_bitfield_values)), 3)
        weapons = []
        weapons.append(_weapons_bitfield_values[randomWeapons[0]])
        weapons.append(_weapons_bitfield_values[randomWeapons[1]])
        weapons.append(_weapons_bitfield_values[randomWeapons[2]])
        return weapons

    def handle_game_end(self, *args, **kwargs):
        self.set_cvar("g_startingWeapons", self.original_startingweapons)
        
    def handle_game_countdown(self, *args, **kwargs):
        if self.gamemode_active == True:
            weapons = self.selectWeapons()
            bitfield_value = 0
            for weapon in weapons:
                bitfield_value += weapon
            bitfield_value += 1 # add gauntlet
            self.set_cvar("g_startingWeapons", bitfield_value)

    def handle_round_end(self, *args, **kwargs):
        if self.gamemode_active == True:
            weapons = self.selectWeapons()
            bitfield_value = 0
            for weapon in weapons:
                bitfield_value += weapon
            bitfield_value += 1 # add gauntlet
            self.set_cvar("g_startingWeapons", bitfield_value)
            
    def housekeeping_tasks(self): # runs when the plugin unloads
        self.set_cvar("g_startingWeapons", self.original_startingweapons)

        
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

        
        
