import os
import totem
import gconf
import gobject
import gtk
import pango
import socket
import threading
import time
import urllib
import urllib2
import subprocess
from xml.sax.saxutils import escape

class poweroffplugin(totem.Plugin):
    def __init__(self):
        totem.Plugin.__init__(self)
	self.responseLock = threading.Lock()
	self.dialogResponse = gtk.RESPONSE_NONE
	self.dialog = 0
    def activate(self, totem_object):
        self.builder = self.load_interface("poweroffplugin.ui", True, totem_object.get_main_window(), self)
	self.container = self.builder.get_object('container')
        self.configDialog = self.builder.get_object('config_dialog')
        self.radioUseDBus = self.builder.get_object('radioUseDBus')
        self.radioOwnComm = self.builder.get_object('radioOwnComm')
        self.radioPowerOff = self.builder.get_object('radioTurnOff')
	self.radioSuspend = self.builder.get_object('radioSuspend')
	self.radioDoNothing = self.builder.get_object('radioDoNothing')
	self.entryShutDown = self.builder.get_object('entryShutDown')
        self.entrySuspend = self.builder.get_object('entrySuspend')
	self.goButton = self.builder.get_object('go_button')
	self.goButton.connect('clicked', self.goButtonClicked)
        
        self.totem = totem_object
        self.container.show_all();
        self.totem.add_sidebar_page("pluginSidePage", "Power off plugin", self.container)
    def deactivate(selfself, totem_object):
        totem_object.remove_sidebar_page("pluginSidePage")
    def create_configure_dialog(self, *args):
        self.configDialog.set_default_response(gtk.RESPONSE_OK)
        return self.configDialog
    def turnOff(self):
	pid = subprocess.Popen('dbus-send --system --print-reply --dest="org.freedesktop.ConsoleKit" /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).pid
    def suspend(self):
	pid = subprocess.Popen('dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).pid

    def timer(self, delay, command):
	start = time.time();

	while time.time()-start < delay :
	    self.responseLock.acquire()
	    print "timer: zamknul"
	    try:
		if self.dialogResponse == gtk.RESPONSE_REJECT:
			print "cancel, return"
			return
		elif self.dialogResponse == gtk.RESPONSE_ACCEPT:
			print "OK - print - return"
			print command
			return
  	    finally:
		print "timer: odemyka"
		self.responseLock.release()		
	    continue
	print command
	self.dialog.destroy()


    def goButtonClicked(self, *args):
	if self.radioDoNothing.get_active() == True :
		text = "Doing nothing\n"
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
	timerThread = threading.Thread(target=self.timer, args=(5, command))
	self.responseLock = threading.Lock()
	self.dialogResponse = gtk.RESPONSE_NONE
	timerThread.start()

	self.dialog = gtk.Dialog("Performing action"+text, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	self.dialog.vbox.pack_start(label)
	label.show()
	response = self.dialog.run()
	self.responseLock.acquire()
	try:
		self.dialogResponse = response
	finally:
		self.responseLock.release()
	self.dialog.destroy()
    
        
