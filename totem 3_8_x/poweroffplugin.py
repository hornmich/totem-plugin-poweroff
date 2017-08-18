# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Michal Horn <hornmich@fel.cvut.cz>
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


---------------------------------------------------------          
|                    !!!!!!CAUTION!!!!!!                |
|    This version is suitable for Totem 3.8.x	            |
|    For Totem 2.x download apropriate version from     |
|    https://sourceforge.net/p/poweroffplugin/          |
---------------------------------------------------------
"""

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Peas
from gi.repository import Totem
import threading
import subprocess
import gettext

"""
	Constants for Radio Buttons activities
"""
SUSPEND = 0
TURNOFF = 1
NOTHING = 2

t = gettext.translation('poweroffplugin', '/usr/share/locale')
_ = t.lgettext

"""
	Class for maintaining Totem side panel for this plugin.
	------------------------------------------------------
"""
class SidePanel():
	def __init__(self):
		self._buttons = []
		self._widget = Gtk.VBox(False, 1)
		self._caption = Gtk.Label(_("After the end of playback:"))	
		self._buttons.append(Gtk.RadioButton(_("Suspend computer")))
		self._buttons.append(Gtk.RadioButton.new_with_label_from_widget(self._buttons[0], _("Turn off computer")))
		self._buttons.append(Gtk.RadioButton.new_with_label_from_widget(self._buttons[0], _("Do nothing")))
		self._widget.pack_start(self._caption, False, False, 0)
		self._widget.pack_start(self._buttons[0], False, False, 0)
		self._widget.pack_start(self._buttons[1], False, False, 0)
		self._widget.pack_start(self._buttons[2], False, False, 0)
		self._buttons[2].set_active(True)
		self._widget.show_all()

	"""
		Function returns action selected by radio button (SUSPEND, TURNOFF, NOTHING) from group
	"""	
	def getSelectedAction(self):
		i = 0
		ret=i
		for button in self._buttons:
			if button.get_active():
				ret=i
			i=i+1
		return ret
		
	"""
		Side panel GTK Widget getter
	"""
	def getWidget(self):
		return self._widget
		
"""
	Class for managing a dialog informing user about action taken after timeout.
	User has a chance to cancel or accept the action without timeout.

	Time counting runs in a separate thread using busy waiting. This should be repaired.
"""
class TimeDialog():
	def __init__(self, text, time):
		self._label = Gtk.Label(_("Computer is going to ")+text+_(" in ")+str(time)+_(" seconds."))
		self._timerThread = threading.Thread(target=self.timer, args=(time, 0))
		self._dialogLock = threading.Lock()
		self._dialogEnd = threading.Condition(self._dialogLock)
		self._dialogResponse = Gtk.ResponseType.NONE	
		self._dialog = Gtk.Dialog(_("End of playback"), None, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT, Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
	
	"""
		Show dialog, start timer and wait for timeout or user response.
		Returns Gtk.ResponseType.REJECT (cancel), Gtk.ResponseType.ACCEPT (OK) or Gtk.ResponseType.NONE (timeout)
	"""
	def run(self):
		self._timerThread.start()
		self._dialog.vbox.pack_start(self._label, expand=True, fill=True, padding=0)
		self._label.show()

		response = self._dialog.run()
		self._dialogResponse = response
		self._dialog.destroy()
		self._dialogEnd.acquire()
		self._dialogEnd.notify()
		self._dialogEnd.release()
		return self._dialogResponse		

	"""
		Procedure for timer thread.
		Busy waiting until timeout, checking response.
	"""	
	def timer(self, delay, cmd):
		dialogNotEnded = 1;
		self._dialogEnd.acquire()
		while dialogNotEnded :
			self._dialogEnd.wait(delay)
			dialogNotEnded = 0
		self._dialog.destroy()
		self._dialogEnd.release()
		return self._dialogResponse
		

"""
Main class for plugin
"""
class StarterPlugin (GObject.Object, Peas.Activatable):
	__gtype_name__ = 'poweroffplugin'
	object = GObject.property (type = GObject.Object)

	def __init__ (self):
		GObject.Object.__init__ (self)
		self._sidePanel = SidePanel()
		self._totem = None

	"""
	Procedure called when plugin is activated i totem
	"""
	def do_activate (self):
		self._totem = self.object
		self._baconWidget = self._totem.get_video_widget()
		self._baconWidget.connect('eos', self.eosHandler)
		self._totem.add_sidebar_page("poweroffSidePage", _("After playback stops"), self._sidePanel.getWidget())

	"""
	Procedure called when plugin is deactivated in Totem
	"""
	def do_deactivate (self):
		self._totem.remove_sidebar_page("poweroffSidePage")
		self._totem = None

	"""
	Handler for EndOfStream event. 
	Sets apropriate command, shows dialog and wait for the response for 30 seconds.
	Power of, Suspend or nothing happens then
	"""
	def eosHandler(self, *args):
		if self._totem.get_playlist_pos() == 0 :
			action = self._sidePanel.getSelectedAction()
			if action == SUSPEND:
				text =  _("suspend")+"\n"
				command = 'dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
			elif action == TURNOFF:
				text =  _("power off")+"\n"
				command = 'dbus-send --system --print-reply --dest="org.freedesktop.ConsoleKit" /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop'
			elif action == NOTHING:
				text = _("do nothing")+"\n"
				command = ''
				return
			else:
				text =  _("error")+"\n"
				return

			timeDialog = TimeDialog(text, 30)
			response = timeDialog.run()
			if (response == Gtk.ResponseType.NONE or response == Gtk.ResponseType.ACCEPT):

				try:
					pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).pid
				except OSError as e:
					print >>sys.stderr, "Execution failed:", e
				except CalledProcessError as e:
					print >>sys.stderr, "Command returned unexpected value:", e
				except ValueError as e:
					print >>sys.stderr, "Error in plugin - bad argument for subprocess.Popen:", e
		
			

