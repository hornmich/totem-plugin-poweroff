# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Michal Horn <hornmich@fel.cvut.cz>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Power off totem plugin (https://sourceforge.net/p/poweroffplugin/).
"""

"""
---------------------------------------------------------          
|		!!!!!!CAUTION!!!!!			|
|    This version is suitable for Totem 2.x		|
|    Development of plugin for Totem 3.x is in progress	|
---------------------------------------------------------
"""

import totem
import gtk
import threading
import time
import subprocess

"""
Main class for plugin
"""
class poweroffplugin(totem.Plugin):
    def __init__(self):
        totem.Plugin.__init__(self)
	self.dialog = None		# Info dialog when action is in progress
	self.responseLock = threading.Lock()	# Mutex for shared dialog response variable
	self.dialogResponse = gtk.RESPONSE_NONE		# Default response from dialog
	self.container = None		# Side bar container
	self.radioPowerOff = None	# Radio Button - Power off
	self.radioSuspend = None	# Radio Button - Suspend
	self.radioDoNothing = None	# Radio Button - Do nothing
	self.totem_object = None	# Totem API object
    """
	Procedure called when plugin is activated i totem
    """
    def activate(self, totem_object):
        builder = self.load_interface("poweroffplugin.ui", True, totem_object.get_main_window(), self) # Loads GTK GUI form
	self.container = builder.get_object('container')
        self.radioPowerOff = builder.get_object('radioTurnOff')
	self.radioSuspend = builder.get_object('radioSuspend')
	self.radioDoNothing = builder.get_object('radioDoNothing')
	baconWidget = totem_object.get_video_widget()
	self.totem_object = totem_object
	baconWidget.connect('eos', self.eosHandler)
        self.container.show_all();
        self.totem_object.add_sidebar_page("pluginSidePage", "Power off plugin", self.container)
    """
	Procedure called when plugin is deactivated in Totem
    """
    def deactivate(selfself, totem_object):
        totem_object.remove_sidebar_page("pluginSidePage")
    """
	Timer for dialog
	delay - time delay in seconds
	command - command iniciated after delay or confirmation

	Thread waits for the time delay 'delay' and after it or when user confirm the dialog, command 'command' is performed.
 	If user reject the dialog, nothing happens
    """
    def timer(self, delay, command):
	start = time.time();
	while time.time()-start < delay :
	    self.responseLock.acquire()
	    try:
		if self.dialogResponse == gtk.RESPONSE_REJECT:
			return
		elif self.dialogResponse == gtk.RESPONSE_ACCEPT:
			pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).pid
			return
  	    finally:
		self.responseLock.release()		
	    continue
	self.dialog.destroy()
	pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).pid
    """
	Handler for EndOfStream event. 
 	Sets apropriate command, shows dialog and wait for the response for 30 seconds.
	Power of, Suspend or nothing happens then
    """
    def eosHandler(self, *args):
	if self.totem_object.get_playlist_pos() == 0 :
		if self.radioDoNothing.get_active() == True :
			text = "do nothing\n"
			command = ''
			return
		elif self.radioSuspend.get_active() == True :
			text =  "suspend\n"
			command = 'dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
		elif self.radioPowerOff.get_active() == True :
			text =  "power off\n"
			command = 'dbus-send --system --print-reply --dest="org.freedesktop.ConsoleKit" /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop'
		else :
			text =  "error\n"
			return

		label = gtk.Label("Computer is going to "+text+" in 30 seconds.")
		timerThread = threading.Thread(target=self.timer, args=(30, command))
		self.responseLock = threading.Lock()
		self.dialogResponse = gtk.RESPONSE_NONE
		timerThread.start()

		self.dialog = gtk.Dialog("End of playback", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		self.dialog.vbox.pack_start(label)
		label.show()
		response = self.dialog.run()
		self.responseLock.acquire()
		try:
			self.dialogResponse = response
		finally:
			self.responseLock.release()
		self.dialog.destroy()
