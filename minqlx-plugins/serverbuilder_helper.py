import minqlx, time
from random import randint

class serverbuilder_helper(minqlx.Plugin):
    def __init__(self):
        self.add_hook("map", self.handle_map)
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("client_command", self.handle_client_command)
        self.add_hook("player_loaded", self.handle_player_loaded)

        self.set_cvar_once("qlx_infiniteAmmo", "0") # 0=normal ammo, 1=always, 2=during warmup only

        self.Owner = False
        
    @minqlx.next_frame   
    def handle_map(self, mapname, factory):
        # turn on infinite ammo for warm-up
        if self.get_cvar("qlx_infiniteAmmo", int) != 0:
            self.set_cvar("g_infiniteAmmo", "1")

        # correct starting weapons to gaunt+rail if instagib is on
        if self.get_cvar("g_instaGib", bool):
            self.set_cvar("g_startingWeapons", "65")

    def handle_game_countdown(self):
        self.play_sound("sound/items/protect3.ogg")

        if self.get_cvar("qlx_infiniteAmmo", int) == 2:
            self.set_cvar("g_infiniteAmmo", "0")

    def handle_client_command(self, player, command):
        command = command.split()
        if command[0].lower() == "addmod":
            if player is self.Owner:
                try:
                    target = self.player(int(command[1]))
                except:
                    player.tell("Invalid ID.")
                    return minqlx.RET_STOP_ALL
                
                self.addmod(target)
                return minqlx.RET_STOP_ALL

        if command[0].lower() == "demote":
            if player is self.Owner:
                try:
                    target = self.player(int(command[1]))
                except:
                    player.tell("Invalid ID.")
                    return minqlx.RET_STOP_ALL

                if target is self.Owner:
                    player.tell("You cannot demote the server owner.")
                    return minqlx.RET_STOP_ALL
                
                self.demote(target)
                return minqlx.RET_STOP_ALL

    def handle_player_loaded(self, player):
        if str(player.steam_id)[0] == "9": return
        if not self.Owner:
            self.Owner = player
        
