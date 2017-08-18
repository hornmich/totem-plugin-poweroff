# Power off plugin for Totem and Xplayer
This is plugin for Totem and Xplayer multimadia players, available for Gnome Shell and Cinnamon environment.
The plugin adds to the player the possibility of suspending or turning off the computer at the end of playback.

## Compatibility
The plugin has been tested on Ubuntu and Linux Mint distribution on the following versions of players:
* Totem 2.3
* Totem 3.0
* Totem 3.8 on Linux Mint 17
* Xplayer 1.4.3 on Linux Mint 18.2

The plugin might be compatible with other versions, but Totem and all its components are under heavy development and the plugin API is changing all the time, so the compatibility is not guaranteed for all combinations of libraries and players.

If the plugin does not work for you, please send me the output from the command line and version of your player to allow me improve the plugin.

## Installation
There are two ways for installation:
### Script
There is an 'install' script at the root of the repository, that can be used for automatic intallation of the plugin to yout system.

Change to the directory where you have extracted the plugin and run the instllation script

    sudo ./install.sh totem
    
or
 
    sudo ./install.sh xplayer
    
The script is properly installed if the script does not report any error.

Enable the plugin in the player and enjoy.

### Manual installation
If the script did not do the trick, you may install the plugin manualy. First, you have to find out where in your system does Totem or Xplayer look for plugins. Normaly the plugins have to be located at following paths:

For local user

    ~/.local/share/xplayer/plugins
    
    ~/.local/share/totem/plugins

For all users

    /usr/lib/xplayer/plugins/    

    /usr/lib/totem/plugins/  

Once you identify the correct path, change to it and create a directory for the plugin

    mkdir poweroffplugin
    
Change to the directory where you have extracted the plugin and copy the plugin files to the directory

    cp -f poweroffplugin.plugin $pth
    cp -f poweroffplugin.plugin $pth
    
Finally copy the language file to your system locals

    cp -r -f languages/* /usr/share/locale
  
