# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# custom_votes.py - a minqlx plugin to enable the ability to have custom vote functionality in-game.

import minqlx

class custom_votes(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("player_loaded", self.player_loaded)

        self.add_command("tomtec_versions", self.cmd_showversion)
        self.add_command("excessiveweaps", self.cmd_excessive_weaps, 5, usage="on/off")
        self.add_command("ruleset", self.cmd_ruleset, 5, usage="pql/vql")

        self.set_cvar_once("qlx_rulesetLocked", "0")
        self.set_cvar_once("qlx_excessive", "0")
        self.set_cvar_once("qlx_disablePlayerRemoval", "0")
        
        self.plugin_version = "1.3"

    def player_loaded(self, player):
        if (self.get_cvar("qlx_excessive", bool)):
            player.tell("Excessive weapons are ^2enabled^7. To disable them, ^2/cv excessive off^7.")
            
    def cmd_ruleset(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        if msg[1].lower() == "pql":
            minqlx.set_cvar("pmove_airControl", "1")
            minqlx.set_cvar("pmove_rampJump", "1")
            minqlx.set_cvar("weapon_reload_rg", "1200")
            minqlx.set_cvar("pmove_weaponRaiseTime", "10")
            minqlx.set_cvar("pmove_weaponDropTime", "10")
            minqlx.set_cvar("g_damage_lg", "7")
            minqlx.set_cvar("dmflags", "60")
            if self.game.type_short == "ca":
                minqlx.set_cvar("g_startingHealth", "200")
                minqlx.set_cvar("g_startingArmor", "200")
            minqlx.console_command("map_restart")
            self.msg("PQL ruleset is now set.")

        if msg[1].lower() == "vql":
            minqlx.set_cvar("pmove_airControl", "0")
            minqlx.set_cvar("pmove_rampJump", "0")
            minqlx.set_cvar("weapon_reload_rg", "1500")
            minqlx.set_cvar("pmove_weaponRaiseTime", "200")
            minqlx.set_cvar("pmove_weaponDropTime", "200")
            minqlx.set_cvar("g_damage_lg", "6")
            if self.game.type_short == "ca":
                minqlx.set_cvar("dmflags", "28")
            else:
                minqlx.console_command("reset dmflags")
            minqlx.console_command("reset g_startingHealth")
            minqlx.console_command("reset g_startingArmor")
            minqlx.console_command("map_restart")
            self.msg("VQL ruleset is now set.")

    def cmd_excessive_weaps(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        if msg[1] == "on":
            minqlx.set_cvar("weapon_reload_sg", "200")
            minqlx.set_cvar("weapon_reload_rl", "200")
            minqlx.set_cvar("weapon_reload_rg", "50")
            minqlx.set_cvar("weapon_reload_prox", "200")
            minqlx.set_cvar("weapon_reload_pg", "40")
            minqlx.set_cvar("weapon_reload_ng", "800")
            minqlx.set_cvar("weapon_reload_mg", "40")
            minqlx.set_cvar("weapon_reload_hmg", "40")
            minqlx.set_cvar("weapon_reload_gl", "200")
            minqlx.set_cvar("weapon_reload_gauntlet", "100")
            minqlx.set_cvar("weapon_reload_cg", "30")
            minqlx.set_cvar("weapon_reload_bfg", "75")
            minqlx.set_cvar("qlx_excessive", "1")
            self.msg("Excessive weapons are enabled.")
        if msg[1] == "off":
            minqlx.console_command("reset weapon_reload_sg")
            minqlx.console_command("reset weapon_reload_rl")
            if (minqlx.get_cvar("pmove_airControl")) == "1":
                minqlx.set_cvar("weapon_reload_rg", "1200")
            else:
                minqlx.console_command("reset weapon_reload_rg")
            minqlx.console_command("reset weapon_reload_prox")
            minqlx.console_command("reset weapon_reload_pg")
            minqlx.console_command("reset weapon_reload_ng")
            minqlx.console_command("reset weapon_reload_mg")
            minqlx.console_command("reset weapon_reload_hmg")
            minqlx.console_command("reset weapon_reload_gl")
            minqlx.console_command("reset weapon_reload_gauntlet")
            minqlx.console_command("reset weapon_reload_cg")
            minqlx.console_command("reset weapon_reload_bfg")
            minqlx.set_cvar("qlx_excessive", "0")
            self.msg("Excessive weapons are disabled.")
            
    def handle_vote_called(self, caller, vote, args):
        if not (self.get_cvar("g_allowSpecVote", bool)) and caller.team == "spectator":
            if caller.privileges == None:
                caller.tell("You are not allowed to call a vote as spectator.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "infiniteammo":
            # enables the '/cv infiniteammo [on/off]' command
            if args.lower() == "off":
                self.callvote("set g_infiniteAmmo 0", "infinite ammo: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_infiniteAmmo 1", "infinite ammo: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv infiniteammo [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "freecam":
            # enables the '/cv freecam [on/off]' command
            if args.lower() == "off":
                self.callvote("set g_teamSpecFreeCam 0", "team spectator free-cam: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_teamSpecFreeCam 1", "team spectator free-cam: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv freecam [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "floordamage":
            # enables the '/cv floordamage [on/off]' command
            if args.lower() == "off":
                self.callvote("set g_forceDmgThroughSurface 0", "damage through floor: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_forceDmgThroughSurface 1", "damage through floor: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv floordamage [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "alltalk":
            # enables the '/cv alltalk [on/off]' command
            if args.lower() == "off":
                self.callvote("set g_allTalk 0", "voice comm between teams: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_allTalk 1", "voice comm between teams: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv alltalk [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "allready":
            # enables the '/cv allready' command
            if self.game.state == "warmup":
                self.callvote("allready", "begin game immediately")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("You can't vote to begin the game when the game is already on.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "ruleset":
            # enables the '/cv ruleset [pql/vql]' command
            if (minqlx.get_cvar("qlx_rulesetLocked")) == "1":
                caller.tell("Voting to change the ruleset is disabled on ruleset-locked servers.")
                return minqlx.RET_STOP_ALL

            if args.lower() == "pql":
                self.callvote("qlx !ruleset pql", "ruleset: pql")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "vql":
                self.callvote("qlx !ruleset vql", "ruleset: vql")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv ruleset [pql/vql]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL
            
        if vote.lower() == "abort":
            # enables the '/cv abort' command
            if self.game.state != "warmup":
                self.callvote("abort", "abort the game", 30)
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("You can't vote to abort the game when the game isn't in progress.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "chatsounds":
            # enables the '/cv chatsounds [on/off]' command
            if args.lower() == "off":
                self.callvote("qlx !unload fun", "chat-activated sounds: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("qlx !load fun", "chat-activated sounds: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv chatsounds [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() in ("silence", "mute"):
            # enables the '/cv silence <id>' command
            try:
                player_name = self.player(int(args)).clean_name
                player_id = self.player(int(args)).id
            except:
                caller.tell("^1Invalid ID.^7 Use a client ID from the ^2/players^7 command.")
                return minqlx.RET_STOP_ALL

            if self.get_cvar("qlx_serverExemptFromModeration") == "1":
                caller.tell("This server has the serverExemptFromModeration flag set, and therefore, silencing is disabled.")
                return minqlx.RET_STOP_ALL
            
            self.callvote("qlx !silence {} 10 minutes You were call-voted silent for 10 minutes.; mute {}".format(player_id, player_id), "silence {} for 10 minutes".format(player_name))
            self.msg("{}^7 called a vote.".format(caller.name))
            return minqlx.RET_STOP_ALL

        if vote.lower() == "tempban":
            # enables the '/cv tempban <id>' command
            if self.get_cvar("qlx_disablePlayerRemoval", bool):
                if caller.privileges == None:
                    caller.tell("Voting to kick/clientkick is disabled in this server due to repeated misuse.")
                    caller.tell("^2/cv spec <id>^7 and ^2/cv silence <id>^7 exist as substitutes to kicking.")
                    caller.tell("If you believe a player requires further attention, consult a mod/admin in-game or over ^2!world^7.")
                    return minqlx.RET_STOP_ALL
            try:
                player_name = self.player(int(args)).clean_name
                player_id = self.player(int(args)).id
            except:
                caller.tell("^1Invalid ID.^7 Use a client ID from the ^2/players^7 command.")
                return minqlx.RET_STOP_ALL

            if self.player(int(args)).privileges != None:
                caller.tell("The player specified is an admin, a mod or banned, and cannot be tempbanned.")
                return minqlx.RET_STOP_ALL
            
            self.callvote("tempban {}".format(player_id), "^1ban {} until the map changes^3".format(player_name))
            self.msg("{}^7 called a vote.".format(caller.name))
            return minqlx.RET_STOP_ALL

        if vote.lower() == "spec":
            # enables the '/cv spec <id>' command
            try:
                player_name = self.player(int(args)).clean_name
                player_id = self.player(int(args)).id
            except:
                caller.tell("^1Invalid ID.^7 Use a client ID from the ^2/players^7 command.")
                return minqlx.RET_STOP_ALL

            if self.player(int(args)).team == "spectator":
                caller.tell("That player is already in the spectators.")
                return minqlx.RET_STOP_ALL
            
            self.callvote("put {} spec".format(player_id), "move {} to the spectators".format(player_name))
            self.msg("{}^7 called a vote.".format(caller.name))
            return minqlx.RET_STOP_ALL

        if vote.lower() == "excessive":
            # enables the '/cv excessive [on/off]' command
            if args.lower() == "off":
                self.callvote("qlx !excessiveweaps off", "excessive weapons: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("qlx !excessiveweaps on", "excessive weapons: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv excessive [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() in ("kick", "clientkick"):
            if self.get_cvar("qlx_disablePlayerRemoval", bool):
                if caller.privileges == None:
                    caller.tell("Voting to kick/clientkick is disabled in this server due to repeated misuse.")
                    caller.tell("^2/cv spec <id>^7 and ^2/cv silence <id>^7 exist as substitutes to kicking.")
                    caller.tell("If you believe a player requires further attention, consult a mod/admin in-game or over ^2!world^7.")
                    return minqlx.RET_STOP_ALL
                
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4custom_votes.py^7 - version {}, created by Thomas Jones on 01/01/2016.".format(self.plugin_version))

