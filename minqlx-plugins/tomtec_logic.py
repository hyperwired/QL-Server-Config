# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

OWNER_NAME="^7Pur^4g^7er" # used to define the owner's name, this name must = the minqlx.owner()'s name.

GAME_MODERATORS="merozollo, 0regonn, barley, Biokemical, Quarrel, meganfoxxed, Jubblies, zee" # string that displays on player load after a delay
ZERO_WIDTH_SPACE=u"\u200B" # part of the userinfo filtering to prevent illegal names
REG_WIDTH_SPACE=u"\u2002"

import minqlx, datetime, time, subprocess
from random import randint

class tomtec_logic(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_hook("game_countdown", self.game_countdown)
        self.add_hook("game_start", self.game_start)
        self.add_hook("game_end", self.game_end)
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_HIGHEST)
        #self.add_hook("player_spawn", self.handle_player_spawn) disable battle-suits per spawn
        self.add_hook("vote_called", self.handle_vote_called) # to add custom votes
        self.add_hook("vote_started", self.handle_vote_started)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("chat", self.handle_chat)
        self.add_hook("userinfo", self.handle_userinfo, priority=minqlx.PRI_HIGHEST) # to prevent illegal name changes
        
        self.add_command(("help", "about", "version"), self.cmd_help)
        self.add_command("banyoyza", self.cmd_banyoyza)
        self.add_command("rules", self.cmd_showrules)
        self.add_command(("donation_messages", "donate_messages"), self.cmd_donation_messages)
        self.add_command("map_restart", self.cmd_maprestart, 1)
        self.add_command("muteall", self.cmd_muteall, 4)
        self.add_command("unmuteall", self.cmd_unmuteall, 4)
        self.add_command(("forum", "forums", "f"), self.cmd_forums)
        self.add_command(("donate", "donations", "d", "donating"), self.cmd_donate)
        self.add_command("killall", self.cmd_killall, 4)
        self.add_command(("respawn", "spawn"), self.cmd_respawn, 5)
        self.add_command(("respawn_aircontrol", "spawn_aircontrol"), self.respawn_aircontrol, 5)
        
        self.add_command("tomtec_versions", self.cmd_showversion)
        self.add_command(("wiki", "w"), self.cmd_wiki)
        self.add_command(("facebook", "fb"), self.cmd_facebook)
        self.add_command(("acommands", "acmds"), self.cmd_acommands)
        self.add_command("mapname", self.cmd_mapname) # display current map name
        self.add_command("server_reconfigure", self.cmd_reconfigure, 5)
        self.add_command("test", self.cmd_test)
        self.add_command(("listcv", "cvlist", "listcvs"), self.cmd_listcv)
    
        self.disabled_maps = ["proq3dm6"]
        
        self.set_cvar_once("qlx_freezePlayersDuringVote", "0") 
        self.set_cvar_once("qlx_purgeryDonationMessages", "0")
        self.set_cvar_once("qlx_visitForumMessages", "0")
        
        self.set_cvar_once("qlx_strictVql", "0")
        self.set_cvar_once("qlx_ratingLimiter", "0")
        
        self.plugin_version = "4.9"

        self.serverId = int((self.get_cvar("net_port", str))[-1:])
        self.serverLocation = self.get_cvar("sv_location")
        
        self.protectedPlayers = ["76561198213481765", "76561198061594466"] # purger, mf falling comets

        self.purgersBirthday = False

        if self.get_cvar("qlx_visitForumMessages", bool):
            message = "Visit ^2forum.thepurgery.com^7 to vote for/nominate a moderator."
            self.set_cvar("qlx_connectMessage", message)
            self.set_cvar("qlx_endOfGameMessage", message)
            
        if (datetime.datetime.now().month == 3) and (datetime.datetime.now().day == 18):
            # It's Purger's birthday.
            self.purgersBirthday = True
            self.set_cvar("purgersBirthday", "1", 68) # put it in the /serverinfo as read-only
            self.set_cvar("qlx_connectMessage", "^7It's Pur^4g^7er's Birthday!")
            self.set_cvar("qlx_countdownMessage", "^7It's Pur^4g^7er's Birthday!")
        else:
            self.set_cvar("purgersBirthday", "0", 68) # put it in the /serverinfo as read-only
            
        if self.get_cvar("qlx_strictVql", bool):
            minqlx.load_plugin("strictvql")
        
        if self.get_cvar("qlx_ratingLimiter", bool):
            minqlx.load_plugin("ratinglimiter")

        if "auckland" in self.serverLocation.lower(): # was put in to reduce lag and server command traffic in the auckland server.
            @minqlx.delay(20)
            def f():
                try:
                    minqlx.unload_plugin("fun")
                except:
                    pass
            f()
            
        ##########################################################################################
        ######################################## END INIT ########################################
        ##########################################################################################
   
        
    ################################### TESTING STUFF ###################################
    def cmd_test(self, player, msg, channel): # used for testing stuff
        @minqlx.thread
        def f(player, msg, channel):
            pass
        f(player, msg, channel)
        
    def set_player_configstring(self, player, index, key, value): # will let you set a configstring on a per-player basis.
        original_configstring = minqlx.parse_variables(minqlx.get_configstring(index))
        original_configstring[key] = value
        modified_configstring = (("\\") + ("\\".join("\\".join((k,str(v))) for k,v in sorted(original_configstring.items()))))
        minqlx.send_server_command(player.id, "cs {} {}".format(index, modified_configstring))

    def set_nextmaps(self, maps, maps_titles, factories, factories_titles): # will let you set the end-game-voting maps.
        """ EXAMPLE VALUES:
            maps = ("campgrounds", "gridworks", "6plus")
            maps_titles = ("The Campgrounds", "The Gridworks", "Modified Campgrounds")
            factories = ("ca", "duel", "ffa")
            factories_titles = ("VQL Clan Arena", "VQL Duel", "VQL Free For All")
        """
                       
        nextmaps = "\gt_2\{}\cfg_2\{}\title_2\{}\map_2\{}\gt_1\{}\cfg_1\{}\title_1\{}\map_1\{}\gt_0\{}\cfg_0\{}\title_0\{}\map_0\{}".format(
                       factories_titles[0], factories[0], maps_titles[0], maps[0],
                       factories_titles[1], factories[1], maps_titles[1], maps[1],
                       factories_titles[2], factories[2], maps_titles[2], maps[2])

        self.set_cvar("nextmaps", nextmaps)
        #player.tell(self.get_cvar("nextmaps"))
    ################################### TESTING STUFF ###################################


        
    @minqlx.thread
    def cmd_reconfigure(self, player, msg, channel): # clone and redeploy the ql-server-config github repo, downloading new files.
        channel.reply("^1Server: ^7Running ^2initialise.sh --no-restart^7.")
        p = subprocess.Popen("/home/qlserver/initialise.sh --no-restart", shell=True, stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            time.sleep(0.1)
            channel.reply("^1Process Output: ^7{}".format(line))
        retval = p.wait()
        channel.reply("^1Process Return Code: ^7{}".format(retval))
        return minqlx.RET_NONE

    def cmd_banyoyza(self, player, msg, channel):
        try:
            key = self.db["yoyzavote"]
        except:
            key = "Active"
            

        if key == "Active":
            self.callvote("qlx !ban 76561198047120527 50 years You are permanently banned from all ^4The Purgery^7 servers.", "^1ban Yoyza/Chinese characters from ^4The Purgery^1 permanently^3".upper(), 120)
            self.msg("{}^7 called a queued vote.".format(player.name))
            self.db["yoyzavote"] = "Run"
        else:
            channel.reply("This vote can only be called once. Ask Pur^4g^7er to reset this if necessary.")

    def cmd_respawn(self, player, msg, channel): # respawns the player. Will spawn a player no matter the team (spectators included ;))
        if len(msg) < 2:
            minqlx.player_spawn(player.id)
        else:
            try:
                minqlx.player_spawn(self.player(int(msg[1])).id)
            except:
                player.tell("Invalid client ID. Please enter a client ID of the player to (re)spawn.")
            
    def respawn_aircontrol(self, player, msg, channel): # uses a quick cvar switch and client respawn to give the player air control.
        @minqlx.next_frame
        def spawn(msg):
            if len(msg) < 2:
                minqlx.player_spawn(player.id)
            else:
                try:
                    minqlx.player_spawn(int(msg[1]))
                except:
                    player.tell("Invalid client ID. Please enter a client ID of the player to (re)spawn.")
        
        @minqlx.delay(0.2)
        def reset():
            self.set_cvar("pmove_aircontrol", "0")

        
        self.set_cvar("pmove_aircontrol", "1")
        spawn(msg)
        reset()

    def cmd_listcv(self, player, msg, channel):
        player.tell("^3Extra call-vote commands available on this server:^7")
        player.tell("^5   /cv freecam [on/off]            - Enables free-camming around the arena in a team-based game.")
        player.tell("^5   /cv infiniteammo [on/off]       - Enables infinite ammo on all weapons.")
        player.tell("^5   /cv alltalk [on/off]            - Enables voice communication between teams during the game.")
        player.tell("^5   /cv chatsounds [on/off]         - Enables the chat-activated sounds triggered by words.")
        player.tell("^5   /cv allready                    - Forces the game to start.")
        player.tell("^5   /cv abort                       - Abort the current game.")
        player.tell("^5   /cv silence <id>                - Silences a player for 10 minutes.")
        player.tell("^5   /cv floordamage [on/off]        - Permits damage to go through floors/walls/surfaces etc.")
        player.tell("^5   /cv spec <id>                   - Move the player specified to the spectators.")
        player.tell("^5   /cv tempban <id>                - Ban the specified player until the map changes.")
        player.tell("^5   /cv lock (team)                 - Lock both or specified team(s).")
        player.tell("^5   /cv unlock (team)               - Unlock both or specified team(s).")
        player.tell("^5   /cv roundtimelimit [90/120/180] - Changes the round time limit (specified in seconds).")
        player.tell("^5   /cv balancing [on/off]          - Enables/disables the elo/glicko team balancing system.")
        player.tell("^5   /cv lgdamage [6/7]              - Changes Lightning Gun damage/knockback.")
        player.tell("^5   /cv rgdamage [80/100]           - Changes Railgun damage.")
        player.tell("^5   /cv runes [on/off]              - Enables/disables runes.")
        player.tell("^5   /cv lgammo [150/200]            - Change starting lightning gun ammo.")
        player.tell("^5   /cv gibs [on/off]               - Enable server-forced gibs for all players.")
        player.tell("^5   /cv autobot [on/off]            - Enable/disable the bot balancing system.")
        player.tell("^5   /cv do                          - Forces the suggested switch.")
        return minqlx.RET_STOP_ALL

    def cmd_mapname(self, player, msg, channel):
        channel.reply("The current map's name is ^4{}^7.".format(self.game.map))
        
    def cmd_wiki(self, player, msg, channel):
        channel.reply("Visit ^2thepurgery.com^7 to see ^4The Purgery^7's wiki and documentation.")

    def cmd_facebook(self, player, msg, channel):
        channel.reply("Visit ^2fb.me/thepurgery^7 to see ^4The Purgery^7's Facebook page.")

    def cmd_muteall(self, player, msg, channel):
        # mute everybody on the server
        for p in self.players():
            p.mute()

    def cmd_unmuteall(self, player, msg, channel):
        # unmute everybody on the server
        for p in self.players():
            p.unmute()

    def cmd_killall(self, player, msg, channel):
        # kill everybody on the server, causes a round draw
        for p in self.players():
            p.health = 0

    def talk_beep(self, player=None):
        if not player:
            self.play_sound("sound/player/talk.ogg")
        else:
            self.play_sound("sound/player/talk.ogg", player)
            
    ######################################### DONATIONS CODE #########################################
    def cmd_donation_messages(self, player, msg, channel):
        flag = self.db.get_flag(player, "purgery:donation_messages", default=True)
        self.db.set_flag(player, "purgery:donation_messages", not flag)
        if flag:
            word = "disabled"
        else:
            word = "enabled"
        player.tell("Donation messages have been ^4{}^7.".format(word))
        return minqlx.RET_STOP_ALL
    
    def donation_message(self, message, player=None):
        if self.get_cvar("qlx_purgeryDonationMessages", bool):
            if not player:
                for player in self.players():
                    if self.db.get_flag(player, "purgery:donation_messages", default=True):
                        player.tell(message)
                        self.talk_beep(player)
            else:
                if self.db.get_flag(player, "purgery:donation_messages", default=True):
                    player.tell(message)
                    self.talk_beep(player)
    ######################################### DONATIONS CODE #########################################


    ######################################### ILLEGAL NAME CHECKS #########################################
    def handle_player_connect(self, player): # prohibit players to have any protected name in their name
        if str(player.steam_id)[0] == "9": return # don't check bots
        name = self.clean_text(player.name.lower())
        name = name.replace(ZERO_WIDTH_SPACE, "")
        if self.clean_text(OWNER_NAME.lower()) in name:
            if str(player.steam_id) != str(minqlx.owner()): # if the player steam id isn't minqlx.owner id, then it's not me
                return "{}^7 is the name of the server owner and is reserved. Please change your Steam name to something else.\n".format(OWNER_NAME)

    def handle_userinfo(self, player, changed): # kick players who change their in-game name to any protected name
        if str(player.steam_id)[0] == "9": return # don't check bots
        if "name" in changed:
            name = self.clean_text(changed["name"].lower())
            name = name.replace(ZERO_WIDTH_SPACE, "")
            if self.clean_text(OWNER_NAME.lower()) in name:
                if str(player.steam_id) != str(minqlx.owner()): # if the player steam id isn't minqlx.owner id, then it's not me
                    player.kick("{}^7 is the name of the server owner and is reserved. Please change it and re-connect.".format(OWNER_NAME))
    ######################################### ILLEGAL NAME CHECKS #########################################
                    
    @minqlx.next_frame
    def handle_player_loaded(self, player):
        @minqlx.delay(5)
        def f():
            # display donation message if any
            self.donation_message("Consider ^2!donating^7 to ^4The Purgery^7, it would really help a lot with the running costs.", player)

            # announce game mods
            self.talk_beep(player)
            player.tell("Current game moderators: Pur^4g^7er (owner), {}.".format(GAME_MODERATORS))
        f()

    def handle_chat(self, player, msg, channel):
        # notify users if they say certain things I don't like
        msg = msg.lower()
        words = msg.split()
        flag = "purgery:badwords:lag"

        for word in words:
            if word == "lag":
                if self.db.get_flag(player, flag, default=True):
                    player.tell("^2Notice: ^7Please don't complain about lag on this server, we're here to play, not to complain and moan.")
                    player.tell("^2The above message will not appear again.")
                    self.db.set_flag(player, flag, False)
                
        
    def handle_player_spawn(self, player):
        # Add in ExcessivePlus-like feeling, mimicing the spawn behaviour in EP.
        if self.game.type_short != "duel":
            if player.team != "spectator":
                if self.purgersBirthday:
                    p.powerups(quad=3)
                else:
                    p.powerups(battlesuit=3)
                @minqlx.delay(2.5)
                def f():
                    self.play_sound("sound/items/protect3.ogg", player)
                f()

        return minqlx.RET_NONE
        
    @minqlx.next_frame   
    def map_load(self, mapname, factory):
        # turn on infinite ammo for warm-up
        minqlx.set_cvar("g_infiniteAmmo", "1")
        
    def game_countdown(self):
        self.play_sound("sound/items/protect3.ogg")
        minqlx.set_cvar("g_infiniteAmmo", "0")
        if self.game.type_short != "duel":
            for p in self.players():
                p.noclip = True
                if self.purgersBirthday:
                    p.powerups(quad=10)
                else:
                    p.powerups(battlesuit=10)

        self.donation_message("Consider ^2!donating^7 to ^4The Purgery^7, it would really help a lot with the running costs.")
                 
    def game_end(self, data):
        return

    def game_start(self, data):
        # make sure everyone's noclip is off
        for p in self.players():
            p.noclip = False
        self.set_cvar("g_speed", "320")
        self.play_sound("sound/vo_evil/welcome")

    def cmd_clearperms(self, player, msg, channel):
        return
        
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

    def cmd_forums(self, player, msg, channel):
        channel.reply("Visit ^4The Purgery^7's forum at ^2forum.thepurgery.com^7.")

    def cmd_donate(self, player, msg, channel):
        channel.reply("Donations to ^4The Purgery^7 can be made via ^5PayPal^7 or ^3Bitcoin^7, check ^2tomtecsolutions.com.au/quakelive^7 for information.")
        channel.reply("Thank you!")
        
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4tomtec_logic.py^7 - version {}, created by Thomas Jones on 01/11/2015.".format(self.plugin_version))

    def handle_vote_called(self, caller, vote, args):            
        if vote.lower() == "map":
            # prevent certain maps from being loaded, if they're found to have issues
            if args.lower() is "disabled_test" or args.lower() in self.disabled_maps:
                caller.tell("Map ^4{}^7 is currently disabled, please contact an admin/mod for details.".format(args.lower()))
                return minqlx.RET_STOP_ALL

            # exception for maido map
            if args.lower() in "maido":
                voteFlags = self.get_cvar("g_voteFlags")
                self.set_cvar("g_voteFlags", "0")

                if self.game.type_short != "duel": return 
                
                @minqlx.next_frame
                def f(theFlags):
                    minqlx.client_command(caller.id, "callvote map maido maido")
                    self.set_cvar("g_voteFlags", theFlags)
                f(voteFlags)

                return minqlx.RET_STOP_ALL

            if args.lower() == "rustcampgrounds":
                minqlx.client_command(caller.id, "callvote map oxodm102_b1")
                caller.tell("Resolved ^4rustcampgrounds^7 to ^4oxodm102_b1^7.")
                return minqlx.RET_STOP_ALL

        if (vote.lower() == "kick") or (vote.lower() == "clientkick"):
            if len(args.split()) < 1:
                return minqlx.RET_STOP
            
            for steam_id in self.protectedPlayers:
                try:
                    if vote.lower() == "kick":
                        kickee = self.find_player(args.lower())[0]
                    elif vote.lower() == "clientkick":
                        kickee = self.player(int(args))
                        
                    if str(kickee.steam_id) == str(minqlx.owner()):
                        caller.tell("{}^7 is the server owner and cannot be kicked. {}^7 has been notified.".format(kickee.name, kickee.name))
                        kickee.tell("{}^7 just tried to call a {} vote against you.".format(caller.name, vote.lower()))
                        return minqlx.RET_STOP_ALL
                except:
                    return minqlx.RET_STOP
                    
                if str(steam_id) == str(kickee.steam_id):
                    caller.tell("{}^7 is in the list of protected players and cannot be kicked.".format(kickee.name))
                    return minqlx.RET_STOP_ALL

        if vote.lower() == "teamsize":
            if len(args.split()) < 1:
                return minqlx.RET_STOP

            if self.get_cvar("teamsize", str) in str(args):
                caller.tell("You sir, need to open your eyes. Only then will you see that the teamsize is already set to {}.".format(self.get_cvar("teamsize")))
                return minqlx.RET_STOP_ALL

        if vote.lower() == "autobot":
            # enables the '/cv autobot [on/off]' command
            if args.lower() == "off":
                self.callvote("set bot_autoManage 0", "automatic bot management: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set bot_autoManage 1", "automatic bot management: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv autobot [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "gibs":
            # enables the '/cv gibs [on/off]' command
            if args.lower() == "off":
                self.callvote("clearcvar qlx_workshopReferences", "^1gibs^3: off")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            elif args.lower() == "on":
                self.callvote("set qlx_workshopReferences 691078677", "^1gibs^3: on")
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell("^2/cv gibs [on/off]^7 is the usage for this callvote command.")
                return minqlx.RET_STOP_ALL

        if vote.lower() == "draw":
            if self.game.state != "in_progress":
                caller.tell("Voting to draw the round during warm-up isn't possible.")
                return minqlx.RET_STOP_ALL
            else:
                self.callvote("qlx !killall", "round draw")
                self.msg("{}^7 called a vote.".format(caller.name))
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
            minqlx.send_server_command(None, "cp \"^2VOTE PASSED^7\"\n")
        else:
            minqlx.send_server_command(None, "cp \"^1VOTE FAILED^7\"\n")
        self.set_cvar("g_speed", "320")
        
    def cmd_maprestart(self, player, msg, channel):
        # run a map restart
        minqlx.console_command("map_restart")
