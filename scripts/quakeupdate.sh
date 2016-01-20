#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# quakeupdate.sh - quake live multiple server update script, utilising steamcmd and rcon.
# created by Thomas Jones on 09/09/15.
# thomas@tomtecsolutions.com


# Defining variables:
export qUpdateLowestRconPort=28960
export qUpdateHighestRconPort=28967
export qRconPassword=$(cat ~/localConfig-rconPassword-purgery.txt)

echo "========== QuakeUpdate.sh has started. =========="
echo "========= $(date) ========="
# Informing players in the servers that the servers are going down for a bit.
counter="$qUpdateLowestRconPort"

while [ $counter -le $qUpdateHighestRconPort ]
do
	echo Telling players in server port $counter that the servers are going down...
	python2 ~/steamcmd/steamapps/common/qlds/rcon.py --host tcp://127.0.0.1:$counter --password "$qRconPassword" --command "qlx !load maintenance"
	((counter++))
done

# Using 'supervisorctl' to stop all servers. - No need to stop the servers now as they should be in maintenance mode.
#echo Stopping Quake Servers...
#/usr/local/bin/supervisorctl stop all

# Running 'steamcmd' to update qzeroded
echo Updating Quake Server...
~/steamcmd/steamcmd.sh +login anonymous +force_install_dir ~/steamcmd/steamapps/common/qlds/ +app_update 349090 +quit

# Removing the .quakelive directories, except for baseq3.
echo "Removing Purgery 'baseq3' directories..."
cd ~/.quakelive
rm -rf 27960/baseq3 27961/baseq3 27962/baseq3 27963/baseq3 27964/baseq3 27965/baseq3 27966/baseq3 27967/baseq3 #27968/baseq3 27969/baseq3 27970/baseq3 - These servers aren't Purgery anymore.
cd ~

# Running 'autodownload.sh' to recache all workshop items before restarting.
#bash ~/autodownload.sh # going to see how well it does on it's own. # didn't do well, welcome back autodownload.sh... # off it goes again

echo "Running the qzeroded process to download all workshop items once, then exiting the qzeroded process."
~/steamcmd/steamapps/common/qlds/run_server_x64.sh +quit > ~/qzeroded_workshopLog.txt

echo "Reloading the 'supervisord' process..."
/usr/local/bin/supervisorctl reload

echo "Sleeping for 10 seconds to allow Supervisor to fully spawn..."
sleep 10

# Using 'supervisorctl' to start all servers.
echo Starting Quake Servers...
/usr/local/bin/supervisorctl start all

# Pretty obvious what's happening now.
echo Exiting...
exit 0
