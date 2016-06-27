import minqlx, requests, redis, time
from random import randint

class serverbuilder_node(minqlx.Plugin):
    def __init__(self):
        server = (self.get_cvar("qlx_redisAddress").split(":"))
        self.database = redis.Redis(host=server[0], port=server[1], db=15, password=self.get_cvar("qlx_redisPassword"))

        self.set_cvar("qlx_owner", "76561198213481765")
        
        self.add_command("getinfo", self.cmd_getinfo, 0)
        
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("player_disconnect", self.handle_player_disconnect)

        self.server_id = "server_" + self.get_cvar("sv_identifier")
        self.server_location = str.replace(self.get_cvar("sv_location"), " ", "-")
        self.server_key = self.server_location.lower() + ":" + self.server_id
        
        self.is_ready = False

        for key in (self.database.keys("{}:*".format(self.server_key))):
            self.database.delete(key)
    
        self.initialise()


    def initialise(self):
        self.database.set("{}:receiving".format(self.server_key), "1")
        self.checkForConfiguration()

    @minqlx.thread
    def checkForConfiguration(self):
        while True:
            time.sleep(3)
            try:
                active = bool((self.database.get("{}:active".format(self.server_key))).decode())
            except:
                active = False
            if active:
                self.database.set("{}:received".format(self.server_key), "1")
                self.database.set("{}:receiving".format(self.server_key), "0")
                break

        self.configureServer(self.getCvars())
        
    def configureServer(self, config):
        cvars = self.getCvars()
        for cvar, value in cvars.items():
            self.set_cvar(cvar, value)

        for plugin in (self.database.smembers("{}:plugins".format(self.server_key))):
            minqlx.load_plugin(plugin.decode())
            
        self.is_ready = True

    def getCvars(self):
        cvars = list(self.database.smembers("{}:cvars".format(self.server_key)))
        cvardict = dict()
        for cvar in cvars:
            value = self.database.get("{}:cvar:{}".format(self.server_key, cvar.decode()))
            cvardict[cvar.decode()] = value.decode()

        return cvardict

    def handle_player_connect(self, player):
        if not self.is_ready:
            return "^{}http://master.quakelive.tomtecsolutions.com.au/serverbuild\n".format(randint(0,7))

    def handle_player_loaded(self, player):
        player.tell("Run ^2!getinfo^7 to test values went across correctly.\nDisconnecting will shut this server down and reset it.")
        
    def handle_player_disconnect(self, player, reason):
        for key in (self.database.keys("{}:*".format(self.server_key))):
            self.database.delete(key)

        minqlx.console_command("quit")
        
    def cmd_getinfo(self, player, msg, channel):
        cvardict = self.getCvars()
        for cvar, value in cvardict.items():
            self.msg("^1Debug:^7 CVAR: ^2{}^7 => ^2{}^7.".format(cvar, value))

        for plugin in (self.database.smembers("{}:plugins".format(self.server_key))):
            self.msg("^1Debug:^7 Plugin: ^2{}^7 loaded.".format(plugin.decode()))
