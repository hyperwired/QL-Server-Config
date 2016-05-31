# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Created by Thomas Jones on 31/05/16 - thomas@tomtecsolutions.com
# botmanager.py, a plugin for minqlx to manage bots.

BOT_NAME="^7Pur^4g^7obot" # name of bot in-game
BOT_TYPE=("Trainer", "4") # bot, skill level

ZERO_WIDTH_SPACE=u"\u200B" # part of the userinfo filtering to prevent illegal names

import minqlx
class botmanager(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.handle_map)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("team_switch", self.handle_team_switch)
        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_HIGHEST)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("console_print", self.handle_console_print)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("userinfo", self.handle_userinfo, priority=minqlx.PRI_HIGHEST)

        self.add_command("addbot", self.cmd_addbot, 1)
        self.add_command("rembot", self.cmd_rembot, 1)
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.1"

        self.botError = False
        self.atGameEnd = False
        
        self.set_cvar("bot_thinktime", "0")
        self.set_cvar("bot_challenge", "1")
        
        self.set_cvar_once("bot_autoManage", "0")


    ################################ METHODS ################################
    def talk_beep(self, player=None):
        if not player:
            self.play_sound("sound/player/talk.ogg")
        else:
            self.play_sound("sound/player/talk.ogg", player)

    def bots_present(self):
        for p in self.players():
            if str(p.clean_name) == str(self.clean_text(BOT_NAME)):
                return True
        return False

    def bot_team(self):
        for p in self.players():
            if str(p.clean_name) == str(self.clean_text(BOT_NAME)):
                return str(p.team)
        return None

    def bot_checks(self, flags):
        if "addbot" in flags.lower():
            if not self.get_cvar("bot_enable", bool):
                return (False, "^1Error:^7 Bots are not enabled on this server.")
            if self.botError:
                return (False, "^1Error:^7 Bots are not supported on this map.")
            if self.bots_present():
                return (False, "^1Error:^7 There is already a bot on this server.")
            return (True, None)
        elif "rembot" in flags.lower():
            if not self.bots_present():
                return (False, "^1Error:^7 There is no bot currently on this server.")
            return (True, None)
        return (False, None)

    def addbot(self):
        minqlx.console_command("addbot {} {} A 0 {}".format(BOT_TYPE[0], BOT_TYPE[1], BOT_NAME)) # team any, 0 millisecond join delay
        
    def rembot(self):
        minqlx.console_command("kick {}".format(self.clean_text(BOT_NAME))) # kicks BOT_NAME
    ################################ METHODS ################################

    ################################ HANDLERS ################################
    def handle_map(self, mapname, factory):
        if self.get_cvar("bot_enable", bool):
            self.botError = False
            self.addbot()
            self.rembot()
            self.atGameEnd = False
            @minqlx.delay(11)
            def f():
                if self.botError:
                    self.msg("^3Warning:^7 Bots are not supported on this map.")
                    self.talk_beep()
            f()

    def handle_game_end(self, data):
        self.atGameEnd = True
        
    def handle_player_connect(self, player): # prohibit players to have the bot's name in their name/as their name
        if str(player.steam_id)[0] == "9": return # don't check bots
        name = self.clean_text(player.name.lower())
        name = name.replace(ZERO_WIDTH_SPACE, "")
        if self.clean_text(BOT_NAME).lower() in name:
            return "^7Pur^4g^7obot is a restricted name. Please change your Steam name to something else.\n"

    def handle_userinfo(self, player, changed): # kick players who change their in-game name to the bot's name
        if str(player.steam_id)[0] == "9": return # don't check bots
        if "name" in changed:
            name = self.clean_text(changed["name"].lower())
            name = name.replace(ZERO_WIDTH_SPACE, "")
            if self.clean_text(BOT_NAME).lower() in name:
                player.kick("^7Pur^4g^7obot is a restricted name. Please pick another name and re-connect.")
                            
    def handle_console_print(self, text):
        if "botaisetupclient failed" in text.lower():
            self.botError = True
    
    @minqlx.next_frame
    def handle_player_disconnect(self, player, reason): # automatic bot-management
        if self.get_cvar("bot_autoManage", bool):
            if self.game.type_short == "ffa" or self.game.type_short == "duel" or self.game.type_short == "race": return
            if len(self.teams()['red']) != len(self.teams()['blue']):
                if self.bots_present():
                    if self.bot_checks("rembot")[0]:
                        self.msg("^2Bot Manager:^7 Automatically removing {}.".format(BOT_NAME))
                        self.rembot()
                else:
                    if self.bot_checks("addbot")[0]:
                        self.msg("^2Bot Manager:^7 Automatically adding {}.".format(BOT_NAME))
                        self.addbot()
                          
    @minqlx.next_frame
    def handle_team_switch(self, player, old_team, new_team): # automatic bot-management
        if self.get_cvar("bot_autoManage", bool):
            if self.game.type_short == "ffa" or self.game.type_short == "duel" or self.game.type_short == "race": return # exclude non-team gametypes
            if self.atGameEnd: return # do not swap bots during end-game
            if not self.bots_present():
                if len(self.teams()['red']) != len(self.teams()['blue']):
                    if len(self.teams()['red']) > len(self.teams()['blue']):
                        self.set_cvar("teamsize", str(len(self.teams()['red'])))
                    elif len(self.teams()['blue']) > len(self.teams()['red']):
                        self.set_cvar("teamsize", str(len(self.teams()['blue'])))
                    self.set_cvar("teamsize", str(self.get_cvar("teamsize", int) + 1)) # teamsize = teamsize + 1
                    if self.bot_checks("addbot")[0]:
                        self.msg("^2Bot Manager:^7 Automatically adding {}.".format(BOT_NAME))
                        self.addbot()
            else:
                if len(self.teams()['red']) != len(self.teams()['blue']):
                    if self.bot_checks("rembot")[0]:
                        self.msg("^2Bot Manager:^7 Automatically removing {}.".format(BOT_NAME))
                        bot_team = self.bot_team()
                        self.rembot()
                        if new_team != "spectator": player.team = bot_team

    def handle_vote_called(self, caller, vote, args):
        if vote.lower() == "addbot":
            # enables the '/cv addbot' command
            checker = self.bot_checks("addbot") # store the checker array here
            if self.get_cvar("bot_autoManage", bool):
                caller.tell("^1Error: ^7Automatic bot management is enabled. Manual bot commands are therefore disabled.")
                return minqlx.RET_STOP_ALL
            if checker[0]:
                self.callvote("qlx !addbot", "add ^7{}^3".format(BOT_NAME))
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell(checker[1])
                return minqlx.RET_STOP_ALL

        if vote.lower() == "rembot":
            # enables the '/cv rembot' command
            checker = self.bot_checks("rembot") # store the checker array here
            if self.get_cvar("bot_autoManage", bool):
                caller.tell("^1Error: ^7Automatic bot management is enabled. Manual bot commands are therefore disabled.")
                return minqlx.RET_STOP_ALL
            if checker[0]:
                self.callvote("qlx !rembot", "remove ^7{}^3".format(BOT_NAME))
                self.msg("{}^7 called a vote.".format(caller.name))
                return minqlx.RET_STOP_ALL
            else:
                caller.tell(checker[1])
                return minqlx.RET_STOP_ALL
    ################################ HANDLERS ################################

    ################################ COMMANDS ################################
    def cmd_addbot(self, player, msg, channel):
        checker = self.bot_checks("addbot") # store the checker array here
        if self.get_cvar("bot_autoManage", bool):
            channel.reply("^1Error: ^7Automatic bot management is enabled. Manual bot commands are therefore disabled.")
            return minqlx.RET_STOP_ALL
        if checker[0]:
            self.addbot()
            player.tell("Remember to ^2!rembot^7 when you're finished with your bot.")
        else:
            channel.reply(checker[1]) # report error to client 
            return minqlx.RET_STOP_ALL

    def cmd_rembot(self, player, msg, channel):
        checker = self.bot_checks("rembot") # store the checker array here
        if self.get_cvar("bot_autoManage", bool):
            channel.reply("^1Error: ^7Automatic bot management is enabled. Manual bot commands are therefore disabled.")
            return minqlx.RET_STOP_ALL
        if checker[0]:
            self.rembot()
        else:
            channel.reply(checker[1]) # report error to client 
            return minqlx.RET_STOP_ALL
    
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4botmanager.py^7 - version {}, created by Thomas Jones on 31/05/16.".format(self.plugin_version))
    ################################ COMMANDS ################################
