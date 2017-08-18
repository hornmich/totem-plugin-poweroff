                   Poweroffplugin for Totem 3.8.x

  What is it?
  -----------

  The Poweroffplugin is plugin for Totem 3.8.x player, used in Gnome Shell.
  It provides an ability to suspend or turn computer off after end of
  stream is reached.


  The Latest Version
  ------------------

  Newest stable version can be found at
  https://sourceforge.net/projects/poweroffplugin/

  Development version can be downloaded from repository
  git://git.code.sf.net/p/poweroffplugin/code poweroffplugin-code
  This version contains all newest features, but may be unstable.

  Documentation
  -------------

  The documentation of the source code can be found in poweroffplugin.py
  file in form of comments.

  Aditional information about plugin can be obtained from project wiki at
  https://sourceforge.net/p/poweroffplugin/wiki/Home/

  Installation
  ------------

  For automatic installation please run script install.sh as root. If it
  will not work for some reason, use manual installation.

    Manual installation
    -------------------
    There are two possible paths, where to install plugins for Totem.
    1) ~/.local/share/totem/plugins/ -- for one user
    2) /usr/lib/totem/plugins/ -- for all users

	Make directory poweroffplugin in one of the paths, for example
	mkdir -p ~/.local/share/totem/plugins/poweroffplugin

	Copy poweroffplugin.py and poweroffplugin.plugin into the directory,
    for example
    cp poweroffplugin.py ~/.local/share/totem/plugins/poweroffplugin
    cp poweroffplugin.plugin ~/.local/share/totem/plugins/poweroffplugin

    Copy language files as root into /usr/share/locale
	cp -r -f languages/* /usr/share/locale

	Run Totem and enjoy

  Running plugin
  --------------
  When you run Totem player, activate the plugin and view side panel.  

  Licensing
  ---------

  Copyright (c) 2013 Michal Horn <hornmich@fel.cvut.cz>

  Permission is hereby granted, free of charge, to any person obtaining a
  copy of this software and associated documentation files (the "Software"),
  to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense,
  and/or sell copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.
 
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  DEALINGS IN THE SOFTWARE.

