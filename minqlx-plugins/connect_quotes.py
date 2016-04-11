# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).

QUOTES = [
    "Sit Ubu, sit! Good dog!",
    "Time is an illusion, lunchtime doubly so.",
    "Don't whizz on the electric fence!",
    "Roses are red, violets are blue, I'm schizophrenic, and so am I.",
    "There are lots of people who mistake their imagination for their memory.",
    "A woman's mind is cleaner than a man's: She changes it more often.",
    "Always borrow money from a pessimist. He won’t expect it back.",
    "The scientific theory I like best is that the rings of Saturn are composed entirely of lost airline luggage.",
    "Friendship is like peeing on yourself: everyone can see it, but only you get the warm feeling that it brings.",
    "Dogs have masters. Cats have staff.",
    "It is a mistake to think you can solve any major problems just with potatoes.",
    "Flying is learning how to throw yourself at the ground and miss.",
    "Isn't it enough to see that a garden is beautiful without having to believe that there are fairies at the bottom of it too?",
    "I may not have gone where I intended to go, but I think I have ended up where I needed to be.",
    "Anyone who is capable of getting themselves made President should on no account be allowed to do the job.",
    "A common mistake that people make when trying to design something completely foolproof is to underestimate the ingenuity of complete fools.",
    "In the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move.",
    "I love deadlines. I like the whooshing sound they make as they fly by.",
    "The major difference between a thing that might go wrong and a thing that cannot possibly go wrong is that when a thing that cannot possibly go wrong goes wrong it usually turns out to be impossible to get at and repair."
]


import minqlx
from random import randint
class connect_quotes(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_loaded", self.handle_player_loaded)

        self.add_command("tomtec_versions", self.cmd_showversion)
        
        self.plugin_version = "1.0"

        self.playerConnectedYetList = []
        
        
    def handle_player_connect(self, player):
        if player not in self.playerConnectedYetList:
            self.playerConnectedYetList.append(player)
            randomNumber = randint(0, (len(QUOTES) - 1))
            randomQuote = QUOTES[randomNumber]
            return randomQuote

    def handle_player_loaded(self, player):
        try:
            self.playerConnectedYetList.remove(player)
        except:
            return

    def cmd_showversion(self, player, msg, channel):
        channel.reply("^4connect_quotes.py^7 - version {}, created by Thomas Jones on 08/04/2016.".format(self.plugin_version))
