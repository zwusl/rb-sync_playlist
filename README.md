Sync Playlists
==============
A Rhythmbox plugin to synchronize the selected playlist to a folder

What can that be good for?

You can use this plugin to transfer music from the linux desktop to your (Android) phone.
Since the mtp connection is not reliable, at least not for my devices, this plugin
can be used to transfer the tracks of a playlist to a folder.

The directory structure is preserved, that means that if two tracks have the same filename (e.g. track01.mp3),
they do not overwrite each other, as it would be if the tracks are copied to one single flat directory.

The playlst itself is tranfered to an other folder.
The entries are prepared in a format, so that they can be used on an other device.

Then one can transfer the tracks and the playlist by reliable means to an other device.
For me syncthing does the job.

Installation
------------
- Pull the project and run the install.sh . If you are on RB 2.XX check the "install.sh -h"
- Then restart Rhythmbox

Usage
--------------------
Define two directories in the settings of the plugin, one for the tracks, one for the playlist.
Select a playlist, under the menue "playlist" you will find the entry "sync playlist".
sync the playlist, and then use e.g. syncthing to transfer the tracks and and the playlist to the mobile device.
On the mobile device import the playlist, it should be readable without further editing.
E.g. foobar2000 can deal with the so provided playlists.


Change log
--------------------
- 0.0.1 2021-02-06 Initial release
- 0.0.5 2021-02-11 First testversion
