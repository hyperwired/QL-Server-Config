# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class q3audio(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.map_load)
        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("round_countdown", self.handle_round_countdown)
        self.add_hook("round_start", self.handle_round_start)
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.0"
        
    def map_load(self, mapname, factory):
        self.game.workshop_items += [614429927]

    def handle_vote_called(self, player, vote, args):
        @minqlx.next_frame
        def vote_now():
            self.stop_sound()
            self.play_sound("q3_audio/vo/vote/vote_now.wav")
        vote_now()
        
    def handle_vote_ended(self, votes, vote, args, passed):
        @minqlx.next_frame
        def vote_passed_or_failed():
            self.stop_sound()
            if passed:
                self.play_sound("q3_audio/vo/vote/vote_passed.wav")
            else:
                self.play_sound("q3_audio/vo/vote/vote_failed.wav")
        vote_passed_or_failed()

    def handle_game_countdown(self):
        @minqlx.next_frame
        def prepare_your_team():
            self.stop_sound()
            self.play_sound("q3_audio/vo/gamestates/prepare_your_team.wav")
        prepare_your_team()


    def handle_round_countdown(self, *args, **kwargs):
        @minqlx.delay(4.6)
        def stop_round_begins_in():
            self.stop_sound()
        stop_round_begins_in()
        
        @minqlx.delay(6.6)
        def three():
            self.stop_sound()
            self.play_sound("q3_audio/vo/gamestates/countdown/3.wav")
        three()

        @minqlx.delay(7.6)
        def two():
            self.stop_sound()
            self.play_sound("q3_audio/vo/gamestates/countdown/2.wav")
        two()

        @minqlx.delay(8.6)
        def one():
            self.stop_sound()
            self.play_sound("q3_audio/vo/gamestates/countdown/1.wav")
        one()
        
    def handle_round_start(self, *args, **kwargs):
        @minqlx.next_frame
        def fight():
            self.stop_sound()
            self.play_sound("q3_audio/vo/gamestates/countdown/F.wav")
        fight()
        
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4q3audio.py^7 - version {}, created by Thomas Jones on 03/02/2016.".format(self.plugin_version))
