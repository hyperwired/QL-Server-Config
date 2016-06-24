import minqlx, requests, redis

class serverbuild_node(minqlx.Plugin):
    def __init__(self):
        server = (self.get_cvar("qlx_redisAddress").split(":"))
        self.database = redis.Redis(host=server[0], port=server[1], db=15, password=self.get_cvar("qlx_redisPassword"))
        self.server_id = "server_" + (self.get_cvar("net_port"))[-1]

        self.add_command("getdbstuff", self.cmd_importcvarsfromdb, 0)
        
        self.player(0).tell(self.database.get("testkey"))

    def cmd_importcvarsfromdb(self, player, msg, channel):
        value = ""
        cvars = list(self.database.smembers("{}:cvars".format(self.server_id)))
        for cvar in cvars:
            value = self.database.get("{}:cvar:{}".format(self.server_id, cvar.decode()))
            self.msg("{} => {}".format(cvar.decode(), value.decode()))
