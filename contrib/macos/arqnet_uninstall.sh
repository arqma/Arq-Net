#!/bin/sh
launchctl stop com.arqma.arqnet.daemon
launchctl unload /Library/LaunchDaemons/com.arqma.arqnet.daemon.plist

killall arqnet

rm -rf /Library/LaunchDaemons/com.arqma.arqnet.daemon.plist
rm -rf /Applications/ArqnetGUI.app
rm -rf /var/lib/arqnet
rm -rf /usr/local/arqnet/
rm -rf /opt/arqnet

