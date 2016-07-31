# minqlx - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>

# This file is part of minqlx.

# minqlx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# minqlx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with minqlx. If not, see <http://www.gnu.org/licenses/>.

import minqlx
import requests
import itertools
import threading
import random
import time
import collections
import hashlib

from minqlx.database import Redis

RATING_KEY = "minqlx:players:{0}:ratings:{1}" # 0 == steam_id, 1 == short gametype.
MAX_ATTEMPTS = 3
CACHE_EXPIRE = 60*30 # 30 minutes TTL.
DEFAULT_RATING = 1200
SUPPORTED_GAMETYPES = ("ca", "ctf", "dom", "ft", "tdm")
# Externally supported game types. Used by !getrating for game types the API works with.
EXT_SUPPORTED_GAMETYPES = ("ca", "ctf", "dom", "ft", "tdm", "duel", "ffa")


#----------------------------------------------------------------------------------------------------------------------------------------
# unstak, an alternative balancing method for minqlx created by github/hyperwired aka "stakz", 2016-07-31
# This plugin is released to everyone, for any purpose. It comes with no warranty, no guarantee it works, it's released AS IS.
# You can modify everything, except for lines 1-4. They're there to indicate I whacked this together originally. Please make it better :D

def format_obj_desc_str(obj):
    oclass = obj.__class__
    a = str(obj.__module__)
    b = str(obj.__class__.__name__)
    return "%s.%s %s" % (a, b, obj.desc())


def format_obj_desc_repr(obj):
    return "<%s object @ 0x%x>" % (format_obj_desc_str(obj), id(obj))


class PerformanceSnapshot(object):
    def __init__(self, elo, elo_variance):
        self._elo = elo
        self._elo_variance = elo_variance

    @property
    def elo(self):
        return self._elo

    @property
    def elo_variance(self):
        return self._elo_variance

    def desc(self):
        return "elo=%s (~%s)" % (self._elo, self._elo_variance)

    def __str__(self):
        return format_obj_desc_str(self)

    def __repr__(self):
        return format_obj_desc_repr(self)


class PerformanceHistory(object):
    def __init__(self):
        self._snapshots = []

    def has_data(self):
        return len(self._snapshots)

    def latest_snapshot(self):
        if self.has_data():
            return self._snapshots[-1]
        return None

    def desc(self):
        latest = self.latest_snapshot()
        if latest:
            return "%s, history=%s" % (latest.desc(), len(self._snapshots))
        return "<empty>"

    def __str__(self):
        return format_obj_desc_str(self)

    def __repr__(self):
        return format_obj_desc_repr(self)


class PlayerInfo(object):
    def __init__(self, name=None, perf_history=None, steam_id=None, ext_obj=None):
        self._name = name
        self._perf_history = perf_history
        self._steam_id = steam_id
        self._ext_obj = ext_obj

    @property
    def steam_id(self):
        return self._steam_id

    @property
    def ext_obj(self):
        return self._ext_obj

    @property
    def perf_history(self):
        return self._perf_history

    @property
    def latest_perf(self):
        return self._perf_history.latest_snapshot()

    @property
    def elo(self):
        return self.latest_perf.elo

    @property
    def elo_variance(self):
        return self.latest_perf.elo_variance

    @property
    def name(self):
        return self._name

    def desc(self):
        return "'%s': %s" % (self._name, self._perf_history.desc())

    def __str__(self):
        return format_obj_desc_str(self)

    def __repr__(self):
        return format_obj_desc_repr(self)


def player_info_list_from_steam_id_name_ext_obj_elo_dict(d):
    out = []
    for steam_id, (name, elo, ext_obj) in d.items():
        perf_snap = PerformanceSnapshot(elo, 0)
        perf_history = PerformanceHistory()
        perf_history._snapshots.append(perf_snap)
        player_info = PlayerInfo(name, perf_history, steam_id=steam_id, ext_obj=ext_obj)
        out.append(player_info)
    return out


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

# end unstak
#----------------------------------------------------------------------------------------------------------------------------------------



class balance(minqlx.Plugin):
    database = Redis
    
    def __init__(self):
        self.add_hook("round_countdown", self.handle_round_countdown)
        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_command(("setrating", "setelo", "setglicko"), self.cmd_setrating, 3, usage="<id> <rating>")
        self.add_command(("getrating", "getelo", "elo", "glicko"), self.cmd_getrating, usage="<id> [gametype]")
        self.add_command(("remrating", "remelo", "remglicko"), self.cmd_remrating, 3, usage="<id>")
        self.add_command("balance", self.cmd_balance, 1)
        self.add_command("unstak", self.cmd_unstak, 1)
        self.add_command(("teams", "teens"), self.cmd_teams)
        self.add_command("do", self.cmd_do, 1)
        self.add_command(("agree", "a"), self.cmd_agree)
        self.add_command(("ratings", "elos", "selo", "sglickos"), self.cmd_ratings)

        self.ratings_lock = threading.RLock()
        # Keys: steam_id - Items: {"ffa": {"elo": 123, "games": 321, "local": False}, ...}
        self.ratings = {}
        # Keys: request_id - Items: (players, callback, channel)
        self.requests = {}
        self.request_counter = itertools.count()
        self.suggested_pair = None
        self.suggested_agree = [False, False]
        self.in_countdown = False

        self.set_cvar_once("qlx_balanceUseLocal", "1")
        self.set_cvar_once("qlx_balanceUrl", "qlstats.net:8080")
        self.set_cvar_once("qlx_balanceAuto", "1")
        self.set_cvar_once("qlx_balanceMinimumSuggestionDiff", "25")
        self.set_cvar_once("qlx_balanceApi", "elo")

        self.use_local = self.get_cvar("qlx_balanceUseLocal", bool)
        self.api_url = "http://{}/{}/".format(self.get_cvar("qlx_balanceUrl"), self.get_cvar("qlx_balanceApi"))

    def handle_round_countdown(self, *args, **kwargs):
        if all(self.suggested_agree):
            # If we don't delay the switch a bit, the round countdown sound and
            # text disappears for some weird reason.
            @minqlx.next_frame
            def f():
                self.execute_suggestion()
            f()
        
        self.in_countdown = True

    def handle_round_start(self, *args, **kwargs):
        self.in_countdown = False

    def handle_vote_ended(self, votes, vote, args, passed):
        if passed == True and vote == "shuffle" and self.get_cvar("qlx_balanceAuto", bool):
            gt = self.game.type_short
            if gt not in SUPPORTED_GAMETYPES:
                return

            @minqlx.delay(3.5)
            def f():
                players = self.teams()
                if len(players["red"] + players["blue"]) % 2 != 0:
                    self.msg("Teams were ^4NOT^7 balanced due to the total number of players being an odd number.")
                    return
                
                players = dict([(p.steam_id, gt) for p in players["red"] + players["blue"]])
                self.add_request(players, self.callback_balance, minqlx.CHAT_CHANNEL)
            f()

    @minqlx.thread
    def fetch_ratings(self, players, request_id):
        if not players:
            return

        # We don't want to modify the actual dict, so we use a copy.
        players = players.copy()

        # Get local ratings if present in DB.
        if self.use_local:
            for steam_id in players.copy():
                gt = players[steam_id]
                key = RATING_KEY.format(steam_id, gt)
                if key in self.db:
                    with self.ratings_lock:
                        if steam_id in self.ratings:
                            self.ratings[steam_id][gt] = {"games": -1, "elo": int(self.db[key]), "local": True, "time": -1}
                        else:
                            self.ratings[steam_id] = {gt: {"games": -1, "elo": int(self.db[key]), "local": True, "time": -1}}
                    del players[steam_id]

        attempts = 0
        last_status = 0
        while attempts < MAX_ATTEMPTS:
            attempts += 1
            url = self.api_url + "+".join([str(sid) for sid in players])
            res = requests.get(url)
            last_status = res.status_code
            if res.status_code != requests.codes.ok:
                continue
            
            js = res.json()
            if "players" not in js:
                last_status = -1
                continue

            # Fill our ratings dict with the ratings we just got.
            for p in js["players"]:
                sid = int(p["steamid"])
                del p["steamid"]
                t = time.time()

                with self.ratings_lock:
                    if sid not in self.ratings:
                        self.ratings[sid] = {}
                    
                    for gt in p:
                        p[gt]["time"] = t
                        p[gt]["local"] = False
                        self.ratings[sid][gt] = p[gt]
                        
                        if sid in players and gt == players[sid]:
                            # The API gave us the game type we wanted, so we remove it.
                            del players[sid]

                    # Fill the rest of the game types the API didn't return but supports.
                    for gt in SUPPORTED_GAMETYPES:
                        if gt not in self.ratings[sid]:
                            self.ratings[sid][gt] = {"games": -1, "elo": DEFAULT_RATING, "local": False, "time": time.time()}

            # If the API didn't return all the players, we set them to the default rating.
            for sid in players:
                with self.ratings_lock:
                    if sid not in self.ratings:
                        self.ratings[sid] = {}
                    self.ratings[sid][players[sid]] = {"games": -1, "elo": DEFAULT_RATING, "local": False, "time": time.time()}

            break

        if attempts == MAX_ATTEMPTS:
            self.handle_ratings_fetched(request_id, last_status)
            return

        self.handle_ratings_fetched(request_id, requests.codes.ok)

    @minqlx.next_frame
    def handle_ratings_fetched(self, request_id, status_code):
        players, callback, channel, args = self.requests[request_id]
        del self.requests[request_id]
        if status_code != requests.codes.ok:
            # TODO: Put a couple of known errors here for more detailed feedback.
            channel.reply("ERROR {}: Failed to fetch glicko ratings.".format(status_code))
        else:
            callback(players, channel, *args)

    def add_request(self, players, callback, channel, *args):
        req = next(self.request_counter)
        self.requests[req] = players.copy(), callback, channel, args

        # Only start a new thread if we need to make an API request.
        if self.remove_cached(players):
            self.fetch_ratings(players, req)
        else:
            # All players were cached, so we tell it to go ahead and call the callbacks.
            self.handle_ratings_fetched(req, requests.codes.ok)

    def remove_cached(self, players):
        with self.ratings_lock:
            for sid in players.copy():
                gt = players[sid]
                if sid in self.ratings and gt in self.ratings[sid]:
                    t = self.ratings[sid][gt]["time"]
                    if t == -1 or time.time() < t + CACHE_EXPIRE:
                        del players[sid]

        return players

    def cmd_getrating(self, player, msg, channel):
        if len(msg) == 1:
            sid = player.steam_id
        else:
            try:
                sid = int(msg[1])
                target_player = None
                if 0 <= sid < 64:
                    target_player = self.player(sid)
                    sid = target_player.steam_id
            except ValueError:
                player.tell("Invalid ID. Use either a client ID or a SteamID64.")
                return minqlx.RET_STOP_ALL
            except minqlx.NonexistentPlayerError:
                player.tell("Invalid client ID. Use either a client ID or a SteamID64.")
                return minqlx.RET_STOP_ALL

        if len(msg) > 2:
            if msg[2].lower() in EXT_SUPPORTED_GAMETYPES:
                gt = msg[2].lower()
            else:
                player.tell("Invalid gametype. Supported gametypes: {}"
                    .format(", ".join(EXT_SUPPORTED_GAMETYPES)))
                return minqlx.RET_STOP_ALL
        else:
            gt = self.game.type_short
            if gt not in EXT_SUPPORTED_GAMETYPES:
                player.tell("This game mode is not supported by the balance plugin.")
                return minqlx.RET_STOP_ALL

        self.add_request({sid: gt}, self.callback_getrating, channel, gt)

    def callback_getrating(self, players, channel, gametype):
        sid = next(iter(players))
        player = self.player(sid)
        if player:
            name = player.name
        else:
            name = sid
        
        channel.reply("{} has a glicko rating of ^4{}^7 in {}.".format(name, self.ratings[sid][gametype]["elo"], gametype.upper()))

    def cmd_setrating(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE
        
        try:
            sid = int(msg[1])
            target_player = None
            if 0 <= sid < 64:
                target_player = self.player(sid)
                sid = target_player.steam_id
        except ValueError:
            player.tell("Invalid ID. Use either a client ID or a SteamID64.")
            return minqlx.RET_STOP_ALL
        except minqlx.NonexistentPlayerError:
            player.tell("Invalid client ID. Use either a client ID or a SteamID64.")
            return minqlx.RET_STOP_ALL
        
        try:
            rating = int(msg[2])
        except ValueError:
            player.tell("Invalid rating.")
            return minqlx.RET_STOP_ALL

        if target_player:
            name = target_player.name
        else:
            name = sid
        
        gt = self.game.type_short
        self.db[RATING_KEY.format(sid, gt)] = rating

        # If we have the player cached, set the rating.
        with self.ratings_lock:
            if sid in self.ratings and gt in self.ratings[sid]:
                self.ratings[sid][gt]["elo"] = rating
                self.ratings[sid][gt]["local"] = True
                self.ratings[sid][gt]["time"] = -1

        channel.reply("{}'s {} glicko rating has been set to ^4{}^7.".format(name, gt.upper(), rating))

    def cmd_remrating(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        try:
            sid = int(msg[1])
            target_player = None
            if 0 <= sid < 64:
                target_player = self.player(sid)
                sid = target_player.steam_id
        except ValueError:
            player.tell("Invalid ID. Use either a client ID or a SteamID64.")
            return minqlx.RET_STOP_ALL
        except minqlx.NonexistentPlayerError:
            player.tell("Invalid client ID. Use either a client ID or a SteamID64.")
            return minqlx.RET_STOP_ALL
        
        if target_player:
            name = target_player.name
        else:
            name = sid
        
        gt = self.game.type_short
        del self.db[RATING_KEY.format(sid, gt)]

        # If we have the player cached, remove the game type.
        with self.ratings_lock:
            if sid in self.ratings and gt in self.ratings[sid]:
                del self.ratings[sid][gt]

        channel.reply("{}'s locally set {} rating has been deleted.".format(name, gt.upper()))

    def cmd_balance(self, player, msg, channel):
        gt = self.game.type_short
        if gt not in SUPPORTED_GAMETYPES:
            player.tell("This game mode is not supported by the balance plugin.")
            return minqlx.RET_STOP_ALL

        teams = self.teams()
        if len(teams["red"] + teams["blue"]) % 2 != 0:
            player.tell("The total number of players should be an even number.")
            return minqlx.RET_STOP_ALL
        
        players = dict([(p.steam_id, gt) for p in teams["red"] + teams["blue"]])
        self.add_request(players, self.callback_balance, minqlx.CHAT_CHANNEL)

    def callback_balance(self, players, channel):
        # We check if people joined while we were requesting ratings and get them if someone did.
        teams = self.teams()
        current = teams["red"] + teams["blue"]
        gt = self.game.type_short

        for p in current:
            if p.steam_id not in players:
                d = dict([(p.steam_id, gt) for p in current])
                self.add_request(d, self.callback_balance, channel)
                return

        # Start out by evening out the number of players on each team.
        diff = len(teams["red"]) - len(teams["blue"])
        if abs(diff) > 1:
            if diff > 0:
                for i in range(diff - 1):
                    p = teams["red"].pop()
                    p.put("blue")
                    teams["blue"].append(p)
            elif diff < 0:
                for i in range(abs(diff) - 1):
                    p = teams["blue"].pop()
                    p.put("red")
                    teams["red"].append(p)

        # Start shuffling by looping through our suggestion function until
        # there are no more switches that can be done to improve teams.
        switch = self.suggest_switch(teams, gt)
        if switch:
            while switch:
                p1 = switch[0][0]
                p2 = switch[0][1]
                self.switch(p1, p2)
                teams["blue"].append(p1)
                teams["red"].append(p2)
                teams["blue"].remove(p2)
                teams["red"].remove(p1)
                switch = self.suggest_switch(teams, gt)
            avg_red = self.team_average(teams["red"], gt)
            avg_blue = self.team_average(teams["blue"], gt)
            diff_rounded = abs(round(avg_red) - round(avg_blue)) # Round individual averages.
            if round(avg_red) > round(avg_blue):
                self.msg("^1{} ^7vs ^4{}^7 - DIFFERENCE: ^1{}"
                    .format(round(avg_red), round(avg_blue), diff_rounded))
            elif round(avg_red) < round(avg_blue):
                self.msg("^1{} ^7vs ^4{}^7 - DIFFERENCE: ^4{}"
                    .format(round(avg_red), round(avg_blue), diff_rounded))
            else:
                self.msg("^1{} ^7vs ^4{}^7 - Holy shit!"
                    .format(round(avg_red), round(avg_blue)))
        else:
            channel.reply("Teams are good! Nothing to balance.")
        return True

    def cmd_unstak(self, player, msg, channel):
        gt = self.game.type_short
        if gt not in SUPPORTED_GAMETYPES:
            player.tell("This game mode is not supported by the balance plugin.")
            return minqlx.RET_STOP_ALL

        teams = self.teams()
        if len(teams["red"] + teams["blue"]) <= 2:
            player.tell("Nothing to balance.")
            return minqlx.RET_STOP_ALL

        players = dict([(p.steam_id, gt) for p in teams["red"] + teams["blue"]])
        self.add_request(players, self.callback_unstak, minqlx.CHAT_CHANNEL)

    def callback_unstak(self, players, channel):
        # We check if people joined while we were requesting ratings and get them if someone did.
        teams = self.teams()
        current = teams["red"] + teams["blue"]
        gt = self.game.type_short

        for p in current:
            if p.steam_id not in players:
                d = dict([(p.steam_id, gt) for p in current])
                self.add_request(d, self.callback_unstak, channel)
                return

        # Generate an unstak PlayerInfo list
        players_dict = {}
        for p in current:
            player_steam_id = p.steam_id
            player_name = p.clean_name
            player_elo = self.ratings[p.steam_id][gt]["elo"]
            players_dict[p.steam_id] = (player_name, player_elo, p)
        players_info = player_info_list_from_steam_id_name_ext_obj_elo_dict(players_dict)

        # do unstak balancing on player data (doesnt actually do any balancing operations)
        new_blue_team, new_red_team = balance_players_by_skill_band(players_info)

        def move_players_to_new_team(team, team_index):
            """
            Move the given players to this team.
            :param team: PlayerInfo list for one of the teams
            :param team_index: The corresponding index of team. 0 = blue, 1 = red
            :return: True if any players were moved
            """
            team_names = ["blue", "red"]
            players_moved = False
            this_team_name = team_names[team_index]
            other_team_name = team_names[1 - team_index]
            for player_info in team:
                assert isinstance(player_info, PlayerInfo)
                p = player_info.ext_obj
                assert p
                players_moved = (p.team != this_team_name) 
                p.team = this_team_name
                    
            return players_moved

        moved_players = False
        moved_players = move_players_to_new_team(new_blue_team, 0) or moved_players
        moved_players = move_players_to_new_team(new_red_team, 1) or moved_players

        if not moved_players:
            channel.reply("No one was moved.")
            return True

        self.report_team_stats(teams, gt, new_blue_team, new_red_team)
        return True

    # TODO: other reporting sites (e.g. balance/teams command) could be updated to use this (needs to use PlayerInfo)
    def report_team_stats(self, teams, gt, new_blue_team, new_red_team):
        # print some stats
        avg_red = self.team_average(teams["red"], gt)
        avg_blue = self.team_average(teams["blue"], gt)
        diff_rounded = abs(round(avg_red) - round(avg_blue))  # Round individual averages.

        def team_color(team_index):
            if team_index == 0:
                # red
                return "^1"
            elif team_index == 1:
                # blue
                return "^4"
            return ""

        def stronger_team_index(red_amount, blue_amount):
            if red_amount > blue_amount:
                return 0
            if red_amount < blue_amount:
                return 1
            return None

        round_avg_red = round(avg_red)
        round_avg_blue = round(avg_blue)
        favoured_team_colour_prefix = team_color(stronger_team_index(round_avg_red, round_avg_blue))
        avg_msg = "^1{} ^7vs ^4{}^7 - DIFFERENCE: ^{}{}".format(round_avg_red,
                                                                round_avg_blue,
                                                                favoured_team_colour_prefix,
                                                                diff_rounded)
        self.msg(avg_msg)
        # print some skill band stats
        bands_msg = []
        blue_bands = split_players_by_skill_band(new_blue_team)
        red_bands = split_players_by_skill_band(new_red_team)
        for category_name in blue_bands.keys():
            blue_players = blue_bands[category_name]
            red_players = red_bands[category_name]
            difference = abs(len(blue_players) - len(red_players))
            if difference:
                adv_team_idx = stronger_team_index(len(red_players), len(blue_players))
                bands_msg.append("{}:{}+{}".format(category_name,
                                                   team_color(adv_team_idx),
                                                   difference))
        bands_diff_content = "Balanced"
        if bands_msg:
            bands_diff_content = "^7, ".join(bands_msg)

        bands_msg = "Net skill band diff: " + bands_diff_content
        self.msg(bands_msg)

    def cmd_teams(self, player, msg, channel):
        gt = self.game.type_short
        if gt not in SUPPORTED_GAMETYPES:
            player.tell("This game mode is not supported by the balance plugin.")
            return minqlx.RET_STOP_ALL
        
        teams = self.teams()
        if len(teams["red"]) != len(teams["blue"]):
            player.tell("Both teams should have the same number of players.")
            return minqlx.RET_STOP_ALL
        
        teams = dict([(p.steam_id, gt) for p in teams["red"] + teams["blue"]])
        self.add_request(teams, self.callback_teams, channel)

    def callback_teams(self, players, channel):
        # We check if people joined while we were requesting ratings and get them if someone did.
        teams = self.teams()
        current = teams["red"] + teams["blue"]
        gt = self.game.type_short

        for p in current:
            if p.steam_id not in players:
                d = dict([(p.steam_id, gt) for p in current])
                self.add_request(d, self.callback_teams, channel)
                return

        avg_red = self.team_average(teams["red"], gt)
        avg_blue = self.team_average(teams["blue"], gt)
        switch = self.suggest_switch(teams, gt)
        diff_rounded = abs(round(avg_red) - round(avg_blue)) # Round individual averages.
        if round(avg_red) > round(avg_blue):
            channel.reply("^1{} ^7vs ^4{}^7 - DIFFERENCE: ^1{}"
                .format(round(avg_red), round(avg_blue), diff_rounded))
        elif round(avg_red) < round(avg_blue):
            channel.reply("^1{} ^7vs ^4{}^7 - DIFFERENCE: ^4{}"
                .format(round(avg_red), round(avg_blue), diff_rounded))
        else:
            channel.reply("^1{} ^7vs ^4{}^7 - Holy shit!"
                .format(round(avg_red), round(avg_blue)))

        minimum_suggestion_diff = self.get_cvar("qlx_balanceMinimumSuggestionDiff", int)
        if switch and switch[1] >= minimum_suggestion_diff:
            channel.reply("SUGGESTION: switch ^4{}^7 with ^4{}^7. Mentioned players can type ^4!a^7 to agree."
                .format(switch[0][0].clean_name, switch[0][1].clean_name))
            if not self.suggested_pair or self.suggested_pair[0] != switch[0][0] or self.suggested_pair[1] != switch[0][1]:
                self.suggested_pair = (switch[0][0], switch[0][1])
                self.suggested_agree = [False, False]
        else:
            i = random.randint(0, 99)
            if not i:
                channel.reply("Teens look ^4good!")
            else:
                channel.reply("Teams look good!")
            self.suggested_pair = None

        return True

    def cmd_do(self, player, msg, channel):
        """Forces a suggested switch to be done."""
        if self.suggested_pair:
            self.execute_suggestion()

    def cmd_agree(self, player, msg, channel):
        """After the bot suggests a switch, players in question can use this to agree to the switch."""
        if self.suggested_pair and not all(self.suggested_agree):
            p1, p2 = self.suggested_pair
            
            if p1 == player:
                self.suggested_agree[0] = True
            elif p2 == player:
                self.suggested_agree[1] = True

            if all(self.suggested_agree):
                # If the game's in progress and we're not in the round countdown, wait for next round.
                if self.game.state == "in_progress" and not self.in_countdown:
                    self.msg("The switch will be executed at the start of next round.")
                    return

                # Otherwise, switch right away.
                self.execute_suggestion()

    def cmd_ratings(self, player, msg, channel):
        gt = self.game.type_short
        if gt not in EXT_SUPPORTED_GAMETYPES:
            player.tell("This game mode is not supported by the balance plugin.")
            return minqlx.RET_STOP_ALL
        
        players = dict([(p.steam_id, gt) for p in self.players()])
        self.add_request(players, self.callback_ratings, channel)

    def callback_ratings(self, players, channel):
        # We check if people joined while we were requesting ratings and get them if someone did.
        teams = self.teams()
        current = self.players()
        gt = self.game.type_short

        for p in current:
            if p.steam_id not in players:
                d = dict([(p.steam_id, gt) for p in current])
                self.add_request(d, self.callback_ratings, channel)
                return

        if teams["free"]:
            free_sorted = sorted(teams["free"], key=lambda x: self.ratings[x.steam_id][gt]["elo"], reverse=True)
            free = ", ".join(["{}: ^4{}^7".format(p.clean_name, self.ratings[p.steam_id][gt]["elo"]) for p in free_sorted])
            channel.reply(free)
        if teams["red"]:
            red_sorted = sorted(teams["red"], key=lambda x: self.ratings[x.steam_id][gt]["elo"], reverse=True)
            red = ", ".join(["{}: ^1{}^7".format(p.clean_name, self.ratings[p.steam_id][gt]["elo"]) for p in red_sorted])
            channel.reply(red)
        if teams["blue"]:
            blue_sorted = sorted(teams["blue"], key=lambda x: self.ratings[x.steam_id][gt]["elo"], reverse=True)
            blue = ", ".join(["{}: ^4{}^7".format(p.clean_name, self.ratings[p.steam_id][gt]["elo"]) for p in blue_sorted])
            channel.reply(blue)
        if teams["spectator"]:
            spec_sorted = sorted(teams["spectator"], key=lambda x: self.ratings[x.steam_id][gt]["elo"], reverse=True)
            spec = ", ".join(["{}: {}".format(p.clean_name, self.ratings[p.steam_id][gt]["elo"]) for p in spec_sorted])
            channel.reply(spec)

    def suggest_switch(self, teams, gametype):
        """Suggest a switch based on average team ratings."""
        avg_red = self.team_average(teams["red"], gametype)
        avg_blue = self.team_average(teams["blue"], gametype)
        cur_diff = abs(avg_red - avg_blue)
        min_diff = 999999
        best_pair = None

        for red_p in teams["red"]:
            for blue_p in teams["blue"]:
                r = teams["red"].copy()
                b = teams["blue"].copy()
                b.append(red_p)
                r.remove(red_p)
                r.append(blue_p)
                b.remove(blue_p)
                avg_red = self.team_average(r, gametype)
                avg_blue = self.team_average(b, gametype)
                diff = abs(avg_red - avg_blue)
                if diff < min_diff:
                    min_diff = diff
                    best_pair = (red_p, blue_p)

        if min_diff < cur_diff:
            return (best_pair, cur_diff - min_diff)
        else:
            return None

    def team_average(self, team, gametype):
        """Calculates the average rating of a team."""
        avg = 0
        if team:
            for p in team:
                avg += self.ratings[p.steam_id][gametype]["elo"]
            avg /= len(team)

        return avg

    def execute_suggestion(self):
        p1, p2 = self.suggested_pair
        try:
            p1.update()
            p2.update()
        except minqlx.NonexistentPlayerError:
            return
        
        if p1.team != "spectator" and p2.team != "spectator":
            self.switch(self.suggested_pair[0], self.suggested_pair[1])
        
        self.suggested_pair = None
        self.suggested_agree = [False, False]
