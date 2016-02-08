# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx
import time

class clanspinner(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("unload", self.handle_plugin_unload)
        
        self.add_command("clanspinner", self.cmd_clanspinner, 5, usage="debug commands: [break, continue, initialise]")
        
        self.clanMembers = []
        self.clanTag = "^0kolo^6."
        self.clanAnimation = ["^0k^6.^0olo", "^0ko^6.^0lo", "^0kol^6.^0o", "^0kolo^6.", "^0kol^6.^0o", "^0ko^6.^0lo", "^0k^6.^0olo", "^6.^0kolo"]
        self.clanAnimationDelay = 0.5
        
        self.keep_going = True
        self.initialise()


    def cmd_clanspinner(self, player, msg, channel):
        if len(msg) <= 1:
            return minqlx.RET_USAGE
        
        if msg[1].lower() == "break":
            self.keep_going = False

        if msg[1].lower() == "continue":
            self.keep_going = True
            
        if msg[1].lower() == "initialise":
            self.initialise()

    def handle_plugin_unload(self, plugin):
        if plugin == "clanspinner":
            self.keep_going = False
            
    @minqlx.next_frame
    def handle_player_loaded(self, player):
        if player.clan == self.clanTag:
            self.clanMembers.append(player)
            if len(self.clanMembers) == 1:
                self.keep_going = True
                self.start_rotating()
    
    def handle_player_disconnect(self, player, reason):
        try:
            self.clanMembers.remove(player)
            if len(self.clanMembers) <= 1:
                self.keep_going = False
        except KeyError:
            return
        
    def initialise(self):
        for player in self.players():
            if player.clan == self.clanTag:
                self.clanMembers.append(player)

        if len(self.clanMembers) >= 1:
            self.keep_going = True
            self.start_rotating()
                
    @minqlx.thread
    def start_rotating(self):
        while True:
            for text in self.clanAnimation:
                # Make sure we're still supposed to run, otherwise exit.
                if (len(self.clanMembers) == 0 or self.keep_going == False):
                    break
                
                # Set the clan tag to the next animation in the list.
                for p in self.clanMembers:
                    p.clan = text

                # Wait for a bit until we begin again.
                time.sleep(self.clanAnimationDelay)
