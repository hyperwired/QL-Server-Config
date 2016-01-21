# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Created by Thomas Jones on 14/12/2015 - thomas@tomtecsolutions.com

import minqlx
import minqlx.database

class ips(minqlx.Plugin):
    database = minqlx.database.Redis
    
    def __init__(self):
        self.add_command("ip", self.cmd_ip, usage="<id>")
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.0"

    def cmd_ip(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        try:
            steam_id = self.player(int(msg[1])).steam_id
            player_name = self.player(int(msg[1])).name
        except:
            channel.reply("^1Invalid Client ID.^7 Enter a valid client ID to see a list of IP addresses they've used on this server.")
            return
        
        key = "minqlx:players:{}:ips".format(steam_id)
        out = list(self.db.smembers(key))
        channel.reply("{}^7 has played on this server using the following IP addresses:".format(player_name))
        channel.reply(" ^4*^7  {}".format("   \n ^4*^7  ".join(out)))
        
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4ips.py^7 - version {}, created by Thomas Jones on 21/01/2016.".format(self.plugin_version))
