"""General-purpose functions and classes.

Typically we install this with "pip install --editable ." and then can make
changes/additions here and they're immediately available in other projects.
"""
import configparser
import csv
import datetime
import hashlib
import json
import os
import time

def bytecount(numbytes=0): #-------------------------------------------------<<<
    """Convert byte count to display string as bytes, KB, MB or GB.

    1st parameter = # bytes (may be negative)
    Returns a short string version, such as '17 bytes' or '47.6 GB'
    """
    retval = '-' if numbytes < 0 else '' # leading '-' for negative values
    absvalue = abs(numbytes)
    if absvalue < 1024:
        retval = retval + format(absvalue, '.0f') + ' bytes'
    elif 1024 <= absvalue < 1024*100:
        retval = retval + format(absvalue/1024, '0.1f') + ' KB'
    elif 1024*100 <= absvalue < 1024*1024:
        retval = retval + format(absvalue/1024, '.0f') + ' KB'
    elif 1024*1024 <= absvalue < 1024*1024*100:
        retval = retval + format(absvalue/(1024*1024), '0.1f') + ' MB'
    elif 1024*1024*100 <= absvalue < 1024*1024*1024:
        retval = retval + format(absvalue/(1024*1024), '.0f') + ' MB'
    else:
        retval = retval + format(absvalue/(1024*1024*1024), ',.1f') + ' GB'
    return retval

class ChangeDirectory: #-----------------------------------------------------<<<
    """Context manager for changing current working directory.

    with ChangeDirectory(folder):
        # code that should run in folder
        # returns to previous working directory when done
    """
    def __init__(self, new_path):
        self.new_path = new_path
        self.saved_path = None
    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)
    def __repr__(self):
        return '<' + (self.__class__.__name__ + ' object, new_path = ' +
                      self.new_path + '>')

def cls(): #-----------------------------------------------------------------<<<
    """Cross-platform clear-screen command for console apps.
    """
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def column_values(infile, column, outfile): #--------------------------------<<<
    """Generate a summary of unique values for a column/field.

    infile = a CSV file; must have a header row
    column = a column number or name
    outfile = output file to be written

    the output file contains each unique value found in the specified column,
    sorted alphabetically. Each line contains the value twice, separated by
    a comma. The second value is typically manually edited to create a shorter
    version for reports, and the lines may be re-arranged to specify the order
    these values should appear in reports. See race_abbrev() and race_sort() for
    examples of how this data can be used.
    """
    colnames = open(infile, 'r').readline().strip().split(',')
    if isinstance(column, int):
        colno = column
        colname = colnames[colno]
    else:
        colname = column
        colno = 0 # default if not found in CSV header
        for fieldno, fieldname in enumerate(colnames):
            if fieldname.lower() == colname.lower():
                colno = fieldno
                break

    myreader = csv.reader(open(infile, 'r'), delimiter=',', quotechar='"')
    next(myreader, None) # skip header
    value_list = set()
    for values in myreader:
        value_list.add(values[colno])

    for value in sorted(value_list):
        print(value + ',' + value)

def csvfields(values, columns): #--------------------------------------------<<<
    """Return specified set of fields/columns from a line of a CSV file.

    values = list of values, as returned from a csv.reader().
    columns = list of indices (0-based) for the columns that are to be included
              in the returned line.

    Returns a comma-delimited text string containing only the desired columns
    in the order specified in the passed list.
    """
    returned = []
    for column in columns:
        returned.append(values[column])
    return ','.join(returned)

def days_since(datestr): #---------------------------------------------------<<<
    """Return # days since a date in YYYY-MM-DD format.
    """
    return (datetime.datetime.today() -
            datetime.datetime.strptime(datestr, '%Y-%m-%d')).days

def filesize(filename): #----------------------------------------------------<<<
    """Return byte size of specified file.
    """
    return os.stat(filename).st_size

def hashkey(string): #-------------------------------------------------------<<<
    """Return MD5 hex digest for the UTF-8 encoding of a string value.
    """
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def setting(topic=None, section=None, key=None): #---------------------------<<<
    """Retrieve a private setting stored in a local .ini file.

    topic = name of the ini file; e.g., 'azure' for azure.ini
    section = section within the .ini file
    key = name of the key within the section

    Returns the value if found, None otherwise.
    """
    source_folder = os.path.dirname(os.path.realpath(__file__))
    inifile = os.path.join(source_folder, '../_private/' + topic.lower() + '.ini')
    config = configparser.ConfigParser()
    config.read(inifile)
    try:
        retval = config.get(section, key)
    except configparser.NoSectionError:
        retval = None
    return retval

def timestamp(filename=None): #----------------------------------------------<<<
    """Return timestamp as a string.

    filename = optional file, if passed then timestamp is returned for the file

    Otherwise, returns current timestamp.
    """
    if filename:
        unixtime = os.path.getmtime(filename)
        return time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(unixtime))
    else:
        return time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(time.time()))

def write_csv(listobj, filename): #------------------------------------------<<<
    """Write list of dictionaries to a CSV file.

    1st parameter = the list of dictionaries
    2nd parameter = name of CSV file to be written
    """
    csvfile = open(filename, 'w', newline='')

    # note that we assume all dictionaries in the list have the same keys
    csvwriter = csv.writer(csvfile, dialect='excel')
    header_row = [key for key, _ in listobj[0].items()]
    csvwriter.writerow(header_row)

    for row in listobj:
        values = []
        for fldname in header_row:
            values.append(row[fldname])
        csvwriter.writerow(values)

    csvfile.close()

def write_json(source=None, filename=None): #--------------------------------<<<
    """Write list of dictionaries to a JSON file.

    source = the list of dictionaries
    filename = the filename (will be over-written if it already exists)
    <internal>
    """
    if not source or not filename:
        return # nothing to do

    with open(filename, 'w') as fhandle:
        fhandle.write(json.dumps(source, indent=4, sort_keys=True))

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # to do - unit tests
    pass
