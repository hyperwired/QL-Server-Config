# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Some of the votes here rely on the tomtec_logic plugin (ruleset for example).
# custom_votes.py - a minqlx plugin to enable the ability to have custom vote functionality in-game.

import minqlx

class custom_votes(minqlx.Plugin):
    def __init__(self):
        self.add_hook("vote_called", self.handle_vote_called)

        self.add_command("tomtec_versions", self.cmd_showversion)
        
        self.plugin_version = "1.1"

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4custom_votes.py^7 - version {}, created by Thomas Jones on 01/01/2016.".format(self.plugin_version))
        
    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "kick":
            # prevent certain players from being kicked via a call-vote
            playerName = args.lower()
            if playerName == "saturn":
                caller.tell("^7Voting to kick the server owner is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL
            if playerName == "merozollo":
                caller.tell("^7Voting to kick a server administrator is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL
            if playerName == "0regonn":
                caller.tell("^7Voting to kick a protected player is prohibited. This incident has been recorded.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "clientkick":
            # disable client-kick, as it interferes with player protection
            caller.tell("^7Voting from the in-game menu/clientkick is disabled, as it conflicts with the player protection system.")
            caller.tell("^7Please use the ^2/cv^7 or ^2/callvote^7 console commands.")
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

        if vote.lower() == "silence":
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

        def cmd_showversion(self, player, msg, channel):
            channel.reply("^4custom_votes.py^7 - version {}, created by Thomas Jones on 01/01/2016.".format(self.plugin_version))
