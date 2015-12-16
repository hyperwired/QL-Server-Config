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
        self.add_command(("help", "about", "version"), self.cmd_help)
        self.add_command("rules", self.cmd_showrules)
        self.add_command("giveall", self.cmd_giveall, 5)
        self.add_command("map_restart", self.cmd_maprestart, 3)
        self.add_command("muteall", self.cmd_muteall, 4)
        self.add_command("unmuteall", self.cmd_unmuteall, 4)
        self.add_command(("feedback", "fb"), self.cmd_feedback)
        self.add_command("killall", self.cmd_killall, 4)
        self.add_command("excessiveweaps", self.cmd_excessive_weaps, 5, usage="on/off")
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.9"
        
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
        minqlx.set_configstring(3, "^4The Purgery^7 - {} - #{}".format(minqlx.get_cvar("sv_location"), server_number))
        minqlx.set_configstring(678, "Sponsored by ^5TomTec Solutions^7 (^2quakesupport@tomtecsolutions.com^7).")
        minqlx.set_configstring(679, "Visit our IRC channel on QuakeNet, ^4#thepurgery^7. Visit our Facebook page at ^2http://fb.me/thepurgery^7.")

    def map_load(self, mapname, factory):
        # turn on infinite ammo for warm-up
        minqlx.set_cvar("g_infiniteAmmo", "1")     
        
    def game_countdown(self):
        # play the 'battle suit protect' sound, and display a sponsor message during the countdown
        minqlx.send_server_command(None, "cp \"^4The Purgery\n^7Sponsored by ^4TomTec Solutions^7\"\n")
        for p in self.players():
            p.powerups(battlesuit=10000)
            p.noclip = True
            
        self.play_sound("sound/items/protect3.ogg")
       
        # disable infinite ammo after warm-up
        minqlx.set_cvar("g_infiniteAmmo", "0")
        
    def player_loaded(self, player):
        # display a message to a newly-loaded/connected player
        minqlx.send_server_command(player.id, "cp \"^7Welcome to ^4The Purgery^7\"\n")
        self.play_sound("tp_sounds/thomas/welcome_purgery.ogg", player)
        
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
                self.callvote("set g_infiniteAmmo 0", "infinite ammo: off", 30)
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_infiniteAmmo 1", "infinite ammo: on", 30)
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv infiniteammo [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "freecam":
            # enables the '/cv freecam [on/off]' command
            if args.lower() == "off":
                self.callvote("set g_teamSpecFreeCam 0", "team spectator free-cam: off", 30)
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_teamSpecFreeCam 1", "team spectator free-cam: on", 30)
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv freecam [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "alltalk":
            # enables the '/cv alltalk [on/off]' command
            if args.lower() == "off":
                self.callvote("set g_allTalk 0", "voice comm between teams: off", 30)
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set g_allTalk 1", "voice comm between teams: on", 30)
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv alltalk [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "allready":
            # enables the '/cv allready' command
            if self.game.state == "warmup":
                self.callvote("allready", "begin game immediately", 30)
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("You can't vote to begin the game when the game is already on.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "abort":
            # enables the '/cv abort' command
            if self.game.state != "warmup":
                self.callvote("abort", "abort the game", 30)
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("You can't vote to abort the game when the game isn't in progress.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "chatsounds":
            # enables the '/cv chatsounds [on/off]' command
            if args.lower() == "off":
                self.callvote("qlx !unload fun", "chat-activated sounds: off", 30)
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("qlx !load fun", "chat-activated sounds: on", 30)
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
            return minqlx.RET_STOP_ALL

        if vote.lower() == "excessive":
            # enables the '/cv excessive [on/off]' command
            if args.lower() == "off":
                self.callvote("qlx !excessiveweaps off", "excessive weapons: off")
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("qlx !excessiveweaps on", "excessive weapons: on")
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv excessive [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

    def cmd_excessive_weaps(self, player, msg, channel):
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
        if msg[1] == "off":
            minqlx.set_cvar("weapon_reload_sg", "1000")
            minqlx.set_cvar("weapon_reload_rl", "800")
            minqlx.set_cvar("weapon_reload_rg", "1500")
            minqlx.set_cvar("weapon_reload_prox", "800")
            minqlx.set_cvar("weapon_reload_pg", "100")
            minqlx.set_cvar("weapon_reload_ng", "1000")
            minqlx.set_cvar("weapon_reload_mg", "100")
            minqlx.set_cvar("weapon_reload_hmg", "75")
            minqlx.set_cvar("weapon_reload_gl", "800")
            minqlx.set_cvar("weapon_reload_gauntlet", "400")
            minqlx.set_cvar("weapon_reload_cg", "50")
            minqlx.set_cvar("weapon_reload_bfg", "300")
            

                            
    def cmd_maprestart(self, player, msg, channel):
        # run a map restart
        minqlx.console_command("map_restart")
        
    def cmd_giveall(self, player, msg, channel):
        # enables the 'giveall' command, to provide all players with items/powerups/others
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
                    p.powerups(quad=1000000000)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(quad=0)
        elif msg[1] == "regeneration":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(regeneration=1000000000)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(regeneration=0)
        elif msg[1] == "invisibility":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(invisibility=1000000000)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(invisibility=0)
        elif msg[1] == "haste":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(haste=1000000000)
            if msg[2] == "off":
                for p in self.players():
                    p.powerups(haste=0)
        elif msg[1] == "battlesuit":
            if msg[2] == "on":
                for p in self.players():
                    p.powerups(battlesuit=1000000000)
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
