# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

API_URL = "https://glosbe.com/gapi/translate?from=eng&dest=eng&format=json&phrase={}"

import minqlx, requests, json
class dictionary(minqlx.Plugin):
    def __init__(self):
        self.add_command("define", self.define_term, usage="<term>")


    
    def define_term(self, player, msg, channel):
        @minqlx.thread
        def run(player, msg, channel):
            dictData = requests.get(API_URL.format("%20".join(msg[1:])), stream=True)
            jsonDict = json.loads(str(dictData.text))
            try:
                channel.reply("^4Definition: ^7{}^7".format(jsonDict["tuc"][0]["meanings"][0]["text"]))
            except Exception:
                channel.reply("^4Definition: ^1NO DEFINITIONS FOUND^7")
            
        if len(msg) < 2:
            return minqlx.RET_USAGE
        else:
            run(player, msg, channel)
            
    

        
        
