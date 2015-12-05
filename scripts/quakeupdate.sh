#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# quakestart.sh - quake live multiple server update script, utilising steamcmd.
# created by Thomas Jones on 09/09/15.
# purger@tomtecsolutions.com

# This script will be replaced in the near future. Consider this an active legacy script.

# Defining variables:
export qUpdateServerMessage="^7All ^4TomTec Solutions^7 hosted servers are going down ^1within a minute^7 for daily updating. They will be back in ^410 minutes^7."
export qUpdateLowestRconPort=28960
export qUpdateHighestRconPort=28970
export qRconPassword=$(cat ~/localConfig-rconPassword-purgery.txt)

echo "========== QuakeUpdate.sh has started. =========="
echo "========= $(date) ========="
# Informing players in the servers that the servers are going down for a bit.
counter="$qUpdateLowestRconPort"

while [ $counter -le $qUpdateHighestRconPort ]
do
	echo Telling players in server port $counter that the servers are going down...
	python2 ~/steamcmd/steamapps/common/qlds/rcon.py --host tcp://127.0.0.1:$counter --password "$qRconPassword" --command "say $qUpdateServerMessage"
	((counter++))
done

# Using 'supervisorctl' to stop all servers.
echo Stopping Quake Servers...
/usr/local/bin/supervisorctl stop all

# Running 'steamcmd' to update qzeroded
echo Updating Quake Server...
~/steamcmd/steamcmd.sh +login anonymous +force_install_dir ~/steamcmd/steamapps/common/qlds/ +app_update 349090 +quit

# Removing the .quakelive directories, except for baseq3.
echo "Removing Purgery 'baseq3' directories..."
cd ~/.quakelive
rm -rf 27960/baseq3 27961/baseq3 27962/baseq3 27963/baseq3 27964/baseq3 27965/baseq3 27966/baseq3 27967/baseq3 27968/baseq3 27969/baseq3 27970/baseq3
cd ~

# Running 'autodownload.sh' to recache all workshop items before restarting.
#bash ~/autodownload.sh # going to see how well it does on it's own. # didn't do well, welcome back autodownload.sh... # off it goes again

# Using 'supervisorctl' to start all servers.
echo Starting Quake Servers...
/usr/local/bin/supervisorctl start all

# Pretty obvious what's happening now.
echo Exiting...
exit 0
