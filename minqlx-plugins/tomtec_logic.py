# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class tomtec_logic(minqlx.Plugin):
    def __init__(self):
        self.add_hook("new_game", self.new_game)
        self.add_hook("map", self.map_load)
        self.add_hook("game_countdown", self.game_countdown)
        self.add_hook("player_loaded", self.player_loaded)
        self.add_hook("game_start", self.game_start)
        self.add_hook("game_end", self.game_end)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_command(("help", "about", "version"), self.cmd_help)
        self.add_command("rules", self.cmd_showrules)
        self.add_command("giveall", self.cmd_giveall, 5, usage="<powerup [on/off]>, <holdable>")
        self.add_command("map_restart", self.cmd_maprestart, 1)
        self.add_command("muteall", self.cmd_muteall, 4)
        self.add_command("unmuteall", self.cmd_unmuteall, 4)
        self.add_command(("feedback", "fb"), self.cmd_feedback)
        self.add_command("killall", self.cmd_killall, 4)
        self.add_command("excessiveweaps", self.cmd_excessive_weaps, 5, usage="on/off")
        self.add_command("addbot", self.cmd_addbot, 1)
        self.add_command("rembot", self.cmd_rembot, 1)
        self.add_command("tomtec_versions", self.cmd_showversion)
        self.add_command("ruleset", self.cmd_ruleset, 5, usage="pql/vql")
        self.add_command(("wiki", "w"), self.cmd_wiki)

        self.set_cvar_once("qlx_excessive", "0")

        self.plugin_version = "2.2"

    def cmd_wiki(self, player, msg, channel):
        channel.reply("Visit ^2tomtecsolutions.com.au/thepurgery^7 to see ^4The Purgery^7's wiki.")
        
    def cmd_addbot(self, player, msg, channel):
        minqlx.console_command("addbot anarki 5 any 0 ^7Pur^4g^7obot")
        player.tell("Remember to ^2!rembot^7 when you're finished with your bot.")

    def cmd_rembot(self, player, msg, channel):
        minqlx.console_command("kick allbots")

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
            minqlx.console_command("map_restart")
            self.msg("PQL ruleset is now set.")

        if msg[1].lower() == "vql":
            minqlx.set_cvar("pmove_airControl", "0")
            minqlx.set_cvar("pmove_rampJump", "0")
            minqlx.set_cvar("weapon_reload_rg", "1500")
            minqlx.set_cvar("pmove_weaponRaiseTime", "200")
            minqlx.set_cvar("pmove_weaponDropTime", "200")
            minqlx.set_cvar("g_damage_lg", "6")
            minqlx.console_command("map_restart")
            self.msg("VQL ruleset is now set.")
            
    def cmd_muteall(self, player, msg, channel):
        # mute everybody on the server
        for p in self.players():
            p.mute()

    def cmd_unmuteall(self, player, msg, channel):
        # unmute everybody on the server
        for p in self.players():
            p.unmute()

    def cmd_killall(self, player, msg, channel):
        # kill everybody on the server
        for p in self.players():
            self.slay(p)
    
    def new_game(self):
        # brand the map
        server_number = (minqlx.get_cvar("net_port"))
        server_number = str(server_number[-1])
        if server_number == "7":
            server_number = "Test"
        else:
            server_number = "#{}".format(server_number)
            
        minqlx.set_configstring(3, "^4The Purgery^7 - {} - ^2{}".format(minqlx.get_cvar("sv_location"), server_number))
        minqlx.set_configstring(678, "Sponsored by ^5TomTec Solutions^7 (^2quakesupport@tomtecsolutions.com^7).")
        minqlx.set_configstring(679, "Visit our Facebook page at ^2http://fb.me/thepurgery^7, or the wiki at ^2http://tomtecsolutions.com.au/thepurgery^7.")

    def map_load(self, mapname, factory):
        # turn on infinite ammo for warm-up
        minqlx.set_cvar("g_infiniteAmmo", "1")     
        
    def game_countdown(self):
        # play the 'battle suit protect' sound, and display a sponsor message during the countdown
        minqlx.send_server_command(None, "cp \"^4The Purgery\n^7Sponsored by ^4TomTec Solutions^7\"\n")
        for p in self.players():
            p.powerups(battlesuit=10)
            p.noclip = True
            
        self.play_sound("sound/items/protect3.ogg")
       
        # disable infinite ammo after warm-up
        minqlx.set_cvar("g_infiniteAmmo", "0")
        
    def player_loaded(self, player):
        # display a message to a newly-loaded/connected player
        minqlx.send_server_command(player.id, "cp \"^7Welcome to ^4The Purgery^7\"\n")
        self.play_sound("tp_sounds/thomas/welcome_purgery.ogg", player)

        if (minqlx.get_cvar("qlx_excessive")) == "1":
            player.tell("Excessive weapons are ^2enabled^7. To disable them, ^2/cv excessive off^7.")
        
    def game_start(self):
        # make sure everyone's noclip is off
        for p in self.players():
            p.noclip = False
        
    def game_end(self, data):
        #channel.tell("Hurrah!")
        #self.play_sound("sound/items/protect3.ogg")
        pass

    def cmd_showrules(self, player, msg, channel):
        # show the rules to the channel from whence the command was issued
        player.tell("^4========================================================================================")
        player.tell("^4The Purgery^7 - ^3Server Rules:")
        player.tell("^7    1. No racism, neo-nazism, harassment or abuse toward other players via text or voice chat.")
        player.tell("^7    2. No disruptive behaviour of any kind, including 'spamming' and repetitive call-voting")
        player.tell("^7    3. No cheating, hacking or abuse of server privileges.")
        player.tell("^7    4. Lack of common sense is prohibited.")
        player.tell("^7    5. If you've been muted, you're obviously doing something that one or more server ops don't approve of.")
        player.tell("^7    6. These servers are being paid for by Sa^4t^7urn, and the donators that assist with the funding.")
        player.tell("^1  Failure to comply with these rules will result in a mute, a temporary ban, or a permanent ban.")
        player.tell("^7  Have ^2fun^7, play, enjoy, don't do anything stupid.")
        player.tell("^4========================================================================================")

    def cmd_help(self, player, msg, channel):
        player.tell("This server runs ^4tomtec_logic.py^7, a ^4minqlx^7 plugin designed for ^4The Purgery^7 servers.")
        player.tell("^4tomtec_logic.py^7 is (c) 2015, Thomas Jones (Sa^4t^7urn), TomTec Solutions.")
        player.tell("Please visit ^2http://tomtecsolutions.com.au/thepurgery^7 for information about the servers.")
        return minqlx.RET_STOP_EVENT

    def cmd_feedback(self, player, msg, channel):
        channel.reply("To provide feedback on ^4The Purgery^7 servers, please email ^2quakesupport@tomtecsolutions.com^7.")

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4tomtec_logic.py^7 - version {}, created by Thomas Jones on 01/11/2015.".format(self.plugin_version))
        
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

        if vote.lower() == "map":
            # prevent certain maps from being loaded, if they're found to have issues
            if args.lower() == "disabled_test":
                caller.tell("Map ^4{}^7 is currently disabled, as it breaks the server. ^4-- Sa^4t^7urn (27/11/15)".format(args.lower()))
                return minqlx.RET_STOP_ALL

        if vote.lower() == "silence":
            # enables the '/cv silence <id>' command
            try:
                player_name = self.player(int(args)).clean_name
                player_id = self.player(int(args)).id
            except:
                caller.tell("^1Invalid ID.^7 Use a client ID from the ^2/players^7 command.")
                return minqlx.RET_STOP_ALL

            self.callvote("qlx !silence {} 10 minutes You were call-voted silent for 10 minutes.; mute {}".format(player_id, player_id), "silence {} for 10 minutes".format(player_name))
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

    def handle_vote_ended(self, votes, vote, args, passed):
        self.msg("Vote results: ^2{}^7 - ^1{}^7.".format(votes[0], votes[1]))
        
        if passed:
            if vote.lower() == "map":
                self.msg("The map is changing to {}.".format(args))
                
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
                            
    def cmd_maprestart(self, player, msg, channel):
        # run a map restart
        minqlx.console_command("map_restart")
        
    def cmd_giveall(self, player, msg, channel):
        # enables the '!giveall' command, to provide all players with items/powerups/others
        holdTime = minqlx.get_cvar("roundtimelimit")
        if msg[1] == "kamikaze":
            for p in self.players():
                p.holdable = "kamikaze"
        elif msg[1] == "teleporter":
            for p in self.players():
                p.holdable = "teleporter"
        elif msg[1] == "portal":
            for p in self.players():
                p.holdable = "portal"
        elif msg[1] == "flight":
            for p in self.players():
                p.holdable = "flight"
        elif msg[1] == "quaddamage":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(quad=holdTime)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(quad=0)
        elif msg[1] == "regeneration":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(regeneration=holdTime)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(regeneration=0)
        elif msg[1] == "invisibility":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(invisibility=holdTime)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(invisibility=0)
        elif msg[1] == "haste":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(haste=holdTime)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(haste=0)
        elif msg[1] == "battlesuit":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(battlesuit=holdTime)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(battlesuit=0)
        elif msg[1] == "noclip":
            if msg[2] == "on":
                for p in self.players():
                    p.noclip = True
            if msg[2] == "off":
                for p in self.players():
                    p.noclip = False
