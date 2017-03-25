"""General-purpose functions and classes.

bytecount() ------> convert byte count to display string as bytes, KB, MB or GB
cls() ------------> clear screen (cross-platform)
ChangeDirectory --> context manager class for changing working directory
"""
import os

#------------------------------------------------------------------------------
def bytecount(numbytes=0):
    """Convert byte count to display string as bytes, KB, MB or GB.

    1st parameter = # bytes (may be negative)
    Returns a short string version, such as '17 bytes' or '47.6 GB'
    """
    retval = '-' if numbytes<0 else '' # leading '-' for negative values
    absvalue = abs(numbytes)
    if absvalue<1024:
        retval = retval + format(absvalue,'.0f') + ' bytes'
    elif (1024 <= absvalue < 1024*100):
        retval = retval + format(absvalue/1024,'0.1f') + ' KB'
    elif (1024*100 <= absvalue < 1024*1024):
        retval = retval + format(absvalue/1024,'.0f') + ' KB'
    elif (1024*1024 <= absvalue < 1024*1024*100):
        retval = retval + format(absvalue/(1024*1024),'0.1f') + ' MB'
    elif (1024*1024*100 <= absvalue < 1024*1024*1024):
        retval = retval + format(absvalue/(1024*1024),'.0f') + ' MB'
    else:
        retval = retval + format(absvalue/(1024*1024*1024),',.1f') + ' GB'
    return retval

#------------------------------------------------------------------------------
def cls():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

#------------------------------------------------------------------------------
class ChangeDirectory:
    """Context manager for changing current working directory.

    with ChangeDirectory(folder):
        # code that should run in folder
        # returns to previous working directory when done
    """
    def __init__(self, newPath):
        self.newPath = newPath
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
    def __repr__(self):
        return '<' + (self.__class__.__name__ + ' object, newPath = ' +
        self.newPath + '>')

#------------------------------------------------------------------------------
if __name__ == "__main__":
    # TO DO - unit tests for dougerino module.
    pass
