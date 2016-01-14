#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# quakestart.sh - quake live multiple server spawning script.
# created by Thomas Jones on 09/09/15.
# thomas@tomtecsolutions.com

# Defining globally used variables/configuration.
export qMinqlxRedisPassword=$(<~/localConfig-redispassword.txt)
export qServerLocation=$(<~/localConfig-serverLocation.txt)
export qServerLocationHyphenated=`echo $qServerLocation | sed 's/ /-/g'`
export qGlobalOptions="+set sv_location $qServerLocation"
export qPathToMinqlxStartScript="~/steamcmd/steamapps/common/qlds/run_server_x64_minqlx.sh +set qlx_redisPassword $qMinqlxRedisPassword $qGlobalOptions"
export qPathToVanillaStartScript="~/steamcmd/steamapps/common/qlds/run_server_x64.sh $qGlobalOptions"
export qIrcNickname="$qServerLocationHyphenated-$1"

# Purgery specific variables/configuration.
export qPurgeryOwnerSteam64ID="76561198213481765"
export qRconPasswordPurgery=$(<~/localConfig-rconPassword-purgery.txt)
export qPurgeryStart="$qPathToMinqlxStartScript \
+set qlx_owner $qPurgeryOwnerSteam64ID \
+set qlx_plugins \"DEFAULT, tomtec_logic, tp_fun, fun, balance, irc, aliases, votestats, custom_votes, cleverbot\" \
+set qlx_ircPassword $qRconPasswordPurgery \
+set qlx_ircRelayChannel #thepurgery \
+set qlx_ircServer irc.tomtecsolutions.com.au \
+set qlx_chatlogs 20 \
+set qlx_motdSound 0 \
+set qlx_ircColors 0 \
+set g_inactivity 120"

sponsortag="$qServerLocation,TomTec Solutions"
gameport=`expr $1 + 27960`
rconport=`expr $1 + 28960`
servernum=`expr $1 + 0`

# Starts servers with different settings, based off the process number parsed
# as argument 1 by supervisord.

echo "========== QuakeStart.sh has started. =========="
echo "========= $(date) ========="
cd ~/steamcmd/steamapps/common/qlds/baseq3

if [ $1 -eq 0 ]
# starting PQL CA 1
then
echo "Starting clan arena server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "     #$servernum The Purgery $qServerLocation PQL - Clan Arena" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_voteFlags "9320" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_pqlca.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 1 \
    +set qlx_balanceApi elo_b
elif [ $1 -eq 1 ]
# starting VQL CA 1
then
echo "Starting clan arena server 2..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "    #$servernum The Purgery $qServerLocation VQL - Clan Arena" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_voteFlags "9320" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_vqlca.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set g_damage_lg 6 \
    +set qlx_rulesetLocked 1 \
    +set qlx_disablePlayerRemoval 0
elif [ $1 -eq 2 ]
# starting PQL Race 1...
then
echo "Starting race server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "    #$servernum The Purgery $qServerLocation - Race" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "grappling hook,crouch slide,$sponsortag" \
    +set g_voteFlags "0" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 0 \
   	+set bot_nochat 1 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_pqlrace.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 3 ]
# starting PQL FFA 1...
then
echo "Starting free for all server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "    #$servernum The Purgery $qServerLocation PQL - Free For All" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_voteFlags "9320" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
   	+set bot_nochat 1 \
    +set g_damage_lg 6 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_pqlffa.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 1
elif [ $1 -eq 4 ]
# starting vql duel 1...
then
echo "Starting VQL duel server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "    #$servernum The Purgery $qServerLocation VQL - Duel" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_voteFlags "9320" \
    +set g_allowSpecVote 0 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_damage_lg 6 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_vqlduel.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 1
elif [ $1 -eq 5 ]
# starting PQL Multi-Gametype 1...
then
echo "Starting PQL Multi-Gametype server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname " #$servernum The Purgery $qServerLocation PQL - Multi-Gametype" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_pqlmulti.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set g_damage_lg 6 \
    +set g_voteFlags 0 \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 6 ]
# starting VQL MultiGame 1...
then
echo "Starting multi game type VQL server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname " #$servernum The Purgery $qServerLocation VQL - Multi-Gametype" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_accessFile "access_purgery.txt" \
    +set sv_mappoolFile "mappool_default.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 7 ]
# starting Scrim SERVER 1...
then
echo "Starting scrim SERVER server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname " #$servernum The Purgery $qServerLocation - Unmoderated Scrim Server" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "unmoderated,$sponsortag" \
    +set g_allowSpecVote 1 \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_accessFile "access_staffonly.txt" \
    +set sv_mappoolFile "mappool_ca.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 0 \
    +set qlx_serverExemptFromModeration 1
elif [ $1 -eq 8 ]
# starting reythe (sub580)...
then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]
then
echo "Starting reythe's duel house (sub580) 1..."
exec $qPathToVanillaStartScript \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "Reythe's Duel House" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$(<~/localConfig-rconPassword-reythe.txt)" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "$(<~/localConfig-rconPassword-reythe.txt)" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$qServerLocation" \
    +set bot_enable 0 \
    +set g_accessFile "access_reythe.txt" \
    +set sv_mappoolFile "mappool_reythe.txt" \
    +set fs_homepath ~/.quakelive/REYTHE-SUB580 \
    +set g_damage_lg 6 \
    +set g_voteFlags 8 \
    +set sv_location "$qServerLocation"
else
echo "This system is not intended to host reythe (sub580) server."
fi
elif [ $1 -eq 9 ]
# starting pit (sub586)...
then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]
then
echo "Starting pit clan server (sub586) 1..."
exec $qPathToMinqlxStartScript \
    +set net_strict 1 \
    +set qlx_redisDatabase 2 \
    +set net_port $gameport \
    +set qlx_owner $qPurgeryOwnerSteam64ID \
    +set qlx_plugins "DEFAULT, branding, fun" \
    +set qlx_serverBrandName "^1=^4P^1i^4T^1=^7 Clan Server" \
    +set qlx_serverBrandTopField "Check out our forums at ^2http://intothepit.org^7." \
    +set qlx_serverBrandBottomField "" \
    +set sv_hostname "=PiT= Clan Server" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$(<~/localConfig-rconPassword-pit.txt)" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "$(<~/localConfig-rconPassword-pit.txt)" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$qServerLocation" \
    +set bot_enable 1 \
    +set bot_nochat 1 \
    +set g_accessFile "access_pit.txt" \
    +set sv_mappoolFile "mappool_pit.txt" \
    +set fs_homepath ~/.quakelive/PIT-SUB586 \
    +set g_damage_lg 6 \
    +set sv_location "$qServerLocation"
else
echo "This system is not intended to host pit clan (sub586) server."
fi
elif [ $1 -eq 10 ]
# starting 4sg tournament server CA
then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]
then
echo "Starting starting 4sg tournament server CA..."
exec $qPathToMinqlxStartScript \
    +set net_strict 1 \
    +set qlx_redisDatabase 1 \
    +set net_port $gameport \
    +set qlx_owner $qPurgeryOwnerSteam64ID \
    +set sv_hostname "4SGv2 - Tournament CA" \
    +set qlx_plugins "DEFAULT, branding, custom_votes" \
    +set qlx_serverBrandName "^54SGv2 Tournament - Clan Arena^7" \
    +set qlx_serverBrandTopField "Run by ^54Seasons Gaming^7. ^2http://4seasonsgaming.com^7." \
    +set qlx_serverBrandBottomField "Admins: ^4mickzerofive, zlr, phy1um^7." \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$(<~/localConfig-rconPassword-4sg.txt)" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "$(<~/localConfig-rconPassword-4sg.txt)" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$qServerLocation,4Seasons Gaming" \
    +set bot_enable 0 \
    +set g_accessFile "access_4seasonsgaming.txt" \
    +set sv_mappoolFile "mappool_4sg_ca.txt" \
    +set fs_homepath ~/.quakelive/4sg-tournament-ca \
    +set g_damage_lg 6 \
    +set sv_location "$qServerLocation" \
    +set g_password "$(<~/localConfig-rconPassword-4sg.txt)" \
    +set qlx_teamsizeMaximum 2 \
    +set teamsize 2
else
echo "This system is not intended to host 4sg tournament server CA"
fi
elif [ $1 -eq 11 ]
# starting 4sg tournament server DUEL
then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]
then
echo "Starting starting 4sg tournament server DUEL..."
exec $qPathToMinqlxStartScript \
    +set net_strict 1 \
    +set qlx_redisDatabase 1 \
    +set net_port $gameport \
    +set qlx_owner $qPurgeryOwnerSteam64ID \
    +set sv_hostname "4SGv2 - Tournament DUEL" \
    +set qlx_plugins "DEFAULT, branding, custom_votes" \
    +set qlx_serverBrandName "^54SGv2 Tournament - Duel^7" \
    +set qlx_serverBrandTopField "Run by ^54Seasons Gaming^7. ^2http://4seasonsgaming.com^7." \
    +set qlx_serverBrandBottomField "Admins: ^4mickzerofive, zlr, phy1um^7." \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$(<~/localConfig-rconPassword-4sg.txt)" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "$(<~/localConfig-rconPassword-4sg.txt)" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$qServerLocation,4Seasons Gaming" \
    +set bot_enable 0 \
    +set g_accessFile "access_4seasonsgaming.txt" \
    +set sv_mappoolFile "mappool_4sg_duel.txt" \
    +set fs_homepath ~/.quakelive/4sg-tournament-duel \
    +set g_damage_lg 6 \
    +set sv_location "$qServerLocation" \
    +set g_password "$(<~/localConfig-rconPassword-4sg.txt)" \
    +set g_voteFlags 2048
else
echo "This system is not intended to host 4sg tournament server DUEL"
fi
fi
