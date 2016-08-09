#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# quakestart.sh - quake live multiple server spawning script.
# created by Thomas Jones on 09/09/15.
# thomas@tomtecsolutions.com

# Defining globally used variables/configuration.
export qMinqlxRedisPassword=$(<~/localConfig-redisPassword.txt)
export qServerLocation=$(<~/localConfig-serverLocation.txt)
export qServerLocationHyphenated=`echo $qServerLocation | sed 's/ /-/g'`
export qGlobalOptions="+set sv_location $qServerLocation"
export qPathToMinqlxStartScript="~/steamcmd/steamapps/common/qlds/run_server_x64_minqlx.sh +set qlx_redisPassword $qMinqlxRedisPassword $qGlobalOptions"
export qPathToVanillaStartScript="~/steamcmd/steamapps/common/qlds/run_server_x64.sh $qGlobalOptions"
export qCommlinkServerName="$qServerLocationHyphenated-$1"

# Purgery specific variables/configuration.
export qPurgeryOwnerSteam64ID="76561198213481765"
export qRconPasswordPurgery=$(<~/localConfig-rconPassword-purgery.txt)
export qPurgeryServerTitle="^4The Purgery^7 - $qServerLocation - ^2#$1^7"
export qPurgeryStart="$qPathToMinqlxStartScript \
+set qlx_owner $qPurgeryOwnerSteam64ID \
+set qlx_plugins DEFAULT, tomtec_logic, botmanager, cleverbot, tp_fun, fun, balance, commlink, aliases, votestats, custom_votes, votemanager, branding, q3resolver, queue, pummel \
+set qlx_commlinkIdentity thepurgery \
+set qlx_commlinkServerName $qCommlinkServerName
+set qlx_chatlogs 20 \
+set qlx_motdSound 0 \
+set g_inactivity 120 \
+set qlx_serverBrandName $qPurgeryServerTitle \
+set qlx_serverBrandTopField ^7Sponsored by ^5TomTec Solutions^7. Visit the forums at ^2forum.thepurgery.com^7. \
+set qlx_serverBrandBottomField ^5www.4seasonsgaming.com^7, home to the Australian and New Zealand Quake community. \
+set qlx_loadedMessage Welcome to ^4The Purgery^7 \
+set qlx_countdownMessage ^5Good luck, and have fun.^7 \
+set qlx_endOfGameMessage ^2Good game!^7 \
+set qlx_purgeryDonationMessages 0 \
+set qlx_visitForumMessages 0"

sponsortag="$qServerLocation,TomTec Solutions"
gameport=`expr $1 + 27960`
rconport=`expr $1 + 28960`
servernum=`expr $1 + 0`

# Starts servers with different settings, based off the process number parsed
# as argument 1 by supervisord.

echo "========== QuakeStart.sh has started. =========="
echo "========= $(date) ========="
cd ~/steamcmd/steamapps/common/qlds/baseq3

if [ $1 -eq 0 ]; then
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
    +set bot_nochat 0 \
    +set sv_mappoolFile "mappool_pqlca.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 1 \
    +set qlx_balanceApi elo_b \
    +set qlx_leaverBan 1 \
    +set g_warmupReadyDelay 90 \
    +set g_warmupReadyDelayAction 2
elif [ $1 -eq 1 ]; then
echo "Starting vql clan arena server 1..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "    #$servernum The Purgery $qServerLocation VQL - Clan Arena #1 (Unrestricted)" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_voteFlags "9320" \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 0 \
    +set bot_nochat 1 \
    +set sv_mappoolFile "mappool_vqlca.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set g_damage_lg 6 \
    +set qlx_rulesetLocked 1 \
    +set qlx_disablePlayerRemoval 0 \
    +set qlx_privatiseVotes 1 \
    +set qlx_strictVql 0 \
    +set teamsize 5
elif [ $1 -eq 2 ]; then
echo "Starting vql clan arena server 2..."
exec $qPurgeryStart \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "    #$servernum The Purgery $qServerLocation VQL - Clan Arena #2 (Max 6v6)" \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password "$qRconPasswordPurgery" \
    +set zmq_rcon_port $rconport \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password "eggplant" \
    +set zmq_stats_port $gameport \
    +set sv_tags "$sponsortag" \
    +set g_voteFlags "9320" \
    +set g_allowVoteMidGame 1 \
    +set bot_enable 0 \
    +set bot_nochat 1 \
    +set sv_mappoolFile "mappool_vqlca.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set g_damage_lg 6 \
    +set qlx_rulesetLocked 1 \
    +set qlx_disablePlayerRemoval 0 \
    +set qlx_teamsizeMaximum 6 \
    +set qlx_privatiseVotes 1 \
    +set qlx_strictVql 1 \
    +set teamsize 5
  elif [ $1 -eq 3 ]; then
  echo "Starting clan arena server 3..."
  exec $qPurgeryStart \
      +set net_strict 1 \
      +set net_port $gameport \
      +set sv_hostname "    #$servernum The Purgery $qServerLocation VQL - Clan Arena #3 (Max 5v5)" \
      +set zmq_rcon_enable 1 \
      +set zmq_rcon_password "$qRconPasswordPurgery" \
      +set zmq_rcon_port $rconport \
      +set zmq_stats_enable 1 \
      +set zmq_stats_password "eggplant" \
      +set zmq_stats_port $gameport \
      +set sv_tags "$sponsortag" \
      +set g_voteFlags "9320" \
      +set g_allowVoteMidGame 1 \
      +set bot_enable 0 \
      +set bot_nochat 1 \
      +set sv_mappoolFile "mappool_vqlca.txt" \
      +set fs_homepath ~/.quakelive/$gameport \
      +set qlx_ircNickname "$qIrcNickname" \
      +set g_damage_lg 6 \
      +set qlx_rulesetLocked 1 \
      +set qlx_disablePlayerRemoval 0 \
      +set qlx_teamsizeMaximum 5 \
      +set qlx_privatiseVotes 1 \
      +set qlx_strictVql 1 \
      +set teamsize 5
elif [ $1 -eq 4 ]; then
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
    +set sv_mappoolFile "mappool_pqlrace.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 5 ]; then
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
    +set sv_mappoolFile "mappool_pqlffa.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 6 ]; then
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
    +set sv_mappoolFile "mappool_vqlduel.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 1 \
    +set g_timeoutCount 2 \
    +set g_timeoutLen 90
elif [ $1 -eq 7 ]; then
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
    +set sv_mappoolFile "mappool_pqlmulti.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set g_damage_lg 6 \
    +set g_voteFlags 0 \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 8 ]; then
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
    +set sv_mappoolFile "mappool_default.txt" \
    +set fs_homepath ~/.quakelive/$gameport \
    +set qlx_ircNickname "$qIrcNickname" \
    +set qlx_rulesetLocked 0
elif [ $1 -eq 9 ]; then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]; then
echo "Starting reythe's duel house (sub580) 1..."
exec $qPathToVanillaStartScript \
    +set net_strict 1 \
    +set net_port $gameport \
    +set sv_hostname "Reythe's Duel House" \
    +set zmq_rcon_enable 0 \
    +set zmq_stats_enable 1 \
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
elif [ $1 -eq 10 ]; then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]; then
echo "Starting pit clan server (sub586) 1..."
exec $qPathToMinqlxStartScript \
    +set net_strict 1 \
    +set qlx_redisDatabase 2 \
    +set net_port $gameport \
    +set qlx_owner $qPurgeryOwnerSteam64ID \
    +set qlx_plugins "DEFAULT, branding, fun, balance, votestats" \
    +set qlx_serverBrandName "^1=^4P^1i^4T^1=^7 Clan Server" \
    +set qlx_serverBrandTopField "Check out our forums at ^2http://intothepit.org^7." \
    +set qlx_serverBrandBottomField "" \
    +set sv_hostname "=PiT= Clan Server" \
    +set zmq_stats_enable 1 \
    +set sv_tags "$qServerLocation" \
    +set g_accessFile "access_pit.txt" \
    +set sv_mappoolFile "mappool_pit.txt" \
    +set fs_homepath ~/.quakelive/PIT-SUB586 \
    +set g_damage_lg 6 \
    +set sv_location "$qServerLocation" \
    +set qlx_connectMessage Connected to the ^1=^4P^1i^4T^1=^7 Clan Server \
    +set qlx_loadedMessage Welcome to ^4The ^1=^4P^1i^4T^1=^7 Clan Server^7 \
    +set qlx_countdownMessage ^1Good luck, and have fun!^7 \
    +set qlx_balanceUrl stats.quakelive.tomtecsolutions.com.au:8080
else
echo "This system is not intended to host pit clan (sub586) server."
fi
elif [ $1 -eq 11 ]; then
if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]; then
echo "Starting toey's server (sub613) 1..."
exec $qPathToMinqlxStartScript \
    +set net_strict 1 \
    +set qlx_redisDatabase 6 \
    +set net_port $gameport \
    +set qlx_owner $qPurgeryOwnerSteam64ID \
    +set qlx_plugins "DEFAULT, balance, custom_votes, branding" \
    +set sv_hostname "TOEY'S FFA" \
    +set zmq_rcon_enable 0 \
    +set zmq_stats_enable 1 \
    +set sv_tags "$qServerLocation" \
    +set g_accessFile "access_toey.txt" \
    +set sv_mappoolFile "mappool_ffa.txt" \
    +set fs_homepath ~/.quakelive/TOEY-SUB613 \
    +set sv_location "$qServerLocation, TOEY" \
    +set sv_mappoolFile "mappool_toey.txt" \
    +set qlx_serverBrandName "TOEY'S FFA"
else
echo "This system is not intended to host toey's (sub613) server."
fi
fi

#elif [ $1 -ge 12 ] && [ $1 -le 16 ]; then
#if [ $(hostname) == "sydney.quakelive.tomtecsolutions.com.au" ]; then
#servernum=`expr $1 - 11`
#echo "Starting starting 4sg tournament server $servernum..."
#exec $qPathToMinqlxStartScript \
#    +set net_strict 1 \
#    +set qlx_redisDatabase 1 \
#    +set net_port $gameport \
#    +set qlx_owner $qPurgeryOwnerSteam64ID \
#    +set sv_hostname "4SG CA Tournament Server #$servernum" \
#    +set qlx_plugins "DEFAULT, branding" \
#    +set qlx_serverBrandName "^54SG CA Tournament Server^7" \
#    +set qlx_serverBrandTopField "Run by ^54Seasons Gaming^7. ^2http://4seasonsgaming.com^7. Admins: mickzerofive, zlr, phy1um, luna, grrrdian^7." \
#    +set qlx_serverBrandBottomField "Server $servernum of 6." \
#    +set zmq_rcon_enable 0 \
#    +set zmq_stats_enable 1 \
#    +set zmq_stats_password "eggplant" \
#    +set zmq_stats_port $gameport \
#    +set sv_tags "$qServerLocation,4Seasons Gaming" \
#    +set bot_enable 0 \
#    +set g_accessFile "access_4seasonsgaming.txt" \
#    +set sv_mappoolFile "mappool_4sg.txt" \
#    +set fs_homepath ~/.quakelive/4sg-tournament-$gameport \
#    +set g_damage_lg 6 \
#    +set sv_location "$qServerLocation" \
#    +set g_voteFlags 264 \
#    +set g_allowVoteMidGame 1 \
#    +set g_allowSpecVote 0 \
#    +set teamsize 4
#else
#echo "This system is not intended to host 4sg tournament servers SYD"
#fi
#elif [ $1 -eq 17 ]; then
#if [ $(hostname) == "perth.quakelive.tomtecsolutions.com.au" ]; then
#servernum=`expr $1 - 11`
#echo "Starting starting 4sg tournament server $servernum..."
#exec $qPathToMinqlxStartScript \
#    +set net_strict 1 \
#    +set qlx_redisDatabase 1 \
#    +set net_port $gameport \
#    +set qlx_owner $qPurgeryOwnerSteam64ID \
#    +set sv_hostname "4SG CA Tournament Server #6" \
#    +set qlx_plugins "DEFAULT, branding" \
#    +set qlx_serverBrandName "^54SG CA Tournament Server^7" \
#    +set qlx_serverBrandTopField "Run by ^54Seasons Gaming^7. ^2http://4seasonsgaming.com^7. Admins: mickzerofive, zlr, phy1um, luna, grrrdian^7." \
#    +set qlx_serverBrandBottomField "Server 6 of 6." \
#    +set zmq_rcon_enable 0 \
#    +set zmq_stats_enable 1 \
#    +set zmq_stats_password "eggplant" \
#    +set zmq_stats_port $gameport \
#    +set sv_tags "$qServerLocation,4Seasons Gaming" \
#    +set bot_enable 0 \
#    +set g_accessFile "access_4seasonsgaming.txt" \
#    +set sv_mappoolFile "mappool_4sg.txt" \
#    +set fs_homepath ~/.quakelive/4sg-tournament-$gameport \
#    +set g_damage_lg 6 \
#    +set sv_location "$qServerLocation" \
#    +set g_voteFlags 264 \
#    +set g_allowVoteMidGame 1 \
#    +set g_allowSpecVote 0 \
#    +set teamsize 4
#else
#echo "This system is not intended to host 4sg tournament servers PER"
#fi
