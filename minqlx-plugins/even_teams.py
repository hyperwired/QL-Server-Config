# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx

class even_teams(minqlx.Plugin):
    def __init__(self):
        self.add_hook("team_switch", self.handle_team_switch)
        #self.add_hook("round_countdown", self.handle_round_countdown)
        self.add_hook("round_start", self.handle_round_start)

        self.last_joined_id = None
        self.last_left_team = None
        self.last_left_id = None
        self.last_left_funcactive = 0

        self.lowest = None

    def handle_team_switch(self, player, old_team, new_team):
        if self.game.type_short == "ca":
            if old_team.lower() == "spectator":
                self.last_joined_id = player.id
                if len(teams["red"] + teams["blue"]) % 2 != 0:
                    player.tell("^1You will be put back to the spectators if the teams are uneven upon round start.")
                
            """if new_team.lower() == "spectator":
                self.last_left_team = old_team.lower()
                self.last_left_id = player.id
                self.last_left_funcactive = 1
                #player.tell("Because you've moved to spectator, the lowest-scoring player from the other team")
                #player.tell("will also be moved to spectator on next round start, unless someone else jumps in.")
                if old_team.lower() == "red":
                    self.lowest = sorted(teams["blue"], key=lambda p: p.stats.score)
                    self.lowest[0].tell("As you're the lowest-scoring player on the blue team, you'll be moved to spec to fix")
                    self.lowest[0].tell("team unevenness, unless another player jumps in to the red team before the round starts.")
                elif old_team.lower() == "blue":
                    self.lowest = sorted(teams["red"], key=lambda p: p.stats.score)
                    self.lowest[0].tell("As you're the lowest-scoring player on the red team, you'll be moved to spec to fix")
                    self.lowest[0].tell("team unevenness, unless another player jumps in to the blue team before the round starts.")"""


    """def handle_round_countdown(self, round_number):
       if self.game.type_short == "ca":
            teams = self.teams()
            if len(teams["red"] + teams["blue"]) % 2 != 0:
                try:
                    self.msg("{} will be moved to the spectators unless someone joins the {} team.".format(self.lowest[0].clean_name, self.last_left_team))
                except:
                    pass"""


    def handle_round_start(self, round_number):
        if self.game.type_short == "ca":
            teams = self.teams()
            if len(teams["red"] + teams["blue"]) % 2 != 0:
                #if self.last_left_funcactive == 1:
                #    self.last_left_funcactive = 0
                #    self.lowest[0].put("spectator")
                #    self.lowest[0].tell("You have been moved to the spectators to even up the teams, as no-one joined in time.")
                #    self.lowest[0].tell("Join again when someone else joins.")
                #if self.last_left_funcactive == 0:
                target_player = self.player(self.last_joined_id)
                target_player.put("spectator")
                target_player.tell("^1You have been put back to the spectators because the teams are uneven.")
                target_player.tell("Please join a team when another spectator does, so the teams are even.")

