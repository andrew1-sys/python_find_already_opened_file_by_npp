# Python script which allow find already are opened files in the instances by Notepad++(NPP).

Before using install packages:
	pip install pygetwindow pyautogui

Npp works in two mode:
1. 	Session (mono-instance), when one instance contains in the tabs many are opened files.
2. 	New instance, open file in separate window.

This script can be run in two modes:
1. 	Looking in all instances for already opened file.
		   If found then will make active.
		   If not found create new instance of NPP and open file there

		   Example:
		   python c:\temp\s.py 0 c:\temp\find_me.txt

		   You can replace original "Total Commander" editor (key F4) for using NPP instead.
		   In menu: <Configuration>/<Options><Edit/View> Editor for F4: python c:\temp\s.py 0

2. 	Looking in all instances and in every instance enumerate all tabs for already opened file.
		   If found then will make active.
		   If not found create new instance of NPP and open file there.

		   Example:
		   python c:\temp\s.py 0 c:\temp\find_me.txt

		   You can use it for searching files are opened in mono-instance mode of NPP.
		   You can create shortcut for opening most used files, using additionaly application AutoHotKey:
		   Example script for combination: CTRL+ALT+V

			^!v::
				; Path to the shortcut file (.lnk)
				ShortcutPath := "python c:\temp\s.py 1 c:\temp\somefile.txt"

				; Run the shortcut
				Run, %ShortcutPath%
			return