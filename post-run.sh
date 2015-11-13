#! /bin/bash
# Post-run script

# Starting supervisord again now the new inet-based config is in place.
/usr/local/bin/supervisord
sleep 300

echo "Running 'quakeupdate.sh'..."
bash ~/quakeupdate.sh

exit 0