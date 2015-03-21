"""
    Name: pathname.py
    
    Usage: pathname.py <root_path>
    
    Author: Bar Harel
    
    Purpose:
        Change the file names containing a character in REPLACE_FROM to REPLACE_TO

    Changelog:
        21/03/2015 - Conversion to python 3, change to a module
        28/01/2015 - Creation.
"""

import os
import os.path

from functools import reduce

REPLACE_FROM    = [" ", "."]
REPLACE_TO        = "_"
USAGE_MSG        = "Usage: pathname.py <root_path>"
PATH_MSG        = "Error: path does not exist."
FILE_EXCEPT_MSG    = "WARNING: %d files weren't converted. (Perhaps they're name is in a different language?)"
DIR_EXCEPT_MSG    = "WARNING: %d directories weren't converted. (Perhaps they're name is in a different language?)"
WARNING_MSG        = "This software should not be used on software directories.\nUsing this script may render them useless.\nProceed?"

def convert_names(root_directory, replace_from_list, replace_to, warning = False):
    """
        Replace all occurences of characters from the replace_from_list to replace_to in all files and folders under the given root directory.

        Return value: (files_not_converted, directories_not_converted)
        
        Remarks:
            - Warning = True means it will print a warning for each file not convered to the stdout
            - The function returns a tuple of 2 lists that contain paths to the files and directories that weren't converted.
            - Keep in mind that using this function on software directories can render the software useless.
    """
    # Initialize variables
    files_not_converted = []
    directories_not_converted = []

    # For each file and directory under the root directory
    for curr_dir, dirnames, filenames in os.walk(root_directory, topdown=False):
        # For each file
        for fname in filenames:
            # split the extension
            split_fname = os.path.splitext(fname)
            # Rename
            new_name = reduce(lambda temp_name, curr_replace: temp_name.replace(curr_replace, REPLACE_TO), REPLACE_FROM, split_fname[0])
            # Apply
            try:
                os.rename(os.path.join(curr_dir, fname), os.path.join(curr_dir, new_name + split_fname[1]))
            except WindowsError, error:
                if warning:
                    print (fname, "- problem converting")
                files_not_converted.append(os.path.join(curr_dir, fname))
        for dname in dirnames:
            try:
                # Rename & Apply
                os.rename(os.path.join(curr_dir, dname), os.path.join(curr_dir, reduce(lambda temp_name, curr_replace: temp_name.replace(curr_replace, REPLACE_TO), REPLACE_FROM, dname)))
            except WindowsError, error:
                if warning:
                    print (dname, "- problem converting")
                directories_not_converted.append(os.path.join(curr_dir, dname))

    return (files_not_converted, directories_not_converted)

def main():
    if len(sys.argv) != 2:
        print USAGE_MSG
        return 1

    # Check if input path exists
    if not os.path.exists(sys.argv[1]):
        print(USAGE_MSG)
        return 1
    
    if win32ui.MessageBox(WARNING_MSG, "Warning", win32con.MB_YESNO|win32con.MB_ICONWARNING|win32con.MB_DEFBUTTON2) != win32con.IDYES:
        return 2

    files_not_converted, directories_not_converted = convert_names(sys.argv[1], REPLACE_FROM, REPLACE_TO)
    if files_not_converted != [] or directories_not_converted != []: print ("\n")
    if files_not_converted != []: print (FILE_EXCEPT_MSG % (len(files_not_converted)))
    if directories_not_converted != []: print (DIR_EXCEPT_MSG % (len(directories_not_converted)))
    print ("\nDone replacing all names in \"%s\"." % (sys.argv[1]))
    return 1

if __name__ == "__main__":
    import sys
    import win32ui
    import win32con
    main()