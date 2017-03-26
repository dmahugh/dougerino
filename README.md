# dougerino
Library of functions for common Python development tasks.

* [bytecount](#bytecount)
* [cdow](#cdow)
* [ChangeDirectory](#ChangeDirectory)
* [cls](#cls)
* [csv_count](#csv_count)
* [csv2dict](#csv2dict)
* [csv2json](#csv2json)
* [csv2list](#csv2list)
* [days_since](#days_since)
* [dicts2csv](#dicts2csv)
* [dicts2json](#dicts2json)
* [filesize](#filesize)
* [hashkey](#hashkey)
* [json2csv](#json2csv)
* [list_projection](#list_projection)
* [percent](#percent)
* [printlines](#printlines)
* [progressbar](#progressbar)
* [setting](#setting)
* [time_stamp](#time_stamp)
* [yeardiff](#yeardiff)

## bytecount

Function for concise display of approximate numeric values. Examples:

```
bytecount(123) -----------> 123 bytes
bytecount(5280) ----------> 5.2 KB
bytecount(12345678) ------> 11.8 MB
bytecount(12345678901) ---> 11.5 GB
```

## cdow

Returns a weekday name, arguments can be a date, datetime, or year/month/day.

![cdow() examples](images/example-cdow.png)

## ChangeDirectory

This class is a context manager for changing to another directory and then reverting to the prior working directory when done.
```python
from dougerino import ChangeDirectory
with ChangeDirectory(folder):
    pass # code that should run in folder
# returns to previous working directory when done
```
## cls

Cross-platform clear-screen function for console apps.

## csv_count

Function arguments: csvfile, column

Counts the occurences of each distinct value in a specified column of a CSV file.
Returns a dictionary whose keys are the distinct values, and the value of each
dictionary entry is the count for that distinct value.

## csv2dict

Function arguments: filename, key_column, val_column, lower, header

Returns a dictionary with one entry for each row in a specified CSV file,
using the specified columns for the dictionary's key/value pairs.
Optional arguments for whether to make all keys lower-case (default=True)
and whether the CSV file has a header row (default=True).

## csv2json

Arguments: csvdata, header

Returns a JSON object (list of dictionaries) that contains all of the data from
the contents of a CSV file (passed as a string). Optional parameter to indicate
whether the CSV data includes a header row (default=True). If no header row,
the dictionaries have keys named field0, field1, etc.

## csv2list

Arguments: filename, column, lower, header, dedupe

Returns a specified column number (0-based) of a CSV file as a list. Optional
parameters for whether to return values as lower-case (default=True), whether
the CSV file has a header (default=True), and whether to eliminate duplicate
entries in the list (default=True).

## days_since

Return number of days that have passed since a specified date. Date is passed
as a string, YYYY-MM-DD format.

## dicts2csv

Write a specified list of dictionaries (as returned by json.loads()) to a specified
CSV file.

## dicts2json

Write a specified list of dictionaries (as returned by json.loads()) to a specified
JSON file.

## filesize

Returns byte size for a specified filename. (Wrapper around os.stat().st_size.)

## hashkey

![hashkey() example](images/example-hashkey.png)

## json2csv

Arguments: jsondata, header (default=True)

Converts a JSON document (string) to a CSV representation (string).

Note that this function takes a *string* version of the JSON data, because
it is commonly used with data read from a file. E.g., ```open('filename.json').read()```.

## list_projection

Returns a comma-delimited string containing specified values from a list.

![list_project() example](images/example-list_projection.png)

## percent
    
///

## printlines

///

## progressbar

///

```python
print('Example of using progressbar() function ...')
progressbar.lastdisplay = ''
for progress_value in range(100):
    progressbar(progress_value/100, bar_length=80, done_char='#')
    time.sleep(.02)
progressbar(1, bar_length=80, done_char='#') # 1 = 100% finished
```

## setting

///

## time_stamp

///

## yeardiff

///
