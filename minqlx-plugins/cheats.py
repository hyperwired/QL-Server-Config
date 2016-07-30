import minqlx

class cheats(minqlx.Plugin):
    def __init__(self):
        self.add_hook("client_command", self.handle_client_command)
        self.add_command("add50", self.cmd_add50)
        
        self.specialCommands = ["noclip"]
        
        self.plugin_version = "0.9"

        self.noclipped = []
        
    def handle_client_command(self, player, cmd):
        if cmd in self.specialCommands:
            if self.db.has_permission(player.steam_id, 5):
                if cmd == self.specialCommands[0]: # noclip
                    if player.noclip:
                        player.noclip = False
                        player.tell("noclip OFF")
                    else:
                        player.noclip = True
                        player.tell("noclip ON")

                return minqlx.RET_STOP_ALL

    def cmd_add50(self, player, msg, channel):
        player.health += 50
        return minqlx.RET_STOP_ALL


    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4cheats.py^7 - version {}, created by Thomas Jones on 16/02/2016.".format(self.plugin_version))
