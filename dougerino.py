"""General-purpose functions and classes.
Copyright 2015-2017 by Doug Mahugh.
Licensed under the MIT License.
"""
import calendar
import collections
import configparser
import csv
import datetime
import functools
import gzip
import hashlib
import json
import os
import platform
import shutil
import socket
import sys
import time
from fnmatch import fnmatch
from pprint import pprint
from timeit import default_timer

import pkg_resources

# logcalls() appears first in this file, so that it can be used to decorate
# other functions below
def logcalls(options="args/return/timer"):
    """Decorator to log (to console) information about calls to a function.

    options = string containing various options, delimited by /:
              'args' (default) - show arguments passed to function
              'args=pprint' - pretty-print the passed arguments
              'args=no' or 'args=off' - don't show arguments
              'return' (default) - show value returned by function
              'return=type' - only show the return value's type/size
              'return=pprint' - pretty-print the returned value
              'return=no' or 'return=off' - don't show returned value
              'timer' (default) - show elapsed time for wrapped function
              'timer=no' or 'timer=off' - don't show elapsed time

    Note that because we're passing an optional argument to the decorator, you
    must include the parenthese - @logcalls() - even if no options are passed.
    To log all calls to function funcname:
        @logcalls()
        def funcname(...):
            ...
    """
    # parse options string into an option dictionary
    option = dict()
    for option_string in options.lower().split("/"):
        if "=" in option_string:
            key, val = option_string.split("=")
            option[key] = val
        else:
            option[option_string] = ""

    def outer_wrapper(func):
        # use functools to preserve wrapped function metadata (for debugging)
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):

            # display the wrapped function
            print((" " + func.__name__ + "(): ").center(80, "-"))

            # display passed arguments
            if option.get("args", None) == "pprint":
                print("arguments:")
                print(pprint(args))
                print(pprint(kwargs))
            elif option.get("args", None) in ["no", "off"]:
                pass  # do nothing
            else:
                print("arguments: " + str(args) + ", " + str(kwargs))

            if not option.get("timer", None) in ["no", "off"]:
                start_seconds = default_timer()

            # call the wrapped function
            return_value = func(*args, **kwargs)

            if not option.get("timer", None) in ["no", "off"]:
                elapsed_msg = " elapsed: {0:.3f} seconds ".format(
                    default_timer() - start_seconds
                )
                print(40 * " " + elapsed_msg.center(40, "-"))

            # display the returned value
            returned_size = len(str(return_value))
            if option.get("return", None) == "type":
                print(
                    "returned: "
                    + str(type(return_value))
                    + ", size = {0} bytes".format(returned_size)
                )
            elif option.get("return", None) == "pprint":
                print("returned:")
                print(str(pprint(return_value)))
            elif option.get("return", None) in ["no", "off"]:
                pass  # do nothing
            else:
                print("returned: " + str(return_value))  # default behavior

            return return_value

        return inner_wrapper

    return outer_wrapper


def bytecount(numbytes):
    """Convert byte count to display string as bytes, KB, MB or GB.

    1st parameter = # bytes (may be negative)
    Returns a short string version, such as '17 bytes' or '47.6 GB'
    """
    retval = "-" if numbytes < 0 else ""  # leading '-' for negative values
    absvalue = abs(numbytes)
    if absvalue < 1024:
        retval = retval + format(absvalue, ".0f") + " bytes"
    elif 1024 <= absvalue < 1024 * 100:
        retval = retval + format(absvalue / 1024, "0.1f") + " KB"
    elif 1024 * 100 <= absvalue < 1024 * 1024:
        retval = retval + format(absvalue / 1024, ".0f") + " KB"
    elif 1024 * 1024 <= absvalue < 1024 * 1024 * 100:
        retval = retval + format(absvalue / (1024 * 1024), "0.1f") + " MB"
    elif 1024 * 1024 * 100 <= absvalue < 1024 * 1024 * 1024:
        retval = retval + format(absvalue / (1024 * 1024), ".0f") + " MB"
    else:
        retval = retval + format(absvalue / (1024 * 1024 * 1024), ",.1f") + " GB"
    return retval


def cdow(date_or_year, month_int=1, day_int=1):
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

    thedate = datetime.date(date_or_year, month_int, day_int)
    return calendar.day_name[thedate.weekday()]


class ChangeDirectory:
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
        return "<" + (
            self.__class__.__name__ + " object, new_path = " + self.new_path + ">"
        )


def cls():
    """Cross-platform clear-screen command for console apps.
    """
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def csv_count(csvfile, column):
    """Generate a summary of unique values for a column/field.

    infile = a CSV file; must have a header row
    column = a column number or name

    Returns a dictionary whose keys are the unique values found in the
    specified field, and values are the count for each unique value.
    """
    colnames = open(csvfile, "r").readline().strip().split(",")
    if isinstance(column, int):
        colno = column
        colname = colnames[colno]
    else:
        colname = column
        colno = 0  # default if not found in CSV header
        for fieldno, fieldname in enumerate(colnames):
            if fieldname.lower() == colname.lower():
                colno = fieldno
                break

    myreader = csv.reader(open(csvfile, "r"), delimiter=",", quotechar='"')
    next(myreader, None)  # skip header
    unique_values = collections.OrderedDict()
    for values in myreader:
        key = values[colno]
        if key in unique_values:
            unique_values[key] += 1
        else:
            unique_values[key] = 1

    return unique_values


def csv2dict(filename, key_column, val_column, lower=True, header=True):
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
    for line in open(filename, "r").readlines():
        if firstline and header:
            firstline = False
            continue  # skip over the header line
        key_val = line.split(",")[key_column].strip()
        val_val = line.split(",")[val_column].strip()
        if lower:
            thedict[key_val.lower()] = val_val
        else:
            thedict[key_val] = val_val
    return thedict


def csv2json(csvdata, header=True):
    """Convert CSV data to JSON (i.e., list of dictionaries).

    csvdata = string containing a CSV file
              e.g., open('filename.csv').read()
    header = whether the data contains a header row (if not, output fields
             are named 'field0,field1,etc')

    Returns a list of dictionaries, with each dictionary corresponding to a row
    of data from the CSV data.
    """
    if not csvdata:
        return ""  # no CSV data found

    row1 = csvdata.split("\n")[0]

    if header:
        fldnames = row1.split(",")  # get field names from CSV header
    else:
        # no CSV header included, so make up field names
        fldnames = ["field" + str(fieldno) for fieldno, _ in enumerate(row1.split(","))]

    jsondata = []
    firstline = True
    for row in csvdata.split("\n"):
        if not row:
            continue  # skip blank lines
        if firstline and header:
            firstline = False
            continue
        values = row.split(",")
        rowdict = dict()
        for fieldno, fldname in enumerate(fldnames):
            rowdict[fldname] = values[fieldno]
        jsondata.append(rowdict)

    return jsondata


def csv2list(filename, column, lower=True, header=True, dedupe=True):
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
    for line in open(filename, "r").readlines():
        if firstline and header:
            firstline = False
            continue  # skip over the header line
        listval = (
            line.split(",")[column].strip().lower()
            if lower
            else line.split(",")[column].strip()
        )
        thelist.append(listval)

    if dedupe:
        return sorted(list(set(thelist)))

    return sorted(thelist)


def days_since(datestr):
    """Return # days since a date in YYYY-MM-DD format.
    """
    return (
        datetime.datetime.today() - datetime.datetime.strptime(datestr, "%Y-%m-%d")
    ).days


def dicts2csv(listobj, filename):
    """Write list of dictionaries to a CSV file.

    1st parameter = the list of dictionaries
    2nd parameter = name of CSV file to be written
    """
    csvfile = open(filename, "w", newline="")

    # note that we assume all dictionaries in the list have the same keys
    csvwriter = csv.writer(csvfile, dialect="excel")
    header_row = [key for key, _ in listobj[0].items()]
    csvwriter.writerow(header_row)

    for row in listobj:
        values = []
        for fldname in header_row:
            values.append(row[fldname])
        csvwriter.writerow(values)

    csvfile.close()


def dicts2json(source=None, filename=None):
    """Write list of dictionaries to a JSON file.

    source = the list of dictionaries
    filename = the filename (will be over-written if it already exists)
    <internal>
    """
    if not source or not filename:
        return  # nothing to do

    with open(filename, "w") as fhandle:
        fhandle.write(json.dumps(source, indent=4, sort_keys=True))


def filesize(filename):
    """Return byte size of specified file.
    """
    return os.stat(filename).st_size


def gzunzip(zippedfile, unzippedfile):
    """Decompress a .gz (GNU Zip) file.
    """
    with open(unzippedfile, "w") as fhandle:
        fhandle.write("githubuser,email\n")
        for line in gzip.open(zippedfile).readlines():
            jsondata = json.loads(line.decode("utf-8"))
            outline = jsondata["ghu"] + "," + jsondata["aadupn"]
            fhandle.write(outline + "\n")


def hashkey(string, encoding="utf-8"):
    """Return MD5 hex digest for a string value.

    Optional encoding argument defaults to UTF-8.
    """
    return hashlib.md5(string.encode(encoding)).hexdigest()


def json2csv(jsondata, header=True):
    """Convert JSON data to CSV.

    jsondata = string containing a JSON document
               e.g., open('filename.json').read()
    header = whether to output a CSV header row of field names

    Returns a string of the CSV version of the JSON data.
    """
    jsondoc = json.loads(jsondata)
    if not jsondoc:
        return ""  # no JSON data found

    fldnames = sorted([field for field in jsondoc[0]])
    csvdata = ",".join(fldnames) + "\n" if header else ""

    for row in jsondoc:
        values = [row[fldname] for fldname in fldnames]
        csvdata += ",".join(values) + "\n"

    return csvdata


def list_projection(values, columns):
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
    return ",".join(returned)


def percent(count, total):
    """Return a percent value, or 0 if undefined.
    Arguments may float, int, or str.
    """
    if not count or not total:
        return 0
    return 100 * float(count) / float(total)


def printlines(filename, numlines=1):
    """Print the first X lines of a text file (default = 1 line).
    """
    with open(filename, "r") as fhandle:
        for _ in range(0, numlines):
            print(fhandle.readline().strip())


def progressbar(progress, bar_length=50, done_char="=", todo_char="-"):
    """Display progress bar showing completion status.

    1st parameter = current progress, as a value between 0 and 1.
    bar_length = # characters in the progress bar
    done_char = the character to display for the portion completed
    todo_char = the character to display for the portion remaining
    """
    # build the display string
    done = int(bar_length * progress)
    todo = bar_length - done
    if done == 0:
        displaystr = "[" + bar_length * todo_char + "]"
    elif done == bar_length:
        displaystr = "[" + bar_length * done_char + "]"
    else:
        displaystr = "[" + (done - 1) * done_char + ">" + todo * todo_char + "]"

    # we only allow for increasing % done, so when it gets to 100% add a
    # newline ...
    if displaystr == "[" + bar_length * done_char + "]":
        displaystr += "\n"

    # update displayed progress
    if progressbar.lastdisplay != displaystr:
        print("\r" + displaystr, end="")
        progressbar.lastdisplay = displaystr


def setting(topic, section, key):
    """Retrieve a private setting stored in a local .ini file.

    topic = name of the ini file; e.g., 'azure' for azure.ini
    section = section within the .ini file
    key = name of the key within the section

    Returns the value if found, None otherwise.
    """
    source_folder = os.path.dirname(os.path.realpath(__file__))
    inifile = os.path.join(source_folder, "../_private/" + topic.lower() + ".ini")
    config = configparser.ConfigParser()
    config.read(inifile)
    try:
        retval = config.get(section, key)
    except configparser.NoSectionError:
        retval = None
    return retval


def sub_dir(searchfor, folder=None):
    """Find all occurrences of files matching a specified search pattern, in
    the specified file and its subfolders.

    searchfor = filename pattern to match (for example, '*.py')
    folder = top-level folder to be searched (default is current folder)

    Returns a list of matches."""
    if not folder:
        folder = os.getcwd()
    print(folder)
    hits = []
    for path, _, files in os.walk(folder):
        for name in files:
            if fnmatch(name, searchfor):
                hits.append(os.path.join(path, name))
    return hits


def sysinfo(newline=None):
    """Return system information.

    newline = delimiter for returned list of key/value pairs; if not
              specified, a dictionary of key/value pairs is returned

    Since this information is typically used for diagnostic printing or
    displaying of values, all vaues are returned as strings.
    """
    sys_info = dict()
    sys_info["PY_VERSION"] = sys.version.strip().split(" ")[0] + (
        " (64-bit)" if "64 bit" in sys.version else " (32-bit)"
    )
    sys_info["PY_LOCATION"] = sys.prefix
    sys_info["PY_PACKAGES"] = ",".join([_ for _ in pkg_resources.working_set])
    sys_info["PY_PATH"] = ",".join(sys.path)
    sys_info["OS_VERSION"] = platform.platform()
    sys_info["HOST_NAME"] = socket.gethostname()
    sys_info["HOST_PROC"] = (
        os.environ["PROCESSOR_ARCHITECTURE"]
        + ", "
        + os.environ["PROCESSOR_IDENTIFIER"].split(" ")[0]
        + ", "
        + os.environ["NUMBER_OF_PROCESSORS"]
        + " cores"
    )
    sys_info["HOST_IPADDR"] = socket.gethostbyname(socket.gethostname())
    sys_info["DIRECTORY"] = os.getcwd()
    size, used, free = shutil.disk_usage("/")
    sys_info["DISK_SIZE"] = "{:,}".format(size)
    sys_info["DISK_USED"] = "{:,}".format(used)
    sys_info["DISK_FREE"] = "{:,}".format(free)

    if newline:
        return newline.join([key + ": " + sys_info[key] for key in sorted(sys_info)])
    return sys_info


def time_stamp(filename=None):
    """Return timestamp as a string.

    filename = optional file, if passed then timestamp is returned for the file

    Otherwise, returns current timestamp.
    """
    if filename:
        unixtime = os.path.getmtime(filename)
        return time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(unixtime))

    return time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(time.time()))


def yeardiff(fromdate=None, todate=None):
    """Calculate difference in years.

    fromdate = starting date (e.g., date of birth); 'm/d/y' or date object
    todate = ending date; 'm/d/y' or date object

    Returns the difference as an integer number of years.
    """
    start = (
        datetime.datetime.strptime(fromdate, "%m/%d/%Y")
        if isinstance(fromdate, str)
        else fromdate
    )
    end = (
        datetime.datetime.strptime(todate, "%m/%d/%Y")
        if isinstance(todate, str)
        else todate
    )
    # note that this is based on False=0/True=1 for the < comparison ...
    return end.year - start.year - ((end.month, end.day) < (start.month, start.day))


if __name__ == "__main__":
    pass  # to do - unit tests
