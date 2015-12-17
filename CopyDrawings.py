import glob
import os
import shutil
import sys

source = str(raw_input("Enter the source directory path:"))
if not os.path.exists(source):
    print "Source directory does not exist"
    sys.exit()
else:
    source = source+"\*.dwg"

destination = str(raw_input("Enter the destination path:"))
if not os.path.exists(destination):
    os.makedirs(destination)
else:
    while True:
        keep_going = str(raw_input("Directory exists.  Do you still want to copy into the directory? (y/n):")).lower()
        if keep_going == "n":
            sys.exit()
        elif keep_going == "y":
            break
        else:
            print "(y/n):"
while True:
    filetype = int(raw_input("Enter drawing type (1,2,3,etc.): "))
    if filetype < 0 or filetype >10:
        filetype = str(raw_input("Enter drawing type: "))
    else:
        break
startmark = "\*.dwg"

startindex = source.find(startmark)

## Grab every dwg file in the directory and store it in fileSRClist
fileSRClist = glob.glob(source)

## Define variables
filetype_loc = startindex + 7
fname, rev, temprev, filenumber, latest_rev_list, count = [], [], "A", 0, [], 0
temp = fileSRClist[0]
tempname = temp[:len(fileSRClist[0])-5]
tempfile = fileSRClist[0]
order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" #Custom order key

## Pre-sort the total file list.  (Just in case.)  This may not be necessary
def revkey(order):
    return order
sorted(fileSRClist, key=revkey)

##  Return the location of the revision character
def length(x):
    return len(x)-5

##  Initialize latest_rev_list by storing the first item from the total file list
for dwg_file in fileSRClist:
    if dwg_file[filetype_loc] == str(filetype):
        latest_rev_list.append(dwg_file)
        break

##  EXTRACT LATEST REVISED FILES ONLY
##  This will loop through every single dwg file from the source directory,
##  extract the revision of the file (assuming that the revision character
##  is the fourth last character) and pull the drawing file with the highest
##  revision character and store it into latest_rev_list.
for dwg_file in fileSRClist:
    if dwg_file[filetype_loc] == str(filetype):
        revision = dwg_file[length(dwg_file)].upper()
        fname.append(dwg_file[:length(dwg_file)])
        rev.append(revision)
        if order.index(revision) >= order.index(temprev) and dwg_file[:length(dwg_file)]==tempname:
            latest_rev_list[count] = dwg_file
            temprev = revision
            tempfile = dwg_file
        elif dwg_file[:length(dwg_file)]!=tempname:
            latest_rev_list.append(dwg_file)
            temprev = revision
            tempname = dwg_file[:length(dwg_file)]
            count += 1

##  PRINT LATEST_REV_LIST
##  the following will print every item in latest_rev_list to test if we did, in fact,
##  grab the latest revised drawing and store it in the list
for item in latest_rev_list:
    print item
print str(len(latest_rev_list)) + " files copied from " + source[:len(source)-6] + " into " + destination

##  COPY AND PASTE
for drawing in latest_rev_list:
    shutil.copy(drawing, destination)
