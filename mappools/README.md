# Server Map-Cycle Files

These files list the maps to be played on certain servers, and provide the array of maps that appear at the end-of-game map voting screen, along with the game type the map can be played with.

For example, if a map-pool file contains the following:
```
campgrounds|ffa
almostlost|ca
```
Then the map Campgrounds will appear at the end-of-game voting screen, and if voted, will switch the game type to Free-For-All, or if map Almost Lost is voted, will switch the game type to Clan Arena.

Comments are supported in map-pool files, though must be pre-pended with `#`, and must be on their own line.
