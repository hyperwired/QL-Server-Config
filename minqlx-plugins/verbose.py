import minqlx

class verbose(minqlx.Plugin):
    def __init__(self):
        self.add_hook("client_command", self.handle_client_command)
        self.add_hook("server_command", self.handle_server_command)
        
        self.plugin_version = "0.9"

    
    def handle_client_command(self, player, cmd):
        self.msg("^1Verbose: ^7Client > Server: {} issued: {}".format(player.id, cmd))

    def handle_server_command(self, player, cmd):
        self.msg("^1Verbose: ^7Server > Client: {} issued: {}".format(player.id, cmd))

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4verbose.py^7 - version {}, created by Thomas Jones on 18/02/2016.".format(self.plugin_version))
