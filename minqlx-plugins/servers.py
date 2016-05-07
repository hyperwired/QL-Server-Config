# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx, socket
import valve.source.a2s as a2s

SERVERS = [
    "103.18.40.15:27960", # purgery sydney
    "103.18.40.15:27961",
    "103.18.40.15:27962",
    "103.18.40.15:27963",
    "103.18.40.15:27964",
    "103.18.40.15:27965",
    "103.18.40.15:27966",
    "103.18.40.15:27967",
    "103.18.40.15:27968",
    "43.245.164.133:27960", # purgery perth
    "43.245.164.133:27961",
    "43.245.164.133:27962",
    "43.245.164.133:27963",
    "43.245.164.133:27964",
    "43.245.164.133:27965",
    "43.245.164.133:27966",
    "43.245.164.133:27967",
    "43.245.164.133:27968",
    "119.252.27.101:27960", # purgery adelaide
    "119.252.27.101:27961",
    "119.252.27.101:27962",
    "119.252.27.101:27963",
    "119.252.27.101:27964",
    "119.252.27.101:27965",
    "119.252.27.101:27966",
    "119.252.27.101:27967",
    "119.252.27.101:27968",
    "101.100.142.120:27960", # purgery auckland
    "101.100.142.120:27961",
    "101.100.142.120:27962",
    "101.100.142.120:27963",
    "101.100.142.120:27964",
    "101.100.142.120:27965",
    "101.100.142.120:27966",
    "101.100.142.120:27967",
    "101.100.142.120:27968"
]

class servers(minqlx.Plugin):
    def __init__(self):
        self.add_command(("servers", "network"), self.cmd_servers)
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.0"


    def cmd_servers(self, player, msg, channel):
        servers = SERVERS
        self.get_servers(servers, player)
        return minqlx.RET_STOP_ALL

    @minqlx.thread
    def get_servers(self, servers, player):
        res = "{} | {} | {}\n".format("IP".center(21), "Server Name".center(60), "Player Count")
        for server in servers:
            hostname, player_count = self.get_server_info(server)
            if player_count[0].isdigit():
                players = [int(n) for n in player_count.split("/")]
            if players[0] == players[1]:
                player_count = "^3{}".format(player_count)
            else:
                player_count = "^2{}".format(player_count)
            res += "{:21} | {:60} | {}^7\n".format(server, hostname, player_count)

        player.tell(res)

    def get_server_info(self, server):
        address = (server.split(":") + [27960])[:2]
        try:
            address[1] = int(address[1])
            server = a2s.ServerQuerier(address)
            info = server.get_info()
            return info['server_name'].lstrip(" "), "{player_count}/{max_players}".format(**info)
        except ValueError as e:
            self.logger.error(e)
            return "Error: Invalid port", "^1..."
        except socket.gaierror as e:
            self.logger.error(e)
            return "Error: Invalid/nonexistent address", "^1..."
        except a2s.NoResponseError as e:
            self.logger.error(e)
            return "Error: Timed out", "^1..."

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4servers.py^7 - version {}, originally created by ^6kanzo^7, readapted by Thomas Jones on 11/04/2016.".format(self.plugin_version))
