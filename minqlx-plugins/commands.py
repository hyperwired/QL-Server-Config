# This plugin created by stakly <root@qw3rty.org>
# Copyright (c) 2016 stakly
#
# This plugin response permitted command list to player, based on currently loaded plugins in markdown

import minqlx


class commands(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_command("me", self.cmd_mycommands, permission=0)

    @minqlx.thread
    def cmd_mycommands(self, player, msg, channel):

        """Response permitted command list to player, based on currently loaded plugins in markdown."""

        prefix = self.get_cvar("qlx_commandPrefix")
        cmds = {}
        for cmd in minqlx.COMMANDS.commands:
            if cmd.permission not in cmds:
                cmds[cmd.permission] = [cmd]
            else:
                cmds[cmd.permission].append(cmd)

        ident = player.steam_id
        player_perm = `self.db.get_permission(ident)

        out = "Commands List for players with your permission level (^4{}^7)\n".format(player_perm)
        for perm in sorted(cmds.keys()):
            for cmd in sorted(cmds[perm], key=lambda x: x.plugin.__class__.__name__):
                name = prefix + cmd.name[0] if cmd.prefix else cmd.name[0]
                if perm <= player_perm:
                    out += "^4{}^7".format(name)
                    if len(cmd.name) > 1:  # Aliases?
                        out += " ^7(or: "
                        for alias in cmd.name[1:]:
                            name_alias = prefix + alias if cmd.prefix else alias
                            out += "^4{}^7, ".format(name_alias)
                        out = out[:-2] + ")"

                # Docstring.
                if cmd.handler.__doc__:
                    out += " ^7{}".format(cmd.handler.__doc__)

                # Usage
                if cmd.usage:
                    out += "\n   ^7Command Usage: ^4{} {}^7\n".format(name, cmd.usage)

                else:
                    out += "\n"

        player.tell(out)
