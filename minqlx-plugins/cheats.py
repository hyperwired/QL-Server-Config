import minqlx

class cheats(minqlx.Plugin):
    def __init__(self):
        self.add_hook("client_command", self.handle_client_command)
        
        self.specialCommands = ["noclip"]
        
        self.plugin_version = "0.9"

        self.noclipped = []
        
    def handle_client_command(self, player, cmd):
        if cmd in self.specialCommands:
            if self.db.has_permission(player.steam_id, 5):
                if cmd == self.specialCommands[0]: # noclip
                    if player in self.noclipped:
                        self.noclipped.remove(player)
                        player.noclip = False
                        player.tell("noclip OFF")
                    else:
                        self.noclipped.append(player)
                        player.noclip = True
                        player.tell("noclip ON")

                return minqlx.RET_STOP_ALL


    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4cheats.py^7 - version {}, created by Thomas Jones on 16/02/2016.".format(self.plugin_version))
