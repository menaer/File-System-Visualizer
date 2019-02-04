import win32file, win32api
import sys, os, sqlite3, time

DRIVE_TYPES = """
0 	Unknown
1 	No Root Directory
2 	Removable Disk
3 	Local Disk
4 	Network Drive
5 	Compact Disc
6 	RAM Disk
"""
"""
drive_types = dict((int (i), j) for (i, j) in (l.split ("\t") for l in DRIVE_TYPES.splitlines () if l))
drives = (drive for drive in win32api.GetLogicalDriveStrings ().split ("\000") if drive)
for drive in drives:
  print drive, "=>", drive_types[win32file.GetDriveType (drive)]
"""

def fnIndexConnect(filename):
    ifile = open(filename, 'w')
    return ifile

def fnDbClose(objConn, objCursor):
    objConn.commit()
    objCursor.close()
    objConn.close()
    return True

def fnDbDropTables(tableNames, cursor):
    for table in tableNames:
        try:
            cursor.execute('drop table %s' %table)
            print 'Dropped %s' %table
        except:
            pass
    return

def fnDbCreateTables(objCursor):

    #Create data table
    command ='data text primary key'
    objCursor.execute('create table Rawdata (%s)'%command)

    #Create drives table
    command ='driveid integer primary key, drive text, no_of_folders,\
                no_of_files integer, folders text, files text'
    objCursor.execute('create table Drives (%s)'%command)

    #Create files table
    command ='fileid integer primary key, filename text, folderid text, extension text,\
                attributes text, date_created text, date_modified text, driveid integer'
    objCursor.execute('create table Files (%s)'%command)
    return

def fnProcessFiles(path, files, ifile):
    counter = 0
    filepath = ''
    filelist = []
    for file in files:
        filename = file
        if path[-1] == '\\': filepath = path + filename
        else: filepath = path + '\\'+ filename
        extension = file.split('.')[-1]
        filesize, filestats = 0, []

        try:
            filestats = os.stat(filepath)
        except:
            print 'error detecting file attributes for %s' %filepath


        tuprowdata = [filename, extension, filestats]
        print >> ifile, tuprowdata


def fnIndexDrives(drives, filename):
    ifile = fnIndexConnect(filename)

    totalerrorcount = 0
    counter = 0
    drivelist = []
    dirlist = []
    for root in drives:

        for path, lstdirs, lstFiles in os.walk(root):
            # File processing
            fnProcessFiles(path, lstFiles, ifile)

    ifile.close()


if __name__ == '__main__':
    intstart = float(time.clock()) #Start

    drives = ['I:\\']
    #drives = [drive for drive in win32api.GetLogicalDriveStrings ().split ("\000") if drive]

    print '\nCreating a new index database file.....\n'

    drivelist = fnIndexDrives(drives, 'InvIndex.txt')
    intfinish = float(time.clock()) #Stop
    print '%d drives %s indexed in %f seconds' %(len(drives), drives, (intfinish-intstart))
    #%print 'errorcount: %d' %errorcount