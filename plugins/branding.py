# This has been created by TomTec Solutions

import minqlx

class branding(minqlx.Plugin):
    def __init__(self):
        self.add_hook("new_game", self.brand_map)
        self.add_hook("game_countdown", self.sponsor_message)
        self.add_hook("player_loaded", self.welcome_message)
        self.add_hook("game_start", self.gamestart_message)
        self.add_hook("game_end", self.gameend_message)
        
        
    def brand_map(self):
        minqlx.set_configstring(3, "^4The Purgery^7")
        minqlx.set_configstring(678, "Sponsored by ^5TomTec Solutions^7 (^2quakesupport@tomtecsolutions.com^7).")
        minqlx.set_configstring(679, "Visit our IRC channel on QuakeNet, ^4#thepurgery^7.")

    def sponsor_message(self):
        minqlx.send_server_command(None, "cp \"^4The Purgery\n^7Sponsored by ^5TomTec Solutions^7\"\n")
        self.play_sound("sound/items/protect3.ogg")
        
    def welcome_message(self, player):
        minqlx.send_server_command(player.id, "cp \"^7Welcome to ^4The Purgery^7\"\n")
        #self.play_sound("sound/items/protect3.ogg") # waaaa, cthulhu's crying about it
        
    def gamestart_message(self):
        #minqlx.send_server_command(None, "cp \"^4The Purgery\n^5Sponsored by TomTec Solutions^7\"\n")
        #self.play_sound("sound/items/protect3.ogg")
        pass
    
    def gameend_message(self):
        #channel.tell("Hurrah!")
        #self.play_sound("sound/items/protect3.ogg")
        pass
