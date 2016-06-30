# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# This file contains community ideas that may be found to be in bad taste. These views do not represent the views of TomTec Solutions

import minqlx
from random import randint

class tp_fun(minqlx.Plugin):
    def __init__(self):
        self.add_command("penislength", self.cmd_penlen) # Junkyard requested
        self.add_command(("vaginadepth", "vaginaldepth", "vaginialdepth"), self.cmd_vagdep) # Junkyard requested
        self.add_command(("msg", "message"), self.cmd_screenmessage, 1, usage="[id] <text>") # Merozollo requested
        self.add_command(("breastsize", "cupsize", "brasize", "boobsize"), self.cmd_boobsize) # 0regonn requested
        self.add_command("fuckyou", self.cmd_printfu, 1)
        self.add_command("bury", self.cmd_bury, 3, usage="<id>")
        self.add_command("digup", self.cmd_digup, 3, usage="<id>")
        self.add_command("smile", self.cmd_elated_emoji) # Purger requested
        self.add_command("pentagram", self.cmd_pentagram, 1, usage="<id>") # Merozollo requested
        self.add_command("tomtec_versions", self.cmd_showversion)

        self.add_hook("chat", self.handle_chat)
        
        self.plugin_version = "1.5"

    def handle_chat(self, player, msg, channel):
        words = msg
        
        if ("When Bio wins, I grins." in words) or ("When Bio dies, I cries." in words): # 0regonn's being gay again
            @minqlx.delay(1)
            def f():
                self.msg("^7Pur^4g^7er: ^2gay") # na na na naa naa, ghost-purgers!
                self.talk_beep()
            f()

    def talk_beep(self, player=None):
        if not player:
            self.play_sound("sound/player/talk.ogg")
        else:
            self.play_sound("sound/player/talk.ogg", player)
            
    def cmd_elated_emoji(self, player, msg, channel):
        num1 = randint(0,6)
        num2 = randint(0,6)
        minqlx.client_command(player.id, "say ^{}:^{}D".format(num1, num2))
        return minqlx.RET_STOP_ALL
        
    def cmd_pentagram(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        try:
            pentagramee = self.player(int(msg[1]))
        except:
            player.tell("Invalid ID.")
            return

        pentagramee.powerups(battlesuit=3)
        self.msg("{}^7 has got the ^1Pentagram of Protection^7!".format(pentagramee.name))
        
    def cmd_penlen(self, player, msg, channel):
        playerName = player.clean_name
        randNum = randint(0,11)
        if randNum == 0:
            channel.reply("^7{}^7's penis length: ^40 inches (inverted!)^7".format(player))
        else:
            channel.reply("^7{}^7's penis length: ^4{} inch(es)^7".format(player, randNum))

    def cmd_vagdep(self, player, msg, channel):
        playerName = player.clean_name
        randNum = randint(0,11)
        if randNum == 0:
            channel.reply("^7{}^7's vaginial depth: ^40 inches (are you trans?)^7".format(player))
        else:
            channel.reply("^7{}^7's vaginial depth: ^4{} inch(es)^7".format(player, randNum))

    def cmd_boobsize(self, player, msg, channel):
        playerName = player.clean_name
        randNum = randint(0,5)
        if randNum == 0:
            cupSize = "A"
        elif randNum == 1:
            cupSize = "B"
        elif randNum == 2:
            cupSize = "C"
        elif randNum == 3:
            cupSize = "D"
        elif randNum == 4:
            cupSize = "DD"
        elif randNum == 5:
            cupSize = "Z (discount wheelbarrow at Bunnings!)"

        channel.reply("^7{}^7's cup size: ^4{}^7".format(playerName, cupSize))
           
    def cmd_screenmessage(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        if (msg[1].isdigit()):
            self.player(int(msg[1])).center_print(" ".join(msg[2:]))
        else:
            self.center_print(" ".join(msg[1:]))

        self.play_sound("sound/world/klaxon2.wav")

    def cmd_printfu(self, player, msg, channel):
        minqlx.send_server_command(None, "cp \"^0FUCK YOU\n^1FUCK YOU\n^2FUCK YOU\n^3FUCK YOU\n^4FUCK YOU\n^5FUCK YOU\n^6FUCK YOU\"\n")

    def cmd_bury(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            i = int(msg[1])
            target_player = self.player(i)
            if not (0 <= i < 64) or not target_player:
                raise ValueError
        except ValueError:
            player.tell("Invalid ID.")
            return minqlx.RET_STOP_ALL

        affected = int(msg[1])
        self.player(affected).position(z=player.state.position.z - 40)
        
    def cmd_digup(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            i = int(msg[1])
            target_player = self.player(i)
            if not (0 <= i < 64) or not target_player:
                raise ValueError
        except ValueError:
            player.tell("Invalid ID.")
            return minqlx.RET_STOP_ALL
        
        affected = int(msg[1])
        self.player(affected).position(z=player.state.position.z + 50)

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4tp_fun.py^7 - version {}, created by the community.".format(self.plugin_version))
