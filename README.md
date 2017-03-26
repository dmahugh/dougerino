# dougerino
Library of functions for common Python development tasks.

* [bytecount](#bytecount)
* [cdow](cdow))
* [ChangeDirectory class](ChangeDirectory class)
* [cls()](cls())
* [column_values](column_values)
def csv2dict(filename, key_column, val_column, lower=True, header=True): #---<<<
def csv2list(filename, column, lower=True, header=True, dedupe=True): #------<<<
def csvfields(values, columns): #--------------------------------------------<<<
def days_since(datestr): #---------------------------------------------------<<<
def dicts2csv(listobj, filename): #------------------------------------------<<<
def dicts2json(source=None, filename=None): #--------------------------------<<<
def filesize(filename): #----------------------------------------------------<<<
def hashkey(string): #-------------------------------------------------------<<<
def percent(count, total): #-------------------------------------------------<<<
def printlines(filename, numlines=1): #--------------------------------------<<<
def progressbar(progress, bar_length=50, done_char='=', todo_char='-'): #----<<<
def setting(topic, section, key): #------------------------------------------<<<
def time_stamp(filename=None): #---------------------------------------------<<<
def yeardiff(fromdate=None, todate=None): #----------------------------------<<<


## bytecount

///

## cdow

///

## ChangeDirectory

For tools that work with files and folders, it's often useful to temporarily change the current working directory. This context managers provides a simple syntax for changing to another directory and then reverting to the prior working directory when don

```python
from dougerino import ChangeDirectory
with ChangeDirectory(folder):
    pass # code that should run in folder
# returns to previous working directory when done
```
## cls

///

## column_values

///

## csv2dict(filename, key_column, val_column, lower=True, header=True)

///

## csv2list(filename, column, lower=True, header=True, dedupe=True)

///

## csvfields(values, columns): #--------------------------------------------<<<
## days_since(datestr): #---------------------------------------------------<<<
## dicts2csv(listobj, filename): #------------------------------------------<<<
## dicts2json(source=None, filename=None): #--------------------------------<<<
## filesize(filename): #----------------------------------------------------<<<
## hashkey(string): #-------------------------------------------------------<<<
## percent(count, total): #-------------------------------------------------<<<
## printlines(filename, numlines=1): #--------------------------------------<<<
## progressbar(progress, bar_length=50, done_char='=', todo_char='-'): #----<<<
## setting(topic, section, key): #------------------------------------------<<<
## time_stamp(filename=None): #---------------------------------------------<<<
## yeardiff(fromdate=None, todate=None): #----------------------------------<<<
