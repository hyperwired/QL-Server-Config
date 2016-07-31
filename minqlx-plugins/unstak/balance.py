# Created by github/hyperwired aka "stakz", 2016-07-31
# unstak, an alternative balancing method for minqlx
# This plugin is released to everyone, for any purpose. It comes with no warranty, no guarantee it works, it's released AS IS.
# You can modify everything, except for lines 1-4. They're there to indicate I whacked this together originally. Please make it better :D

import collections
import hashlib
from player_info import PlayerInfo
import random


def sort_by_elo_descending(players):
    return sorted(players, key=lambda p: (p.elo, p.name), reverse=True)


def balance_players_random(players):
    """
    Shuffle teams completely randomly.
    Non deterministic (random)

    :param players: a list of all the players that are to be balanced
    :return: (team_a, team_b) 2-tuple of lists of players
    """
    out = list(players)
    random.shuffle(out)
    total = len(out)
    return out[:total/2], out[total/2:]


def balance_players_ranked_odd_even(players):
    """
    Balance teams by first sorting players by skill and then picking players alternating to teams.
    Deterministic (Stable) for a given input.

    :param players: a list of all the players that are to be balanced
    :return: (team_a, team_b) 2-tuple of lists of players
    """
    presorted = sort_by_elo_descending(players)
    teams = ([], [])
    for i, player in enumerate(presorted):
        teams[i % 2].append(player)
    return teams


def accumulate_teams(team, players):
    """
    Accumulate input players placement into a target teams collection, returning the input deficit.
    :param team: A 2-tuple of lists ([], []) representing the team we are adding players to
    :param players: A 2-tuple of lists ([], []) representing the players we are adding to the target team
    :return: an int describing the balance of the added players (before they are added to the team)
        1  : The right team got an extra player
        0  : The players added were counted even.
        -1 : The left team got an extra player
    """
    left_count, right_count = len(players[0]), len(players[1])
    team[0].extend(players[0])
    team[1].extend(players[1])
    return right_count - left_count


def distribute_skill_band(players_class, bias_left=True):
    """
    Split a list into two lists by halving. If there is an odd number of elements, the 0th item will go to the
    list determined by bias_left parameter

    :param players_class: a list of PlayerInfo objects
    :param bias_left: True if the left team should get the extra player if there is one. Otherwise right team.
    :return: a 2-tuple of lists ([], []) filled with the placed players.
    """
    sorted_players = sort_by_elo_descending(players_class)
    teams_category = ([], [])

    # Deal with odd case. The bias side has a deficit, so they deserve the top player of this class
    even_start_idx = 0
    bias = 0
    if len(sorted_players) % 2 != 0:
        bias = -1 if bias_left else 1
        idx = 0 if bias_left else 1
        teams_category[idx].append(sorted_players[0])
        even_start_idx = 1

    # Place the remaining players
    bias += accumulate_teams(teams_category, balance_players_ranked_odd_even(sorted_players[even_start_idx:]))
    return teams_category


class SkillBands(object):
    """
    There are 5 broad skill bands:
    - "rookie": Generally are a liability to the team. New or under-performing players starting their skill journey.
    - "standard": An OK player. It is a wide category because typically they are inconsistent.
    - "decent": A mostly reliable/decent player that is often in the top half of the score board in a public match
    - "carry": A consistently top or near-top scoring player. Typically 98th percentile upwards.
    - "pro": Outlier-level excellent player capable of professional solo play. one of the top few in their region.

    Precedence of balancing is [rookie, pro, carries, decent, standard]
    The reasoning is that this is the order in which they usually impact the match outcome
    """
    ROOKIE_CATEGORY_NAME = "rookie"
    STANDARD_CATEGORY_NAME = "standard"
    DECENT_CATEGORY_NAME = "decent"
    CARRY_CATEGORY_NAME = "carry"
    PRO_CATEGORY_NAME = "pro"

    def __init__(self):
        self.ROOKIE_START_ELO = 0
        self.STANDARD_START_ELO = 1250
        self.DECENT_START_ELO = 1720
        self.CARRY_START_ELO = 1950
        self.PRO_START_ELO = 2220
        self.MAX_ELO = 999999

    def get_skill_ordering(self):
        return [self.ROOKIE_CATEGORY_NAME,
                self.STANDARD_CATEGORY_NAME,
                self.DECENT_CATEGORY_NAME,
                self.CARRY_CATEGORY_NAME,
                self.PRO_CATEGORY_NAME]

    def get_balance_ordering(self):
        return [self.ROOKIE_CATEGORY_NAME,
                self.PRO_CATEGORY_NAME,
                self.CARRY_CATEGORY_NAME,
                self.DECENT_CATEGORY_NAME,
                self.STANDARD_CATEGORY_NAME]

    def get_ordering(self, balance_ordering=True):
        if balance_ordering:
            return self.get_balance_ordering()
        else:
            return self.get_skill_ordering()

    def get_category_intervals(self, balance_ordering=True):
        d = {
            self.ROOKIE_CATEGORY_NAME: (self.ROOKIE_START_ELO, self.STANDARD_START_ELO),
            self.STANDARD_CATEGORY_NAME: (self.STANDARD_START_ELO, self.DECENT_START_ELO),
            self.DECENT_CATEGORY_NAME: (self.DECENT_START_ELO, self.CARRY_START_ELO),
            self.CARRY_CATEGORY_NAME: (self.CARRY_START_ELO, self.PRO_START_ELO),
            self.PRO_CATEGORY_NAME: (self.PRO_START_ELO, self.MAX_ELO),
        }
        out = collections.OrderedDict()
        ordering = self.get_ordering(balance_ordering=balance_ordering)
        for band_name in ordering:
            out[band_name] = d[band_name]
        return out


def split_players_by_skill_band(players, balance_ordering=True):
    """
    :param players: a list of all the players (PlayerInfo) that need to be balanced
    :return: players split by skill band [(category name: PlayerInfo), ...]
    """
    default_skill_bands = SkillBands()
    skill_intervals = default_skill_bands.get_category_intervals(balance_ordering=balance_ordering)

    d = collections.OrderedDict()
    for category_name, (interval_start, interval_end) in skill_intervals.items():
        d[category_name] = [p for p in players if (p.elo >= interval_start and p.elo < interval_end)]
    return d


def balance_players_by_skill_band(players):
    """
    Balance teams by classifying players into skill bands, and then try to match band distribution between both
    teams. In scenarios where there are odd players per skill band, we track the deficit and make up for it in
    the next bands.
    Deterministic (Stable) for a given input.

    See SkillBands for a definition of skill bands

    :param players: a list of all the players that are to be balanced
    :return: (team_a, team_b) 2-tuple of lists of players
    """
    bands = split_players_by_skill_band(players, balance_ordering=True)
    categories = list(bands.values())

    # Generate a value based on player elos to pick which side gets tiebreaker bias for first category
    # We do it this way so e.g. left team is not always favoured, but keeping it deterministic so that the
    # same elo profiles input will generate the same matchmaking without introducing RNG randomness (for testability).
    hasher = hashlib.md5()
    sorted_players = sort_by_elo_descending(players)
    for player in sorted_players:
        assert isinstance(player, PlayerInfo)
        hasher.update(("%d-%d" % (player.elo, player.elo_variance)).encode("utf-8"))
    fallback_bias = bytearray(hasher.digest())[0] & 0x1

    team_a = []
    team_b = []

    teams = (team_a, team_b)

    bias_levels = [0]*len(categories)
    last_bias_category = None
    for i, category in enumerate(categories):
        # each category gets alternating default bias
        bias_left = ((fallback_bias + i) % 2) == 0
        if last_bias_category is not None and bias_levels[last_bias_category] != 0:
            bias_left = True if bias_levels[last_bias_category] == 1 else False
        resolved_band = distribute_skill_band(category, bias_left=bias_left)
        category_bias = accumulate_teams(teams, resolved_band)
        bias_levels[i] = category_bias
        if category_bias != 0:
            last_bias_category = i

    #TODO: Are we done? Rebalance between players at same skillrating level per category?
    # i.e. is it possible to match accumulated ELOs closer than they currently are without changing category composition?
    return teams

