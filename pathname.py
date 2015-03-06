"""
	Name: pathname.py
	
	Usage: pathname.py <root_path>
	
	Author: Bar Harel
	
	Purpose:
		Change the file names containing a character in REPLACE_FROM to REPLACE_TO

	Changelog:
		28/01/2015 - Creation.
"""

import os, os.path, sys, threading, win32ui, win32con

REPLACE_FROM	= [" ", "."]
REPLACE_TO		= "_"
USAGE_MSG		= "Usage: pathname.py <root_path>"
PATH_MSG		= "Error: path does not exist."
FILE_EXCEPT_MSG	= "WARNING: %d files weren't converted. (Perhaps they're name is in a different language?)"
DIR_EXCEPT_MSG	= "WARNING: %d directories weren't converted. (Perhaps they're name is in a different language?)"
WARNING_MSG		= "This software should not be used on software directories.\nUsing this software may render them useless.\nProceed?"

def main():
	if len(sys.argv) != 2:
		print USAGE_MSG
		return 1

	# Check if input path exists
	if not os.path.exists(sys.argv[1]):
		print USAGE_MSG
		return 1
	
	if win32ui.MessageBox(WARNING_MSG, "Warning", win32con.MB_YESNO|win32con.MB_ICONWARNING|win32con.MB_DEFBUTTON2) != win32con.IDYES:
		return 2
	print
	# Program start
	file_except_count = 0
	dir_except_count = 0
	
	for curr_dir, dirnames, filenames in os.walk(sys.argv[1], topdown=False):
		for fname in filenames:
			split_fname = os.path.splitext(fname)
			new_name = reduce(lambda temp_name, curr_replace: temp_name.replace(curr_replace, REPLACE_TO), REPLACE_FROM, split_fname[0])
			try:
				os.rename(os.path.join(curr_dir, fname), os.path.join(curr_dir, new_name + split_fname[1]))
			except WindowsError, error:
				print fname, "- problem converting"
				file_except_count += 1
		for dname in dirnames:
			try:
				os.rename(os.path.join(curr_dir, dname), os.path.join(curr_dir, reduce(lambda temp_name, curr_replace: temp_name.replace(curr_replace, REPLACE_TO), REPLACE_FROM, dname)))
			except WindowsError, error:
				print dname, "- problem converting"
				dir_except_count += 1
	if file_except_count != 0 or dir_except_count != 0: print
	if file_except_count != 0: print FILE_EXCEPT_MSG % (file_except_count)
	if dir_except_count != 0: print DIR_EXCEPT_MSG % (dir_except_count)
	print "\nDone replacing all names in \"%s\"." % (sys.argv[1])
	return 1

if __name__ == "__main__":
	main()