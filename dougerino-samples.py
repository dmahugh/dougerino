"""Example usage of a few things from dougerino.py
"""
import os
import time

from dougerino import bytecount, ChangeDirectory, progressbar

#-----------------------------------------------------------------------------
# bytecount() - convert byte count to display string as bytes, KB, MB or GB
#-----------------------------------------------------------------------------
# This function provides a simple way to display byte counts that may vary
# over a wide range of values. It doesn't provide complete precision (most
# values are rounded), instead the goal is a simple short human-readable
# display that uses common byte-oriented suffixes such as KB/MB/GB.
print('\n' + '>>  bytecount() function  <<'.center(75, '-') + '\n')
print('bytecount(123)         = ' + bytecount(123))
print('bytecount(5280)        = ' + bytecount(5280))
print('bytecount(12345678)    = ' + bytecount(12345678))
print('bytecount(12345678901) = ' + bytecount(12345678901))

#-----------------------------------------------------------------------------
# ChangeDirectory - context manager class for changing working directory
#-----------------------------------------------------------------------------
print('\n' + '>>  ChangeDirectory class  <<'.center(75, '-') + '\n')
print('default directory -> ' + os.getcwd() + '\n')
print("with ChangeDirectory(r'C:\Windows'):")
with ChangeDirectory(r'C:\Windows'): # this is all it takes
    # this code block runs in the specified folder
    print('    default directory -> ' + os.getcwd())
# now we're back to the previous working directory
print('\ndefault directory -> ' + os.getcwd())

#-----------------------------------------------------------------------------
# progressbar - display progress bar showing completion status
#-----------------------------------------------------------------------------
print('Example of using progressbar() function ...')
progressbar.lastdisplay = ''
for progress_value in range(100):
    progressbar(progress_value/100, bar_length=80, done_char='#')
    time.sleep(.02)
progressbar(1, bar_length=80, done_char='#') # when value is 1, printed string ends with \n
