#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# autodownload.sh - quake live dedicated server workshop item download utility.
# created by Thomas Jones on 03/10/15.
# thomas@tomtecsolutions.com

workshopFile="download.list"

echo "========== AutoDownload.sh has started. =========="
echo "========= $(date) ========="

workshopIDs=`cat ~/steamcmd/steamapps/common/qlds/baseq3/workshop_* | sort -u | grep -v '#' | sed '/^[ \t]*$/d'`
numOfIDs=`echo "$workshopIDs" | wc -l`
counter=0
rm -r ~/steamcmd/steamapps/workshop
while [ $counter -lt $numOfIDs ]; do
	currentID=`echo $workshopIDs | awk '{ print $1 }'`
	workshopIDs=`echo $workshopIDs | cut -d ' ' -f2-`
	echo -e "Downloading item $currentID from Steam... ($(expr $counter + 1)/$numOfIDs)"
	~/steamcmd/steamcmd.sh +login anonymous +workshop_download_item 282440 $currentID +quit > /dev/null
	((counter++))
done
echo "Removing old workshop data and moving new items into place..."
rm -r ~/steamcmd/steamapps/common/qlds/steamapps/workshop
mv ~/steamcmd/steamapps/workshop/ ~/steamcmd/steamapps/common/qlds/steamapps/workshop
counter=1
while [ $counter -lt 6 ]; do
	echo "Running qzeroded.x64 to make sure all workshop items are downloaded... (instance $counter of 5)"
	~/steamcmd/steamapps/common/qlds/run_server_x64.sh +quit > ~/qzeroded_autoDownload.txt
	((counter++))
done
exit 0
