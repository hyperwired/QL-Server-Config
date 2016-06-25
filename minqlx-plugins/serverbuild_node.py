import minqlx, requests, redis

class serverbuild_node(minqlx.Plugin):
    def __init__(self):
        server = (self.get_cvar("qlx_redisAddress").split(":"))
        self.database = redis.Redis(host=server[0], port=server[1], db=15, password=self.get_cvar("qlx_redisPassword"))
        self.server_id = "server_" + (self.get_cvar("net_port"))[-1]

        self.add_command("setcvarsfromweb", self.cmd_setcvars, 0)
    

    def getCvars(self):
        cvars = list(self.database.smembers("{}:cvars".format(self.server_id)))
        cvardict = dict()
        for cvar in cvars:
            value = self.database.get("{}:cvar:{}".format(self.server_id, cvar.decode()))
            cvardict[cvar.decode()] = value.decode()

        return cvardict

    def cmd_setcvars(self, player, msg, channel):
        cvardict = self.getCvars()
        for cvar, value in cvardict.items():
           self.set_cvar(cvar, value)
           self.msg("^1Debug:^7 Set cvar ^2{}^7 to ^2{}^7.".format(cvar, value))
