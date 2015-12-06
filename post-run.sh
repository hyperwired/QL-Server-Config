#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Post-run script for 'deploy.sh'

echo "Running 'quakeupdate.sh'..."
bash ~/quakeupdate.sh

echo "Running the qzeroded process to download all workshop items once, then exiting the qzeroded process."
~/steamcmd/steamapps/common/qlds/run_server_x64.sh +set ttycon 0 +quit > ~/qzeroded_workshopLog.txt

exit 0
