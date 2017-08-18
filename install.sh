#!/bin/bash
# Installation script for poweroff plugin for Totem and Xplayer media player.
# Run with sudo

if [ $# -ne 1 ] ; then
    echo $0: usage: ./install.sh totem/xplayer
    exit 1
fi

target=$1

if [[ "$target" != "totem" && "$target" != "xplayer" ]] ; then
    echo Invalit target $target. Select totem or xplayer.
    exit 1
fi

answered=false
pth=~/.local/share/$target/plugins/
while !($answered); do
    read -p "Do you wish to install this program for all users [y/n]?" yn
    case $yn in
        [Yy]* ) pth=/usr/lib/$target/plugins/poweroffplugin
				answered=true
				;;
        [Nn]* ) pth=~/.local/share/$target/plugins/poweroffplugin
				answered=true
				;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "Making directory at "$pth
mkdir -p $pth
if [ $? -ne 0 ] ; then
    echo "ERROR: Making directory "$pth" failed!"
	exit 1
fi

echo "Copying poweroffplugin.py to "$pth
cp -f poweroffplugin.py $pth
if [ $? -ne 0 ] ; then
    echo "ERROR: Copy of powerplugin.py to "$pth" failed!"
	exit 1
fi
echo "Copying poweroffplugin.plugin to "$pth
cp -f poweroffplugin.plugin $pth
if [ $? -ne 0 ] ; then
    echo "ERROR: Copy of powerplugin.plugin to "$pth" failed!"
	exit 1
fi
echo "Copying language files to /usr/share/locale"
cp -r -f languages/* /usr/share/locale
if [ $? -ne 0 ] ; then
    echo "ERROR: Copy of language files to /usr/share/locale failed!"
	exit 1
fi

echo "Installation done."

