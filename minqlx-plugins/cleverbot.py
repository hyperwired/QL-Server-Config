# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
You can talk to cleverbot using !chat and it will respond.
"""

import minqlx
import requests
import random


class cleverbot(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_hook("chat", self.handle_chat)

        # Get an API key at cleverbot.io
        self.set_cvar("qlx_cleverbotUser", "04twdDLhNypTzdET")
        self.set_cvar("qlx_cleverbotKey", "pGJUZqVw7ogB5zj7zh3FXfDRHoJmzmjv")
        self.set_cvar("qlx_cleverbotNick", "^7Pur^4g^7obot")

        # Percentage chance to respond to chat, float between 0 and 1.
        self.set_cvar_limit_once("qlx_cleverbotChance", "0", "0", "1")

        self.created = False
        self.create()

    def handle_chat(self, player, msg, channel):
        """Responds to chat message qlx_cleverbotChance * 100 percent of the time"""
        if msg.startswith(self.get_cvar("qlx_commandPrefix")) or channel != "chat":
            return

        try:
            chance = self.get_cvar("qlx_cleverbotChance", float)
        except ValueError:
            self.logger.info("cleverbot: qlx_cleverbotChance is not a valid float.")
            return

        msg = msg.lower()
        if (random.random() < chance) or (self.clean_text(self.get_cvar("qlx_cleverbotNick")).lower() in msg) or ("bot" in msg):
            if self.bot_present():
                msg = self.clean_text(msg)
                self.ask(msg, channel)

    @minqlx.thread
    def create(self):
        """Creates the bot.
        Doc: https://docs.cleverbot.io/docs/getting-started"""
        response = self.post_data("https://cleverbot.io/1.0/create")
        if response:
            nick = self.get_cvar("qlx_cleverbotNick")
            self.msg("^7Bot called ^4{} ^7was created.".format(nick))
            self.created = True

    @minqlx.thread
    def ask(self, text, channel):
        """Doc: https://cleverbot.io/1.0/ask
        :param text: Text to send to the bot.
        :param channel: Channel to reply to.
        """
        response = self.post_data("https://cleverbot.io/1.0/ask", text)
        if response:
            nick = self.get_cvar("qlx_cleverbotNick")
            channel.reply("{}^7:^2 {}".format(nick, response["response"]))
            self.talk_beep()

    def post_data(self, url, text=''):
        """POSTS data to cleverbot.io
        :param url: The url to POST to, either /ask or /create.
        :param text: The text to send to the bot.
        :return: JSON response.
        """
        user = self.get_cvar("qlx_cleverbotUser")
        key = self.get_cvar("qlx_cleverbotKey")
        nick = self.get_cvar("qlx_cleverbotNick")
        if nick == "":
            self.msg("^3Bot nick cannot be blank.")
            return
        if user and key:
            payload = {"user": user, "key": key, "nick": nick, "text": text}
            r = requests.post(url, data=payload)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 400:
                self.msg("^1Bad request.")
            else:
                self.msg("^1Error: ^7{}, {}".format(r.status_code, r.reason))
        else:
            self.msg("^3You need to set qlx_cleverbotUser and qlx_cleverbotKey")

    def talk_beep(self, player=None):
        if not player:
            self.play_sound("sound/player/talk.ogg")
        else:
            self.play_sound("sound/player/talk.ogg", player)


    def bot_present(self):
        for player in self.players():
            if str(player.steam_id)[0] == "9":
                return True
        return False
