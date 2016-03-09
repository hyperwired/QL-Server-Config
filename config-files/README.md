# Server Configuration Files

### `server.txt`
This file is really `server.cfg`, just with the .txt extension to permit GitHub readability (yes I now know that .cfg works, but I can't be bothered changing it right now.)
`server.cfg` is execed on every map load and on server startup. Global options go in this file.

### `crontab.txt`
This file contains all the cron jobs that will run on the Quake Live servers. It's imported with the `crontab` utility by the `deploy.sh` script.

### `supervisord.txt`
This file is really `supervisord.conf` just with the .txt extension to permit GitHub readability (yes I now know that .conf works, but I can't be bothered changing it right now.)
This contains the Supervisor process controller configuration, which is responsible for executing the `quakestart.sh` script with different variables to start multiple servers in different configurations.
