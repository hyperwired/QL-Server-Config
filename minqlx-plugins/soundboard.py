# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

NEW_GAME_SOUND = [False, False]

GAME_COUNTDOWN_SOUND = [False, False]
GAME_START_SOUND = [False, False]
GAME_END_SOUND = ["can_we_still_be_friends", True]

ROUND_COUNTDOWN_SOUND = [False, False]
ROUND_START_SOUND = [False, False]
ROUND_END_SOUND = [False, False]

PLAYER_CONNECT_SOUND = [False, False]
PLAYER_LOADED_SOUND = [False, False]
PLAYER_DISCONNECT_SOUND = [False, False]

PLAYER_VOTED_NO_SOUND = [False, False]
PLAYER_VOTED_YES_SOUND = [False, False]

VOTE_CALLED_SOUND = [False, False]
VOTE_PASSED_SOUND = [False, False]
VOTE_FAILED_SOUND = [False, False]


class soundboard(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.load_workshop_items)
        self.add_hook("new_game", self.play_new_game_sound)
        self.add_hook("game_countdown", self.play_game_countdown_sound)
        self.add_hook("game_start", self.play_game_start_sound)
        self.add_hook("game_end", self.play_game_end_sound)
        self.add_hook("round_countdown", self.play_round_countdown_sound)
        self.add_hook("round_start", self.play_round_start_sound)
        self.add_hook("round_end", self.play_round_end_sound)
        self.add_hook("player_connect", self.play_player_connect_sound)
        self.add_hook("player_loaded", self.play_player_loaded_sound)
        self.add_hook("player_disconnect", self.play_player_disconnect_sound)
        self.add_hook("vote", self.play_player_voted_sound)
        self.add_hook("vote_started", self.play_vote_called_sound)
        self.add_hook("vote_ended", self.play_vote_ended_sound)

        self.set_cvar_once("qlx_soundboardWorkshopId", "645733939")
        self.set_cvar_once("qlx_soundboardDirectory", "soundboard/")

        self.plugin_version = "0.1"
        self.add_command("tomtec_versions", self.cmd_showversion)

    def play_new_game_sound(self, *args, **kwargs):
        play(NEW_GAME_SOUND[0], NEW_GAME_SOUND[1])
        
    def play_game_countdown_sound(self, *args, **kwargs):
        play(GAME_COUNTDOWN_SOUND[0], GAME_COUNTDOWN_SOUND[1])

    def play_game_start_sound(self, *args, **kwargs):
        play(GAME_START_SOUND[0], GAME_START_SOUND[1])
        
    def play_game_end_sound(self, *args, **kwargs):
        play(GAME_END_SOUND[0], GAME_END_SOUND[1])
        
    def play_round_countdown_sound(self, *args, **kwargs):
        play(ROUND_COUNTDOWN_SOUND[0], ROUND_COUNTDOWN_SOUND[1])
        
    def play_round_start_sound(self, *args, **kwargs):
        play(ROUND_START_SOUND[0], ROUND_START_SOUND[1])
        
    def play_round_end_sound(self, *args, **kwargs):
        play(ROUND_END_SOUND[0], ROUND_END_SOUND[1])
        
    def play_player_connect_sound(self, *args, **kwargs):
        play(PLAYER_CONNECT_SOUND[0], PLAYER_CONNECT_SOUND[1])
        
    def play_player_loaded_sound(self, *args, **kwargs):
        play(PLAYER_LOADED_SOUND[0], PLAYER_LOADED_SOUND[1])
        
    def play_player_disconnect_sound(self, *args, **kwargs):
        play(PLAYER_DISCONNECT_SOUND[0], PLAYER_DISCONNECT_SOUND[1])
        
    def play_player_voted_sound(self, player, yes):
        if yes:
            play(PLAYER_VOTED_YES_SOUND[0], PLAYER_VOTED_YES_SOUND[1], player)
        else:
            play(PLAYER_VOTED_NO_SOUND[0], PLAYER_VOTED_NO_SOUND[1], player)
        
    def play_vote_called_sound(self, *args, **kwargs):
        play(VOTE_CALLED_SOUND[0], VOTE_CALLED_SOUND[1])
        
    def play_vote_ended_sound(self, votes, vote, args, passed):
        if passed:
            play(VOTE_PASSED_SOUND[0], VOTE_PASSED_SOUND[1])
        else:
            play(VOTE_FAILED_SOUND[0], VOTE_FAILED_SOUND[1])

    def load_workshop_items(self, *args, **kwargs):
        if not self.get_cvar("qlx_soundboardWorksopId", bool): return        
        self.game.workshop_items += (self.get_cvar("qlx_soundboardWorkshopId", list))

    def play(self, audiofile, isMusic=False, player=None):
        if not audiofile: return
        if isMusic:
            self.play_music(self.get_cvar("qlx_soundboardDirectory") + audiofile, player)
        else:
            self.play_sound(self.get_cvar("qlx_soundboardDirectory") + audiofile, player)
                                     
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4soundboard.py^7 - version {}, created by Thomas Jones on 14/03/16.".format(self.plugin_version))

    
