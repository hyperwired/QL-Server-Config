# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Created by Thomas Jones on 14/12/2015 - thomas@tomtecsolutions.com

import minqlx
import requests
import json
import threading

class locations(minqlx.Plugin):
    def __init__(self):
        self.add_command(("loc", "location"), self.cmd_location, usage="<id>")
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.plugin_version = "1.0"

    @minqlx.thread    
    def cmd_location(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        try:
            player_ip = self.player(int(msg[1])).ip
            player_name = self.player(int(msg[1])).name
        except:
            channel.reply("^1Invalid Client ID.^7 Enter a valid client ID to see their approximate location.")
            return
    
        ipData = requests.get('http://freegeoip.net/json/{}'.format(player_ip), stream=True)
        ipData = str(ipData.text)
        ipDataParsed = json.loads(ipData)

        channel.reply("{}^7's approximate location details:\n    Country Code: {}\n    Country Name: {}\n    Region Code: {}\n    Region Name: {}\n    City: {}\n    Post Code: {}\n    Time Zone: {}".format(player_name, ipDataParsed['country_code'], ipDataParsed['country_name'], ipDataParsed['region_code'], ipDataParsed['region_name'], ipDataParsed['city'], ipDataParsed['zip_code'], ipDataParsed['time_zone']))
        return
    
    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4locations.py^7 - version {}, created by Thomas Jones on 21/01/2016.".format(self.plugin_version))
