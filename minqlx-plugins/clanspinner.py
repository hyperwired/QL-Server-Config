# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

import minqlx
import time

class clanspinner(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("player_disconnect", self.handle_player_disconnect)

        self.add_command("clanspinner", self.cmd_clanspinner, 5, usage="debug commands: [break, continue, initialise]")
        
        self.kolos = []

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

            
    @minqlx.next_frame
    def handle_player_loaded(self, player):
        if player.clan == "^0kolo^6.":
            self.kolos.append(player)
            if len(self.kolos) == 1:
                self.keep_going = True
                self.start_rotating()
            self.msg("A ^0kolo^6.^7 has connected!")
    
    def handle_player_disconnect(self, player, reason):
        try:
            self.kolos.remove(player)
            if len(self.kolos) <= 1:
                self.keep_going = False
                
        except KeyError:
            return
        
    def initialise(self):
        for player in self.players():
            if player.clan == "^0kolo^6.":
                self.kolos.append(player)

        if len(self.kolos) >= 1:
            self.keep_going = True
            self.start_rotating()
                
    @minqlx.thread
    def start_rotating(self):
        while True:
            if (len(self.kolos) == 0 or self.keep_going == False):
                break

            for k in self.kolos:
                k.clan = "^0k^6.^0olo"

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^0ko^6.^0lo"

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^0kol^6.^0o"

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^0kolo^6."

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^0kol^6.^0o"

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^0ko^6.^0lo"

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^0k^6.^0olo"

            time.sleep(0.5)

            for k in self.kolos:
                k.clan = "^6.^0kolo"

            time.sleep(0.5)

            

            
