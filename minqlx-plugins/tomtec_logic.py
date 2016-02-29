# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx
from random import randint

class tomtec_logic(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_hook("game_countdown", self.game_countdown)
        self.add_hook("game_start", self.game_start)
        self.add_hook("game_end", self.game_end)
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote_started", self.handle_vote_started)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_command(("help", "about", "version"), self.cmd_help)
        self.add_command("rules", self.cmd_showrules)
        self.add_command("giveall", self.cmd_giveall, 5, usage="<powerup [on/off]>, <holdable>")
        self.add_command("map_restart", self.cmd_maprestart, 1)
        self.add_command("muteall", self.cmd_muteall, 4)
        self.add_command("unmuteall", self.cmd_unmuteall, 4)
        self.add_command(("feedback", "f"), self.cmd_feedback)
        self.add_command("killall", self.cmd_killall, 4)
        self.add_command("addbot", self.cmd_addbot, 1)
        self.add_command("rembot", self.cmd_rembot, 1)
        self.add_command("tomtec_versions", self.cmd_showversion)
        self.add_command(("wiki", "w"), self.cmd_wiki)
        self.add_command(("facebook", "fb"), self.cmd_facebook)
        self.add_command(("acommands", "acmds"), self.cmd_acommands)
    
        self.disabled_maps = ["proq3dm6", "ra3map1", "ra3map6"]
        
        self.set_cvar_once("qlx_freezePlayersDuringVote", "0")
        self.set_cvar_once("qlx_strictVql", "0")
        self.set_cvar_once("qlx_ratingLimiter", "0")
        
        self.plugin_version = "3.2"

        self.surprise_infected = False
        
        if self.get_cvar("qlx_strictVql", bool):
            minqlx.load_plugin("strictvql")
        
        if self.get_cvar("qlx_ratingLimiter", bool):
            minqlx.load_plugin("ratinglimiter")
        
    def cmd_wiki(self, player, msg, channel):
        channel.reply("Visit ^2thepurgery.com^7 to see ^4The Purgery^7's wiki and documentation.")

    def cmd_facebook(self, player, msg, channel):
        channel.reply("Visit ^2fb.me/thepurgery^7 to see ^4The Purgery^7's Facebook page.")
        
    def cmd_addbot(self, player, msg, channel):
        minqlx.console_command("addbot anarki 5 any 0 ^7Pur^4g^7obot")
        player.tell("Remember to ^2!rembot^7 when you're finished with your bot.")

    def cmd_rembot(self, player, msg, channel):
        minqlx.console_command("kick allbots")
            
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

    @minqlx.next_frame
    def handle_player_loaded(self, player):
        #if player.steam_id == minqlx.owner(): # purger is here, sound effect
        #    self.play_sound("q3_audio/sounds/xaero_deathchime.wav")
            
        if str(player.steam_id) == "76561197960279482": # cryptix is here
            player.name = "^4crypt^7ix"

        if self.surprise_infected:
            player.tell("Surprise ^1Infected^7!")
            self.center_print("Surprise ^1Infected^7!", player.id)
            self.play_sound("sound/vo_evil/infected.wav", player.id)

    @minqlx.next_frame   
    def map_load(self, mapname, factory):
        # turn on infinite ammo for warm-up
        minqlx.set_cvar("g_infiniteAmmo", "1")
        if self.get_cvar("pmove_airControl", bool):
            chance = randint(0,50)
            if chance == 25:
                self.surprise_infected = True
                self.msg("Switched to Surprise ^1Infected^7.")
                self.change_map(mapname, "pqlinfected")

        
    def game_countdown(self):
        self.play_sound("sound/items/protect3.ogg")
        minqlx.set_cvar("g_infiniteAmmo", "0")

    def game_end(self, data):
        self.surprise_infected = False

    def game_start(self, data):
        # make sure everyone's noclip is off
        for p in self.players():
            p.noclip = False
        self.set_cvar("g_speed", "320")

    def cmd_showrules(self, player, msg, channel):
        # show the rules to the channel from whence the command was issued
        player.tell("^4========================================================================================")
        player.tell("^4The Purgery^7 - ^3Server Rules:")
        player.tell("^7    1. No racism, neo-nazism, harassment or abuse toward other players via text or voice chat.")
        player.tell("^7    2. No disruptive behaviour of any kind, including 'spamming' and repetitive call-voting")
        player.tell("^7    3. No cheating, hacking or abuse of server privileges.")
        player.tell("^7    4. Lack of common sense is prohibited.")
        player.tell("^7    5. If you've been muted, you're obviously doing something that one or more server ops don't approve of.")
        player.tell("^7    6. These servers are being paid for by Pur^4g^7er, and the donators that assist with the funding.")
        player.tell("^1  Failure to comply with these rules will result in a mute, a temporary ban, or a permanent ban.")
        player.tell("^7  Have ^2fun^7, play, enjoy, don't do anything stupid.")
        player.tell("^4========================================================================================")

    def cmd_help(self, player, msg, channel):
        player.tell("This server runs ^4tomtec_logic.py^7, a ^4minqlx^7 plugin designed for ^4The Purgery^7 servers.")
        player.tell("^4tomtec_logic.py^7 is (c) 2015, Thomas Jones (Pur^4g^7er), TomTec Solutions.")
        player.tell("Please visit ^2http://tomtecsolutions.com.au/thepurgery^7 for information about the servers.")
        return minqlx.RET_STOP_EVENT

    def cmd_acommands(self, player, msg, channel):
        channel.reply("To see mod/admin commands, check out ^2thepurgery.com^7.")


    def cmd_feedback(self, player, msg, channel):
        channel.reply("To provide feedback on ^4The Purgery^7 servers, please email ^2thomas@tomtecsolutions.com^7.")

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4tomtec_logic.py^7 - version {}, created by Thomas Jones on 01/11/2015.".format(self.plugin_version))

    def handle_vote_called(self, caller, vote, args):            
        if vote.lower() == "map":
            # prevent certain maps from being loaded, if they're found to have issues
            if args.lower() is "disabled_test" or args.lower() in self.disabled_maps:
                caller.tell("Map ^4{}^7 is currently disabled, please contact an admin/mod for details.".format(args.lower()))
                return minqlx.RET_STOP_ALL

    def handle_vote_started(self, caller, vote, args):
        if self.game.state == "warmup":
            if self.get_cvar("qlx_freezePlayersDuringVote", bool):
                self.set_cvar("g_speed", "0")
                self.play_sound("sound/world/klaxon1.wav")
                minqlx.send_server_command(None, "cp \"^7PLEASE VOTE NOW\nPLAYER MOVEMENT IS DISABLED\nUNTIL THE VOTE ENDS\"\n")
        else:
            minqlx.send_server_command(None, "cp \"^7PLEASE VOTE NOW\"\n")
            
    def handle_vote_ended(self, votes, vote, args, passed):
        if passed:
            if vote == "map":
                self.surprise_infected = False
            minqlx.send_server_command(None, "cp \"^2VOTE PASSED^7\"\n")
        else:
            minqlx.send_server_command(None, "cp \"^1VOTE FAILED^7\"\n")
        self.set_cvar("g_speed", "320")
        
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
