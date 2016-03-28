# Quake Live Server Scripts

### `autodownload.sh`
This script downloads all workshop items listed in the workshop listing files via SteamCMD and moves them into place in the qlds/ directory.

### `quakestart.sh`
This script is executed by `supervisord`, it starts all the Quake Live dedicated servers with different configurations depending on the arguments parsed by supervisor during launch.

### `quakeupdate.sh`
This script puts the servers into maintenance mode and updates the QLDS via SteamCMD. It then updates `supervisord`'s configuration and restarts the Quake Live servers.

#### `rcon.py`
This script is called by `quakeupdate.sh` to put the Quake Live servers into maintenance mode.

### `searchlogs.sh`
This script finds terms supplied in the `supervisor` logs within `/tmp` and returns them in the console.
