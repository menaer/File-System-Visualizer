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

def fnDbConnect(txtDbName):
    conn = sqlite3.connect(txtDbName)
    cur = conn.cursor()
    cur.execute('PRAGMA synchronous=OFF')
    return conn, cur

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
    command ='fileid integer primary key, path text, filename text, extension text, type text, iconID integer, size long, year long, month long, day long, date_mod long'
    objCursor.execute('create table Files (%s)'%command)
    return

def fnProcessFiles(path, files, cursor, extdict):
    counter = 0
    filepath = ''
    filelist = []
    for file in files:
        filename = file
        if path[-1] == '\\': filepath = path + filename
        else: filepath = path + '\\'+ filename
        extension = '.'+ file.split('.')[-1].lower()
        filesize, filestats = 0, []

        for item in extdict:
            types = extdict[item]
            try:
                types.index(extension)
                filetype = item
                break   # sue me
            except:
                filetype = 'others'

        try:
            #filestats = os.stat(filepath)
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filepath)
            tuprowdata = (path, filename, extension, filetype, size, int(time.ctime(mtime).split(' ')[-1]), time.ctime(mtime).split(' ')[1], time.ctime(mtime).split(' ')[2])
        except:
            print 'error detecting file attributes for %s' %filepath

        #write to db
        #filelist.append(tuprowdata)
        try:
            cursor.execute('insert into Files (path, filename, extension, type, size, year, month, day) values(?,?,?,?,?,?,?,?)', tuprowdata)
        except:
            print 'unable to insert data for %s' %filepath
            counter += 1

    return counter

def createxts():
    documents = ['.ade', '.adp', '.mpd', '.mde', '.mpc', '.mpp', '.mpv', '.vdx',
                '.mpx', '.vsl', '.vst', '.vsw', '.vsx', '.vtx', '.dvi', '.eps',
                '.jnt', '.latex', '.pm', '.pm5', '.ps', '.pt5', '.rtx', '.tex',
                '.xml', '.pdf', '.doc', '.dot', '.htm', '.html', '.mht', '.one',
                '.rtf', '.txt', '.xml', '.ppz', '.pot', '.pps', '.ppt', '.xls',
                '.xlw', '.csv', '.tsv', '.wks', '.xlb', '.xlc', '.xll', '.xlm',
                '.xls', '.xlw', '.eml', '.msg', '.vcf', '.vcard', '.ics', '.vcs']

    videos = ['.asf', '.asx', '.avi', '.awm', '.cmv', '.m1v', '.mmm', '.mov',
                '.mp2', '.mpa', '.mpe', '.mpeg', '.mpg', '.mpv2', '.mwf', '.qt',
                '.vue', '.wmv', '.wvx']

    images = ['.3ds', '.a11', '.ai', '.ani', '.anm', '.art', '.b_w', '.b&w', '.b1n',
                '.b8', '.bga', '.bit', '.bld', '.bm', '.cdf', '.cdr', '.cmp', '.cps',
                '.cvs', '.dib', '.dip', '.dcx', '.dkb', '.dw2', '.dwg', '.fh3', '.fh4',
                '.fit', '.flc', '.fli', '.gcd', '.gif', '.gl', '.gsd', '.hrf', '.hs2',
                '.hsi', '.iax', '.ica', '.jas', '.jff', '.jpc', '.icb', '.jpe', '.jpeg',
                '.jpg', '.jtf', '.lbm', '.mpt', '.msp', '.nc', '.neo', '.pct', '.pcx',
                '.pda', '.pdd', '.pgm', '.pix', '.png', '.ppm', '.psd', '.pse', '.qdv',
                '.rgb', '.rif', '.rip', '.rix', '.rl4', '.rl8', '.sg1', '.tif', '.tiff',
                '.van', '.vda', '.vdr', '.wmf', '.xif', '.xpm']

    audio = ['.aac', '.aif', '.aiff', '.amf', '.au', '.cda', '.dfs', '.dss', '.far',
                '.m3u', '.mid', '.midi', '.mp3', '.mus', '.okt', '.p16', '.psm', '.ra', '.ram',
                '.rmi', '.s3m', '.snd', '.sng', '.stm', '.ult', '.uw', '.voc', '.wav', '.wma',
                '.xm', '.xmi']

    executables = ['.exe', '.msi', '.com']

    others = ['.acf', '.aifc', '.ascx', '.asm', '.asp', '.aspx', '.bmp', '.cab', '.cpl',
                '.cs', '.css', '.cur', '.def', '.dic', '.emf', '.gz', '.hhc', '.ico', '.idq',
                '.ivf', '.ivf', '.jfif', '.lnk', '.mapiipm.Note', '.mda', '.mp2v', '.odc', '.pl',
                '.rle', '.scd', '.tar', '.tgz', '.tsp', '.wax', '.wbk', '.sch', '.wiz', '.wm',
                '.wmp', '.wmx', '.wmz', '.wri', '.wsz', '.wtx', '.xlk', '.z', '.zip', '.bat',
                '.c', '.cmd', '.cpp', '.cxx', '.Dif', '.disco', '.h', '.hpp', '.hxx', '.idl',
                '.inc', '.inf', '.inx', '.js', '.nws', '.pl', '.ppa', '.pwz', '.rc', '.reg',
                '.resx', '.slk', '.url', '.vbs', '.xla', '.xld', '.xlt', '.xlv', '.xsl']

    return {'doc':documents, 'vid':videos, 'pic':images, 'aud':audio, 'exe':executables, 'others':others}

def fnIndexDrives(drives, dbName):
    conn, cur = fnDbConnect(dbName)
    tableNames = ['Drives', 'Files', 'Rawdata']

    fnDbDropTables(tableNames, cur)
    fnDbCreateTables(cur)

    totalerrorcount = 0
    counter = 0
    drivelist = []
    dirlist = []
    extdict = createxts()
    for root in drives:
        tuprowdata = (root,)
        cur.execute('insert into drives (drive) values(?)', tuprowdata)

        for path, lstdirs, lstFiles in os.walk(root):
            # File processing
            counter = fnProcessFiles(path, lstFiles, cur, extdict)
            #dirlist.append(counter)
            totalerrorcount += counter

        #drivelist.append((root, dirlist))

    print 'Completed'
    #tuprowdata = (str(drivelist),)
    #cur.execute('insert into Rawdata (data) values(?)', tuprowdata)

    conn.commit()
    conn.close()
    return drivelist


if __name__ == '__main__':
    intstart = float(time.clock()) #Start

    drives = ['F:\\']
    #drives = [drive for drive in win32api.GetLogicalDriveStrings ().split ("\000") if drive]

    print '\nCreating a new index database file.....\n'

    drivelist = fnIndexDrives(drives, 'InvIndex.db')
    intfinish = float(time.clock()) #Stop
    print '%d drives %s indexed in %f seconds' %(len(drives), drives, (intfinish-intstart))
    raw_input('Press enter to exit.....')
    #%print 'errorcount: %d' %errorcount