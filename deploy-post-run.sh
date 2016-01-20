#! /bin/bash
# This file is part of the Quake Live server implementation by TomTec Solutions. Do not copy or redistribute or link to this file without the emailed consent of Thomas Jones (thomas@tomtecsolutions.com).
# Post-run script for 'deploy.sh'

if [ "$1" != "--no-restart" ]; then
  echo "Running 'quakeupdate.sh'..."
  bash ~/quakeupdate.sh
else
  echo "The no-restart flag has been appended. Not running QuakeUpdate.sh."
fi

exit 0
