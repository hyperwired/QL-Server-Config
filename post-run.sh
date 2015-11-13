#! /bin/bash
# Post-run script

# Starting supervisord again now the new inet-based config is in place.

echo "Running 'quakeupdate.sh'..."
bash ~/quakeupdate.sh

exit 0