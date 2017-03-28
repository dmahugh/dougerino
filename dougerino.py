"""General-purpose functions and classes.

Typically we install this with "pip install --editable ." and then can make
changes/additions here and they're immediately available in other projects.
"""
import calendar
import collections
import configparser
import csv
import datetime
import hashlib
import json
import os
import time

def bytecount(numbytes): #---------------------------------------------------<<<
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

def cdow(date_or_year, month_int=1, day_int=1): #----------------------------<<<
    """Convert a date or year/month/day to a day-of-week string.

    date_or_year = a date/datetime, or year <int>

    If a year value is passed, then month_int
                   and day_int are required.
    month_int = month as <int>
    day_int = day as <int>

    Returns a weekday name (e.g., "Tuesday").
    """
    if isinstance(date_or_year, datetime.datetime):
        return calendar.day_name[date_or_year.weekday()]
    else:
        thedate = datetime.date(date_or_year, month_int, day_int)
        return calendar.day_name[thedate.weekday()]

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

def csv_count(csvfile, column): #------------------------------------<<<
    """Generate a summary of unique values for a column/field.

    infile = a CSV file; must have a header row
    column = a column number or name

    Returns a dictionary whose keys are the unique values found in the
    specified field, and values are the count for each unique value.
    """
    colnames = open(csvfile, 'r').readline().strip().split(',')
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

    myreader = csv.reader(open(csvfile, 'r'), delimiter=',', quotechar='"')
    next(myreader, None) # skip header
    unique_values = collections.OrderedDict()
    for values in myreader:
        key = values[colno]
        if key in unique_values:
            unique_values[key] += 1
        else:
            unique_values[key] = 1

    return unique_values

def csv2dict(filename, key_column, val_column, lower=True, header=True): #---<<<
    """
    Create a dictionary from two columns in a CSV file.

    filename = name of .CSV file
    key_column = column # (0-based) for dictionary keys
    val_column = column # (0-based) for dictionary values
    lower = whether to make the keys lowercase
    header = whether .CSV file has a header row as the first line

    Returns the dictionary.
    """
    thedict = dict()
    firstline = True
    for line in open(filename, 'r').readlines():
        if firstline and header:
            firstline = False
            continue # skip over the header line
        key_val = line.split(',')[key_column].strip()
        val_val = line.split(',')[val_column].strip()
        if lower:
            thedict[key_val.lower()] = val_val
        else:
            thedict[key_val] = val_val
    return thedict

def csv2json(csvdata, header=True): #----------------------------------------<<<
    """Convert CSV data to JSON (i.e., list of dictionaries).

    csvdata = string containing a CSV file
              e.g., open('filename.csv').read()
    header = whether the data contains a header row (if not, output fields
             are named 'field0,field1,etc')

    Returns a list of dictionaries, with each dictionary corresponding to a row
    of data from the CSV data.
    """
    if not csvdata:
        return '' # no CSV data found

    row1 = csvdata.split('\n')[0]

    if header:
        fldnames = row1.split(',') # get field names from CSV header
    else:
        # no CSV header included, so make up field names
        fldnames = ['field' + str(fieldno) for fieldno, _ in enumerate(row1.split(','))]

    jsondata = []
    firstline = True
    for row in csvdata.split('\n'):
        if not row:
            continue # skip blank lines
        if firstline and header:
            firstline = False
            continue
        values = row.split(',')
        rowdict = dict()
        for fieldno, fldname in enumerate(fldnames):
            rowdict[fldname] = values[fieldno]
        jsondata.append(rowdict)

    return jsondata

def csv2list(filename, column, lower=True, header=True, dedupe=True): #------<<<
    """
    Create a list from a column in a CSV file.

    filename = name of .CSV file
    column = column # (0-based) to be returned as a list
    lower = whether to make the values in the list lowercase
    header = whether .CSV file has a header row as the first line
    dedupe = whether to remove duplicate values

    Returns the list.
    """
    thelist = []
    firstline = True
    for line in open(filename, 'r').readlines():
        if firstline and header:
            firstline = False
            continue # skip over the header line
        listval = line.split(',')[column].strip().lower() if lower else \
            line.split(',')[column].strip()
        thelist.append(listval)

    if dedupe:
        return sorted(list(set(thelist)))
    else:
        return sorted(thelist)

def days_since(datestr): #---------------------------------------------------<<<
    """Return # days since a date in YYYY-MM-DD format.
    """
    return (datetime.datetime.today() -
            datetime.datetime.strptime(datestr, '%Y-%m-%d')).days

def dicts2csv(listobj, filename): #------------------------------------------<<<
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

def dicts2json(source=None, filename=None): #--------------------------------<<<
    """Write list of dictionaries to a JSON file.

    source = the list of dictionaries
    filename = the filename (will be over-written if it already exists)
    <internal>
    """
    if not source or not filename:
        return # nothing to do

    with open(filename, 'w') as fhandle:
        fhandle.write(json.dumps(source, indent=4, sort_keys=True))

def filesize(filename): #----------------------------------------------------<<<
    """Return byte size of specified file.
    """
    return os.stat(filename).st_size

def github_pagination(link_header): #----------------------------------------<<<
    """Parse values from the 'link' HTTP header returned by GitHub API.

    1st parameter = either of these options ...
                    - 'link' HTTP header passed as a string
                    - response object returned by requests library

    Returns a dictionary with entries for the URLs and page numbers parsed
    from the link string: firstURL, firstpage, prevURL, prevpage, nextURL,
    nextpage, lastURL, lastpage.
    <internal>
    """
    # initialize the dictionary
    retval = {'firstpage':0, 'firstURL':None, 'prevpage':0, 'prevURL':None,
              'nextpage':0, 'nextURL':None, 'lastpage':0, 'lastURL':None}

    if isinstance(link_header, str):
        link_string = link_header
    else:
        # link_header is a response object, get its 'link' HTTP header
        try:
            link_string = link_header.headers['Link']
        except KeyError:
            return retval # no Link HTTP header found, nothing to parse

    links = link_string.split(',')
    for link in links:
        # link format = '<url>; rel="type"'
        linktype = link.split(';')[-1].split('=')[-1].strip()[1:-1]
        url = link.split(';')[0].strip()[1:-1]
        pageno = url.split('?')[-1].split('=')[-1].strip()

        retval[linktype + 'page'] = pageno
        retval[linktype + 'URL'] = url

    return retval

def hashkey(string, encoding='utf-8'): #-------------------------------------<<<
    """Return MD5 hex digest for a string value.

    Optional encoding argument defaults to UTF-8.
    """
    return hashlib.md5(string.encode(encoding)).hexdigest()

def json2csv(jsondata, header=True): #----------------------------------------<<<
    """Convert JSON data to CSV.

    jsondata = string containing a JSON document
               e.g., open('filename.json').read()
    header = whether to output a CSV header row of field names

    Returns a string of the CSV version of the JSON data.
    """
    jsondoc = json.loads(jsondata)
    if not jsondoc:
        return '' # no JSON data found

    fldnames = sorted([field for field in jsondoc[0]])
    csvdata = ','.join(fldnames) + '\n' if header else ''

    for row in jsondoc:
        values = [row[fldname] for fldname in fldnames]
        csvdata += ','.join(values) + '\n'

    return csvdata

def list_projection(values, columns): #--------------------------------------<<<
    """Return a comma-delimited string containing specified values from a list.

    values = list of values. (E.g., as returned from a csv.reader().)
    columns = list of indices (0-based) for the columns that are to be included
              in the returned line.

    Returns a comma-delimited text string containing only the desired columns
    in the order specified in the passed list.
    """
    returned = []
    for column in columns:
        returned.append(values[column])
    return ','.join(returned)

def percent(count, total): #-------------------------------------------------<<<
    """Return a percent value, or 0 if undefined.
    Arguments may float, int, or str.
    """
    if not count or not total:
        return 0
    return 100 * float(count) / float(total)

def printlines(filename, numlines=1): #--------------------------------------<<<
    """Print the first X lines of a text file (default = 1 line).
    """
    with open(filename, 'r') as fhandle:
        for _ in range(0, numlines):
            print(fhandle.readline().strip())

def progressbar(progress, bar_length=50, done_char='=', todo_char='-'): #----<<<
    """Display progress bar showing completion status.

    1st parameter = current progress, as a value between 0 and 1.
    bar_length = # characters in the progress bar
    done_char = the character to display for the portion completed
    todo_char = the character to display for the portion remaining
    """
    # build the display string
    done = int(bar_length*progress)
    todo = bar_length - done
    if done == 0:
        displaystr = '[' + bar_length*todo_char  + ']'
    elif done == bar_length:
        displaystr = '[' + bar_length*done_char  + ']'
    else:
        displaystr = '[' + (done-1)*done_char + '>' + todo*todo_char  + ']'

    # we only allow for increasing % done, so when it gets to 100% add a
    # newline ...
    if displaystr == '[' + bar_length*done_char + ']':
        displaystr += '\n'

    # update displayed progress
    if progressbar.lastdisplay != displaystr:
        print('\r' + displaystr, end='')
        progressbar.lastdisplay = displaystr

def setting(topic, section, key): #------------------------------------------<<<
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

def time_stamp(filename=None): #---------------------------------------------<<<
    """Return timestamp as a string.

    filename = optional file, if passed then timestamp is returned for the file

    Otherwise, returns current timestamp.
    """
    if filename:
        unixtime = os.path.getmtime(filename)
        return time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(unixtime))
    else:
        return time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(time.time()))

def yeardiff(fromdate=None, todate=None): #----------------------------------<<<
    """Calculate difference in years.

    fromdate = starting date (e.g., date of birth); 'm/d/y' or date object
    todate = ending date; 'm/d/y' or date object

    Returns the difference as an integer number of years.
    """
    start = datetime.datetime.strptime(fromdate, '%m/%d/%Y') \
        if isinstance(fromdate, str) else fromdate
    end = datetime.datetime.strptime(todate, '%m/%d/%Y') \
        if isinstance(todate, str) else todate
    # note that this is based on False=0/True=1 for the < comparison ...
    return end.year - start.year - \
        ((end.month, end.day) < (start.month, start.day))

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    pass # to do - unit tests
