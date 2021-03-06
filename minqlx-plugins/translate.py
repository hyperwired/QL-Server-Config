# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# It tracksprovides commands to translate words and sentences,
# look up definitions, and provide autotranslation to personal
# languages.
#
# To use this plugin, you need to install 'textblob':
# 1. Open a terminal and type:  $ sudo pip install textblob
#
# 2. When it's done, restart the python module via:
# - /rcon pyrestart in quakelive
# - OR pyrestart in the server console
#
# 3. Once you have it installed, try a word definition.
# A one-time (10mb) file will be downloaded to the server.

import minqlx
import threading
import requests

VERSION = "v0.11"

try:
    import textblob
except:
    pass

# customizable vars
C = "^4"
DEFAULT_LANG = "en"
SERVER_DEFAULT = "en"
AUTO_TRANS_COMMANDS = False

PLAYER_KEY = "minqlx:players:{}"
LANG_KEY = PLAYER_KEY + ":language"
AUTO_KEY = PLAYER_KEY + ":autotranslate"

LANGS = {
'Afrikaans': 'af',
'Albanian': 'sq',
'Arabic': 'ar',
'Armenian': 'hy',
'Azerbaijani': 'az',
'Basque': 'eu',
'Belarusian': 'be',
'Bengali': 'bn',
'Bosnian': 'bs',
'Bulgarian': 'bg',
'Catalan': 'ca',
'Cebuano': 'ceb',
'Chichewa': 'ny',
'Chinese Simplified': 'zh-CN',
'Chinese Traditional': 'zh-TW',
'Croatian': 'hr',
'Czech': 'cs',
'Danish': 'da',
'Dutch': 'nl',
'English': 'en',
'Esperanto': 'eo',
'Estonian': 'et',
'Filipino': 'tl',
'Finnish': 'fi',
'French': 'fr',
'Galician': 'gl',
'Georgian': 'ka',
'German': 'de',
'Greek': 'el',
'Gujarati': 'gu',
'Haitian Creole': 'ht',
'Hausa': 'ha',
'Hebrew': 'iw',
'Hindi': 'hi',
'Hmong': 'hmn',
'Hungarian': 'hu',
'Icelandic': 'is',
'Igbo': 'ig',
'Indonesian': 'id',
'Irish': 'ga',
'Italian': 'it',
'Japanese': 'ja',
'Javanese': 'jw',
'Kannada': 'kn',
'Kazakh': 'kk',
'Khmer': 'km',
'Korean': 'ko',
'Lao': 'lo',
'Latin': 'la',
'Latvian': 'lv',
'Lithuanian': 'lt',
'Macedonian': 'mk',
'Malagasy': 'mg',
'Malay': 'ms',
'Malayalam': 'ml',
'Maltese': 'mt',
'Maori': 'mi',
'Marathi': 'mr',
'Mongolian': 'mn',
'Myanmar (Burmese)': 'my',
'Nepali': 'ne',
'Norwegian': 'no',
'Persian': 'fa',
'Polish': 'pl',
'Portuguese': 'pt',
'Punjabi': 'ma',
'Romanian': 'ro',
'Russian': 'ru',
'Serbian': 'sr',
'Sesotho': 'st',
'Sinhala': 'si',
'Slovak': 'sk',
'Slovenian': 'sl',
'Somali': 'so',
'Spanish': 'es',
'Sudanese': 'su',
'Swahili': 'sw',
'Swedish': 'sv',
'Tajik': 'tg',
'Tamil': 'ta',
'Telugu': 'te',
'Thai': 'th',
'Turkish': 'tr',
'Ukrainian': 'uk',
'Urdu': 'ur',
'Uzbek': 'uz',
'Vietnamese': 'vi',
'Welsh': 'cy',
'Yiddish': 'yi',
'Yoruba': 'yo',
'Zulu': 'zu',}

TAGS = {v: k for k, v in LANGS.items()}

class translate(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_command(("v_translate", "v_translation"), self.cmd_version)
        self.add_command("urban", self.cmd_urban, usage="<word>|<phrase>")
        self.add_command(("leet", "1337", "l33t"), self.cmd_leet, usage="<word>|<phrase>")
        self.add_command("languages", self.cmd_languages)
        self.add_hook("player_connect", self.handle_player_connect)
        self.buffer = []

        try:
            textblob
        except:
            self.help_textblob()
            return

        self.add_hook("chat", self.handle_chat)
        self.add_command(("translate", "trans"), self.cmd_translate, usage="<to> <query>")
        self.add_command(("stranslate", "strans"), self.cmd_silent_translate, usage="<to> <query>")
        self.add_command(("define", "def", "definition"), self.cmd_define, usage="<word>")
        self.add_command(("lang", "language"), self.cmd_language, usage="[<tag>|<language>]")
        self.add_command(("autotrans", "autotranslate"), self.cmd_auto_translate)
        self.add_command(("translatecmds", "transcmds", "transcommands", "translatecommands"), self.cmd_commands)

    def handle_chat(self, player, msg, channel):
        if not player: return
        if not msg: return

        # If you don't want the server to translate commands to people
        if not AUTO_TRANS_COMMANDS:
            # check if a command was spoken
            if msg[0].startswith("!"): return

        try:
            blob = textblob.TextBlob(msg)
            l = blob.detect_language()
            if l != SERVER_DEFAULT:
                #self.buffer.append(msg)
                # this is buffer now
                translations = {}
                for p in self.players():
                    # If it comes from this player, go to next
                    if p.id == player.id: continue
                    # If this player doesnt want auto trans, go to next
                    if not self.help_get_auto_pref(p): continue
                    # If this is the say_team from the other team, go to next
                    if channel == minqlx.RED_TEAM_CHAT_CHANNEL and p.team == 'blue': continue
                    if channel == minqlx.BLUE_TEAM_CHAT_CHANNEL and p.team == 'red': continue
                    # if this is the default language of the player, go to next
                    pref_tag = self.help_get_lang_tag(p)
                    if pref_tag == l: continue
                    # If there is no translation yet, add it
                    if not (pref_tag in translations):
                        translations[pref_tag] = blob.translate(to=pref_tag).raw
                    # Tell translation
                    p.tell("^4AutoTrans^7({}->{}){}: {}".format(l, pref_tag, C, translations[pref_tag]))


        except Exception as e:
            pass

    def cmd_define(self, player, msg, channel):
        if len(msg) != 2:
            return minqlx.RET_USAGE

        def download_wordnet():
            self.msg("^4TranslatePlugin: ^7Starting one-time package 'wordnet' download...")
            import nltk
            nltk.download('wordnet')
            self.msg("^4TranslatePlugin: ^7Wordnet downloading successfull. Installing... ^2complete!")
            try:
                callback(True)
            except Exception as e:
                self.msg("^1DefinitionError^7: {}.".format(e))

        def callback(second_time=False):
            try:
                w = textblob.Word(msg[1])
                defs = w.definitions
                if not defs:
                    channel.reply(C+"No results found for: {}".format(msg[1]))
                else:
                    channel.reply("^7Definition(s): " + C +  "'^7, ^4'".join(defs))
            except:
                if not second_time:
                    download_wordnet()
                    #threading.Thread(target=download_wordnet).start()


        try:
            threading.Thread(target=callback).start()
        except Exception as e:
            threading.Thread(target=download_wordnet).start()

    def cmd_commands(self, player, msg, channel):
        channel.reply("^7TranslationCommands: ^2!languages^7, ^2!lang^7, ^2!define^7, ^2!urban^7, ^2!translate^7, ^2!stranslate^7, ^2!autotrans")

    def cmd_silent_translate(self, player, msg, channel):
        player.tell("^4TranslateRequest: ^2{}".format(msg[1:]))
        self.cmd_translate(player, msg, channel, True)
        return minqlx.RET_STOP_ALL

    def cmd_translate(self, player, msg, channel, silent=False):
        if len(msg) < 3:
            return minqlx.RET_USAGE

        if msg[1].lower() in TAGS:
            to = msg[1]
        elif msg[1].title() in LANGS:
            to = LANGS[msg[1].title()]
        else:
            matches = []
            for lang in LANGS:
                if msg[1].title() in lang:
                    matches.append([lang, LANGS[lang]])
            if not matches:
                player.tell("^4No languages matched {}... Try ^2!languages ^4for a list.".format(msg[1]))
                return minqlx.RET_STOP_ALL
            elif len(matches) == 1:
                lang, tag = matches[0]
                to = tag
            else:
                _map = map(lambda pair: "{}->{}".format(pair[0], pair[1]), matches)
                player.tell("^4Multiple matches found: ^7" + ", ".join(list(_map)))
                return minqlx.RET_STOP_ALL


        message = " ".join(msg[2:])

        blob = textblob.TextBlob(message)
        try:
            translated = blob.translate(to=to).raw
        except Exception as e:
            translated = message

        output = "^7Translation: {}{}".format(C, translated)
        if silent:
            player.tell("^4Psst: " + output)
            return minqlx.RET_STOP_ALL
        channel.reply(output)


    @minqlx.delay(1)
    def help_textblob(self):
        self.msg("^1TranslationError^7: missing library textblob. Install via ^4$ sudo pip install textblob ^7and restart server.")


    def cmd_language(self, player, msg, channel):
        # if no arguments given, just check the language
        if len(msg) < 2:
            if self.help_get_auto_pref(player):
                tag = self.help_get_lang_tag(player)
                lang = TAGS.get(tag, DEFAULT_LANG)
                channel.reply("^7Your default language is: ^4{}^7({}). Use ^2!lang^7 to change it.".format(lang, tag))
                return
            else:
                channel.reply("^7AutoTranslation is turned off. Activate with !autotrans or !language X")
                return
        # otherwise try to set a new language
        else:
            lang = TAGS.get(msg[1].lower()) # try correct tag
            if lang:
                self.help_set_lang_tag(player, msg[1].lower())
                channel.reply("^7AutoTranslate language changed to: ^4{}^7({}).".format(lang, msg[1]))
                self.help_change_auto_pref(player, 1)
                return
            else: # try every language for a match
                maybe = []
                for lang in LANGS:
                    if msg[1].title() in lang:
                        maybe.append([lang, LANGS[lang]])
                if not maybe:
                    player.tell("^4No languages matched {}... Try ^2!languages ^4for a list.".format(msg[1]))
                    return minqlx.RET_STOP_ALL
                elif len(maybe) == 1:
                    lang, tag = maybe[0]
                    self.help_set_lang_tag(player, tag)
                    channel.reply("^7AutoTranslate language changed to: ^4{}^7({}).".format(lang, tag))
                    self.help_change_auto_pref(player, 1)
                    return
                else:
                    _map = map(lambda pair: "{}->{}".format(pair[0], pair[1]), maybe)
                    player.tell("^4Multiple matches found: ^7" + ", ".join(list(_map)))
                    return minqlx.RET_STOP_ALL



    def cmd_languages(self, player, msg, channel):
        _printable = map(lambda key: "^5{}^7({})".format(key, LANGS[key]), sorted(LANGS))
        player.tell("^4Supported languages: ^5" + ", ".join(list(_printable)))
        channel.reply("^7{} can open their console to see all the supported languages.".format(player.name))


    def cmd_auto_translate(self, player, msg, channel):
        # Get the preference
        old_pref = self.help_get_auto_pref(player)
        # Change it
        self.help_change_auto_pref(player)

        if old_pref:
            channel.reply("^7{} will stop receiving automatic translations.".format(player.name))
        else:
            tag = self.help_get_lang_tag(player)
            channel.reply("^7{} activated auto translations in their default language ({}).".format(player.name, tag))

    def cmd_urban(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        query = " ".join(msg[1:])
        url = 'https://mashape-community-urban-dictionary.p.mashape.com/define?term={}'.format(query)
        headers =  { "X-Mashape-Key": "CAwrPAMPB6msh3K3YsRflDE0hmswp14vd4tjsnwbD5rMUVQWvo" }

        self.help_fetch(player, query, url, headers, self.help_callback_urban)

    def cmd_leet(self, player, msg, channel):
        if len(msg)< 2:
            return minqlx.RET_USAGE
        query = "+".join(msg[1:])
        url = 'https://montanaflynn-l33t-sp34k.p.mashape.com/encode?text={}'.format(query)
        headers =  { "X-Mashape-Key": "CAwrPAMPB6msh3K3YsRflDE0hmswp14vd4tjsnwbD5rMUVQWvo" }
        self.help_fetch(player, query, url, headers, self.help_callback_leet)
        return minqlx.RET_STOP_ALL

    @minqlx.thread
    def help_fetch(self, player, query, url, headers, callback):
        res = requests.get(url, headers=headers)
        if res.status_code != requests.codes.ok:
            self.msg("^1RequestError^7: code {}.".format(res.status_code))
            return
        callback(player, query, res)

    def help_callback_urban(self, player, query, results):
        results = results.json()
        if results['result_type'] != "no_results":
            first_result = results['list'][0]
            definition = first_result['definition']
            example = first_result['example']
            self.msg("^5UrbanDef: ^7{}".format(definition))
            if example:
                self.help_delay_msg("^5UrbanExample: ^7{}".format(example))
        else:
            self.msg("{}No urban dict results found for: ".format(C, query))

    def help_callback_leet(self, player, query, results):
        self.msg("{}^7: ^2(!leet) {}".format(player.name, results))

    def help_get_auto_pref(self, player):
        key = AUTO_KEY.format(player.steam_id)
        if not (key in self.db): self.db[key] = 0
        return int(self.db[key])

    def help_change_auto_pref(self, player, force=0):
        key = AUTO_KEY.format(player.steam_id)
        self.db[key] = force or 0 if self.help_get_auto_pref(player) else 1

    def cmd_version(self, player, msg, channel):
        self.check_version(channel=channel)

    @minqlx.thread
    def check_version(self, player=None, channel=None):
        url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/{}.py".format(self.__class__.__name__)
        res = requests.get(url)
        last_status = res.status_code
        if res.status_code != requests.codes.ok: return
        for line in res.iter_lines():
            if line.startswith(b'VERSION'):
                line = line.replace(b'VERSION = ', b'')
                line = line.replace(b'"', b'')
                # If called manually and outdated
                if channel and VERSION.encode() != line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's ^4{}^7 plugin ^1outdated^7 version ^4{}^7.".format(self.__class__.__name__, VERSION))
                # If called manually and alright
                elif channel and VERSION.encode() == line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's latest ^4{}^7 plugin version ^4{}^7.".format(self.__class__.__name__, VERSION))
                # If routine check and it's not alright.
                elif player and VERSION.encode() != line:
                    time.sleep(15)
                    try:
                        player.tell("^3Plugin update alert^7:^4 {}^7's latest version is ^4{}^7 and you're using ^4{}^7!".format(self.__class__.__name__, line.decode(), VERSION))
                    except Exception as e: minqlx.console_command("echo {}".format(e))
                return

    def help_get_lang_tag(self, player):
        # formulate key
        key = LANG_KEY.format(player.steam_id)
        # if no language defined yet, set the default
        if not (key in self.db): self.help_set_lang_tag(player, DEFAULT_LANG)
        # return tag
        return self.db[key]

    def help_set_lang_tag(self, player, tag):
        # formulate key
        key = LANG_KEY.format(player.steam_id)
        # set it (after a quick test that it exists)
        if TAGS.get(tag): self.db[key] = tag

    @minqlx.delay(0.3)
    def help_delay_msg(self, message):
        self.msg(message)

    def handle_player_connect(self, player):
        if self.db.has_permission(player, 5):
            self.check_version(player=player)
