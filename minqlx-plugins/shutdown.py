# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

"""
    This plugin is loaded when we need to kick players off the server.
"""

import minqlx
import time

class shutdown(minqlx.Plugin):
    def __init__(self):
        self.add_command("shutdown", self.cmd_shutdown, 5, usage="<delay in minutes>")

    
    def cmd_shutdown(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            minutes = int(msg[1])
        except ValueError:
            player.tell("Invalid value.")
            return minqlx.RET_STOP_ALL

        self.msg("Server shutdown has been scheduled to occur in ^4{} minutes^7.".format(minutes))

        @minqlx.thread
        def shutdown(shutdownMinutes):
            shutdownSeconds = (shutdownMinutes * 60)
            mainDelay = (shutdownSeconds - 60)
            time.sleep(mainDelay)
            self.msg("The server will be shutting down in ^41 minute^7.")
            time.sleep(30)
            self.msg("The server will be shutting down in ^430 seconds^7.")
            time.sleep(15)
            self.center_print("This server is shutting down\nin ^115 seconds^7.")
            self.msg("This server will be shutting down in ^415 seconds^7.")
            self.play_sound("sound/world/klaxon1")
            time.sleep(5)
            self.center_print("This server is shutting down\nin ^110 seconds^7.")
            time.sleep(1)
            self.center_print("This server is shutting down\nin ^19 seconds^7.")
            time.sleep(1)
            self.center_print("This server is shutting down\nin ^18 seconds^7.")
            time.sleep(1)
            self.center_print("This server is shutting down\nin ^17 seconds^7.")
            time.sleep(1)
            self.center_print("This server is shutting down\nin ^16 seconds^7.")
            time.sleep(1)
            self.center_print("This server is shutting down\nin ^15 seconds^7.")
            time.sleep(1)
            self.play_sound("sound/world/klaxon1")
            self.center_print("This server is shutting down\nin ^14 seconds^7.")
            time.sleep(1)
            self.play_sound("sound/world/klaxon1")
            self.center_print("This server is shutting down\nin ^13 seconds^7.")
            time.sleep(1)
            self.play_sound("sound/world/klaxon1")
            self.center_print("This server is shutting down\nin ^12 seconds^7.")
            time.sleep(1)
            self.play_sound("sound/world/klaxon1")
            self.center_print("This server is shutting down\nin ^11 second^7.")
            time.sleep(1)
            self.play_sound("sound/world/buzzer")
            self.center_print("^1Shutting down.")
            time.sleep(1)
            minqlx.load_plugin("maintenance")

        shutdown(minutes)
