# minqlx - Extends Quake Live's dedicated server with extra functionality and scripting.
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
import collections

class Plugin():
    """The base plugin class.

    Every plugin must inherit this or a subclass of this. It does not support any database
    by itself, but it has a *database* static variable that must be a subclass of the
    abstract class :class:`minqlx.database.AbstractDatabase`. This abstract class requires
    a few methods that deal with permissions. This will make sure that simple plugins that
    only care about permissions can work on any database. Abstraction beyond that is hard,
    so any use of the database past that point will be uncharted territory, meaning the
    plugin will likely be database-specific unless you abstract it yourself.

    Permissions for commands can be overriden in the config. If you have a plugin called
    ``my_plugin`` with a command ``my_command``, you could override its permission
    requirement by adding ``perm_my_command: 3`` under a ``[my_plugin]`` header.
    This allows users to set custom permissions without having to edit the scripts.

    .. warning::
        I/O is the bane of single-threaded applications. You do **not** want blocking operations
        in code called by commands or events. That could make players lag. Helper decorators
        like :func:`minqlx.thread` can be useful.
    
    """
    # Static dictionary of plugins currently loaded for the purpose of inter-plugin communication.
    _loaded_plugins = {}
    # The database driver class the plugin should use.
    database = None

    def __init__(self):
        self._hooks = []
        self._commands = []

    def __str__(self):
        return self.name

    @property
    def db(self):
        """The database instance."""
        if not self.database:
            raise RuntimeError("Plugin '{}' does not have a database driver."
                .format(self.name))
        elif not hasattr(self, "_db_instance"):
            self._db_instance = self.database(self)
        
        return self._db_instance

    @property
    def name(self):
        """The name of the plugin."""
        return self.__class__.__name__
    
    @property
    def plugins(self):
        """A dictionary containing plugin names as keys and plugin instances
        as values of all currently loaded plugins.

        """
        return self._loaded_plugins.copy()

    @property
    def hooks(self):
        """A list of all the hooks this plugin has."""
        if not hasattr(self, "_hooks"):
            self._hooks = []
        return self._hooks.copy()

    @property
    def commands(self):
        """A list of all the commands this plugin has registered."""
        if not hasattr(self, "_commands"):
            self._commands = []
        return self._commands.copy()

    @property
    def game(self):
        """A Game instance."""
        try:
            return minqlx.Game()
        except minqlx.NonexistentGameError:
            return None

    @property
    def logger(self):
        """An instance of :class:`logging.Logger`, but initialized for this plugin."""
        return minqlx.get_logger(self)
    
    # TODO: Document plugin methods.
    def add_hook(self, event, handler, priority=minqlx.PRI_NORMAL):
        if not hasattr(self, "_hooks"):
            self._hooks = []
            
        self._hooks.append((event, handler, priority))
        minqlx.EVENT_DISPATCHERS[event].add_hook(self.name, handler, priority)

    def remove_hook(self, event, handler, priority=minqlx.PRI_NORMAL):
        if not hasattr(self, "_hooks"):
            self._hooks = []
            return
        
        minqlx.EVENT_DISPATCHERS[event].remove_hook(self.name, handler, priority)
        self._hooks.remove((event, handler, priority))

    def add_command(self, name, handler, permission=0, channels=None, exclude_channels=(), priority=minqlx.PRI_NORMAL, client_cmd_pass=False, client_cmd_perm=5, prefix=True, usage=""):
        if not hasattr(self, "_commands"):
            self._commands = []
        
        cmd = minqlx.Command(self, name, handler, permission, channels, exclude_channels, client_cmd_pass, client_cmd_perm, prefix, usage)    
        self._commands.append(cmd)
        minqlx.COMMANDS.add_command(cmd, priority)

    def remove_command(self, name, handler):
        if not hasattr(self, "_commands"):
            self._commands = []
            return
        
        for cmd in self._commands:
            if cmd.name == name and cmd.handler == handler:
                minqlx.COMMANDS.remove_command(cmd)

    @classmethod
    def get_cvar(cls, name, return_type=str):
        """Gets the value of a cvar as a string.

        :param name: The name of the cvar.
        :type name: str
        :param return_type: The type the cvar should be returned in.
            Supported types: str, int, float, bool, list, tuple

        """
        res = minqlx.get_cvar(name)
        if return_type == str:
            return res
        elif return_type == int:
            return int(res)
        elif return_type == float:
            return float(res)
        elif return_type == bool:
            return bool(int(res))
        elif return_type == list:
            return [s.strip() for s in res.split(",")]
        elif return_type == set:
            return {s.strip() for s in res.split(",")}
        elif return_type == tuple:
            return tuple([s.strip() for s in res.split(",")])
        else:
            raise ValueError("Invalid return type: {}".format(return_type))

    @classmethod
    def set_cvar(cls, name, value, flags=0):
        """Sets a cvar. If the cvar exists, it will be set as if set from the console,
        otherwise create it.

        :param name: The name of the cvar.
        :type name: str
        :param value: The value of the cvar.
        :type value: Anything with an __str__ method.
        :param flags: The flags to set if, and only if, the cvar does not exist and has to be created.
        :type flags: int
        :returns: True if a new cvar was created, False if an existing cvar was set.
        :rtype: bool

        """
        if cls.get_cvar(name) == None:
            minqlx.set_cvar(name, value, flags)
            return True
        else:
            minqlx.console_command("{} \"{}\"".format(name, value))
            return False

    @classmethod
    def set_cvar_limit(cls, name, value, minimum, maximum, flags=0):
        """Sets a cvar with upper and lower limits. If the cvar exists, it will be set
        as if set from the console, otherwise create it.

        :param name: The name of the cvar.
        :type name: str
        :param value: The value of the cvar.
        :type value: int, float
        :param minimum: The minimum value of the cvar.
        :type value: int, float
        :param maximum: The maximum value of the cvar.
        :type value: int, float
        :param flags: The flags to set if, and only if, the cvar does not exist and has to be created.
        :type flags: int
        :returns: True if a new cvar was created, False if an existing cvar was set.
        :rtype: bool

        """
        if cls.get_cvar(name) == None:
            minqlx.set_cvar(name, value, flags)
            return True
        else:
            minqlx.console_command("{} \"{}\"".format(name, value))
            return False

    @classmethod
    def set_cvar_once(cls, name, value, flags=0):
        """Sets a cvar. If the cvar exists, do nothing.

        :param name: The name of the cvar.
        :type name: str
        :param value: The value of the cvar.
        :type value: Anything with an __str__ method.
        :param flags: The flags to set if, and only if, the cvar does not exist and has to be created.
        :type flags: int
        :returns: True if a new cvar was created, False if an existing cvar was set.
        :rtype: bool

        """
        return minqlx.set_cvar_once(name, value, flags)

    @classmethod
    def set_cvar_limit_once(cls, name, value, minimum, maximum, flags=0):
        """Sets a cvar with upper and lower limits. If the cvar exists, not do anything.

        :param name: The name of the cvar.
        :type name: str
        :param value: The value of the cvar.
        :type value: int, float
        :param minimum: The minimum value of the cvar.
        :type value: int, float
        :param maximum: The maximum value of the cvar.
        :type value: int, float
        :param flags: The flags to set if, and only if, the cvar does not exist and has to be created.
        :type flags: int
        :returns: True if a new cvar was created, False if an existing cvar was set.
        :rtype: bool

        """
        return minqlx.set_cvar_limit_once(name, value, minimum, maximum, flags)

    @classmethod
    def players(cls):
        """Get a list of all the players on the server."""
        return minqlx.Player.all_players()

    @classmethod
    def player(cls, name, player_list=None):
        """Get a Player instance from the name, client ID,
        or Steam ID. Assumes [0, 64) to be a client ID
        and [64, inf) to be a Steam ID.
        
        """
        # In case 'name' isn't a string.
        if isinstance(name, minqlx.Player):
            return name
        elif isinstance(name, int) and name >= 0 and name < 64:
            try:
                return minqlx.Player(name)
            except minqlx.NonexistentPlayerError:
                return None


        if not player_list:
            players = cls.players()
        else:
            players = player_list

        if isinstance(name, int) and name >= 64:
            for p in players:
                if p.steam_id == name:
                    return p
        else:
            cid = cls.client_id(name, players)
            if cid:
                for p in players:
                    if p.id == cid:
                        return p

        return None
    
    @classmethod
    def msg(cls, msg, chat_channel="chat", **kwargs):
        """Send a message to the chat, or any other channel."""
        if isinstance(chat_channel, minqlx.AbstractChannel):
            chat_channel.reply(msg, **kwargs)
        elif chat_channel == minqlx.CHAT_CHANNEL:
            minqlx.CHAT_CHANNEL.reply(msg, **kwargs)
        elif chat_channel == minqlx.RED_TEAM_CHAT_CHANNEL:
            minqlx.RED_TEAM_CHAT_CHANNEL.reply(msg, **kwargs)
        elif chat_channel == minqlx.BLUE_TEAM_CHAT_CHANNEL:
            minqlx.BLUE_TEAM_CHAT_CHANNEL.reply(msg, **kwargs)
        elif chat_channel == minqlx.CONSOLE_CHANNEL:
            minqlx.CONSOLE_CHANNEL.reply(msg, **kwargs)
        else:
            raise ValueError("Invalid channel.")
    
    @classmethod
    def console(cls, text):
        """Prints text in the console."""
        minqlx.console_print(str(text))

    @classmethod
    def clean_text(cls, text):
        """Removes color tags from text."""
        return minqlx.re_color_tag.sub("", text)
    
    @classmethod
    def colored_name(cls, name, player_list=None):
        """Get the colored name of a decolored name."""
        if isinstance(name, minqlx.Player):
            return name.name

        if not player_list:
            players = cls.players()
        else:
            players = player_list
        
        clean = cls.clean_text(name).lower()
        for p in players:
            if p.clean_text.lower() == clean:
                return p.name

        return None

    @classmethod
    def client_id(cls, name, player_list=None):
        """Get a player's client id from the name, client ID,
        Player instance, or Steam ID. Assumes [0, 64) to be
        a client ID and [64, inf) to be a Steam ID.
        
        """
        if isinstance(name, int) and name >= 0 and name < 64:
            return name
        elif isinstance(name, minqlx.Player):
            return name.id

        if not player_list:
            players = cls.players()
        else:
            players = player_list

        # Check Steam ID first, then name.
        if isinstance(name, int) and name >= 64:
            for p in players:
                if p.steam_id == name:
                    return p.id
        else:
            clean = cls.clean_text(name).lower()
            for p in players:
                if p.clean_name.lower() == clean:
                    return p.id

        return None

    @classmethod
    def find_player(cls, name, player_list=None):
        """Find a player based on part of a players name.

        :param name: A part of someone's name.
        :type name: str
        :returns: A list of players that had that in their names.

        """
        if not player_list:
            players = cls.players()
        else:
            players = player_list

        if not name:
            return players

        res = []
        for p in players:
            if cls.clean_text(name.lower()) in p.clean_name.lower():
                res.append(p)
        
        return res

    @classmethod
    def teams(cls, player_list=None):
        """Get a dictionary with the teams as keys and players as values."""
        if not player_list:
            players = cls.players()
        else:
            players = player_list

        res = collections.OrderedDict.fromkeys(minqlx.TEAMS.values())
        for key in res:
            res[key] = []

        for p in players:
            res[p.team].append(p)

        return res

    @classmethod
    def tell(cls, msg, recipient, **kwargs):
        """Send a tell (private message) to someone.

        :param msg: The message to be sent.
        :type msg: str
        :param recipient: The player that should receive the message.
        :type recipient: str/int/minqlx.Player
        :returns: bool -- True if succeeded, False otherwise.
        :raises: ValueError
        """
        minqlx.TellChannel(recipient).reply(msg, **kwargs)

    @classmethod
    def is_vote_active(cls):
        if minqlx.get_configstring(9):
            return True
        else:
            return False

    @classmethod
    def current_vote_count(cls):
        yes = minqlx.get_configstring(10)
        no = minqlx.get_configstring(11)
        if yes and no:
            return int(yes), int(no)
        else:
            return None

    @classmethod
    def callvote(cls, vote, display, time=30):
        if not cls.is_vote_active():
            # Tell vote_started's dispatcher that it's a vote called by the server.
            minqlx.EVENT_DISPATCHERS["vote_started"].caller(None)
            minqlx.callvote(vote, display, time)
            return True

        return False
    
    @classmethod
    def force_vote(cls, pass_it):
        if pass_it == True or pass_it == False:
            return minqlx.force_vote(pass_it)
        
        raise ValueError("pass_it must be either True or False.")

    @classmethod
    def teamsize(cls, size):
        minqlx.Game().teamsize = size

    @classmethod
    def kick(cls, player, reason=""):
        cid = cls.client_id(player)
        if cid == None:
            raise ValueError("Invalid player.")

        if not reason:
            minqlx.kick(cid, None)
        else:
            minqlx.kick(cid, reason)
    
    @classmethod
    def shuffle(cls):
        minqlx.Game().shuffle()

    @classmethod
    def cointoss(cls):
        # TODO: Call cointoss directly and implement cointoss().
        pass

    @classmethod
    def change_map(cls, new_map, factory=None):
        if not factory:
            minqlx.Game().map = new_map
        else:
            minqlx.console_command("map {} {}".format(new_map, factory))
    
    @classmethod
    def switch(cls, player, other_player):
        p1 = cls.player(player)
        p2 = cls.player(other_player)

        if not p1:
            raise ValueError("The first player is invalid.")
        elif not p2:
            raise ValueError("The second player is invalid.")

        t1 = p1.team
        t2 = p2.team
        
        if t1 == t2:
            raise ValueError("Both players are on the same team.")
        else:
            cls.put(p1, t2)
            cls.put(p2, t1)

    @classmethod
    def play_sound(cls, sound_path, player=None):
        if not sound_path or "music/" in sound_path.lower():
            return False

        if player:
            minqlx.send_server_command(player.id, "playSound {}".format(sound_path))
        else:
            minqlx.send_server_command(None, "playSound {}".format(sound_path))
        return True

    @classmethod
    def play_music(cls, music_path, player=None):
        if not music_path or "sound/" in music_path.lower():
            return False

        if player:
            minqlx.send_server_command(player.id, "playMusic {}".format(music_path))
        else:
            minqlx.send_server_command(None, "playMusic {}".format(music_path))
        return True

    @classmethod
    def stop_sound(cls, player=None):
        minqlx.send_server_command(player.id if player else None, "clearSounds")

    @classmethod
    def stop_music(cls, player=None):
        minqlx.send_server_command(player.id if player else None, "stopMusic")

    @classmethod
    def slap(cls, player, damage=0):
        cid = cls.client_id(player)
        if cid == None:
            raise ValueError("Invalid player.")

        minqlx.console_command("slap {} {}".format(cid, damage))

    @classmethod
    def slay(cls, player):
        cid = cls.client_id(player)
        if cid == None:
            raise ValueError("Invalid player.")

        minqlx.console_command("slay {}".format(cid))

    # ====================================================================
    #                         ADMIN COMMANDS
    # ====================================================================

    @classmethod
    def timeout(cls):
        return minqlx.Game.timeout()

    @classmethod
    def timein(cls):
        return minqlx.Game.timein()

    @classmethod
    def allready(cls):
        return minqlx.Game.allready()

    @classmethod
    def pause(cls):
        return minqlx.Game.pause()

    @classmethod
    def unpause(cls):
        return minqlx.Game.unpause()

    @classmethod
    def lock(cls, team=None):
        return minqlx.Game.lock(team)

    @classmethod
    def unlock(cls, team=None):
        return minqlx.Game.unlock(team)

    @classmethod
    def put(cls, player, team):
        return minqlx.Game.put(player, team)

    @classmethod
    def mute(cls, player):
        return minqlx.Game.mute(player)

    @classmethod
    def unmute(cls, player):
        return minqlx.Game.unmute(player)

    @classmethod
    def tempban(cls, player):
        # TODO: Add an optional reason to tempban.
        return minqlx.Game.tempban(player)

    @classmethod
    def ban(cls, player):
        return minqlx.Game.ban(player)

    @classmethod
    def unban(cls, player):
        return minqlx.Game.unban(player)

    @classmethod
    def opsay(cls, msg):
        return minqlx.Game.opsay(msg)

    @classmethod
    def addadmin(cls, player):
        return minqlx.Game.addadmin(player)

    @classmethod
    def addmod(cls, player):
        return minqlx.Game.addmod(player)

    @classmethod
    def demote(cls, player):
        return minqlx.Game.demote(player)

    @classmethod
    def abort(cls):
        return minqlx.Game.abort()

    @classmethod
    def addscore(cls, player, score):
        return minqlx.Game.addscore(player, score)

    @classmethod
    def addteamscore(cls, team, score):
        return minqlx.Game.addteamscore(team, score)

    @classmethod
    def setmatchtime(cls, time):
        return minqlx.Game.setmatchtime(time)
