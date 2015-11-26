# This has been created by TomTec Solutions

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
        
        
    def new_game(self):
        # brand the map
        minqlx.set_configstring(3, "^4The Purgery^7")
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
        #self.play_sound("sound/items/protect3.ogg") # waaaa, cthulhu's crying about how irritating this sound is...
        
    def game_start(self):
        # make sure everyone's noclip is off
        for p in self.players():
            p.noclip = False
        
    def game_end(self):
        #channel.tell("Hurrah!")
        #self.play_sound("sound/items/protect3.ogg")
        pass

    def cmd_showrules(self, player, msg, channel):
        channel.reply("^4========================================================================================")
        channel.reply("^4The Purgery^7 - ^3Server Rules:")
        channel.reply("^7    1. No racism, neo-nazism, harassment or abuse toward other players via text or voice chat.")
        channel.reply("^7    2. No disruptive behaviour of any kind, including 'spamming' and repetitive call-voting")
        channel.reply("^7    3. No cheating, hacking or abuse of server privileges.")
        channel.reply("^7    4. Lack of common sense is prohibited.")
        channel.reply("^7    5. If you've been muted, you're obviously doing something that one or more server ops don't approve of.")
        channel.reply("^7    6. These servers are being paid for by ^4Zeo^7byte, and the donators that assist with the funding.")
        channel.reply("^1  Failure to comply with these rules will result in a mute, a temporary ban, or a permanent ban.")
        channel.reply("^7  Have ^2fun^7, play, enjoy, don't do anything stupid.")
        channel.reply("^4========================================================================================")

    def cmd_help(self, player, msg, channel):
        player.tell("This server runs ^4tomtec_logic.py^7, a ^4minqlx^7 plugin that adds modification to ^4The Purgery^7 servers.")
        player.tell("^4tomtec_logic.py^7 is (c) 2015, Thomas Jones, TomTec Solutions.")
        return minqlx.RET_STOP_EVENT

    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "kick":
            # prevent certain players from being kicked via a call-vote
            playerName = args.lower()
            if playerName == "zeobyte":
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


