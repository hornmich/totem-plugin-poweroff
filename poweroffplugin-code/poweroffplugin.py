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
    def goButtonClicked(self, *args):
	if self.radioDoNothing.get_active() == True :
		print "Doing nothing\n"
	elif self.radioSuspend.get_active() == True :
		print "Suspending\n"
	elif self.radioPowerOff.get_active() == True :
		print "Power off\n"
	else :
		print "error\n"
	

        
