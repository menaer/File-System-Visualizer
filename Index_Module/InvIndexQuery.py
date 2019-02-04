import os, fnmatch, sqlite3, time
fltstart = float(time.clock())

def fnRunTests():

    print ('Running database tests')
    conn = sqlite3.connect('InvIndex.db')
    cur = conn.cursor()
    #cur.execute('PRAGMA synchronous=NORMAL')

    # Check for tables
    result = cur.execute('select name from sqlite_master where type="table" order by name;')
    print result.fetchall(), '\n'

    # Check for columns
    result = cur.execute('PRAGMA table_info(Files)')
    print 'Columns in Files table ...'
    print result.fetchall(), '\n'

    result = cur.execute('PRAGMA table_info(Drives)')
    print 'Columns in Drives table ...'
    print result.fetchall(), '\n'

    # Get all drives
    print 'Displaying all drives'
    result = cur.execute('select * from drives order by drive;')
    for x in result.fetchmany(15): print x
    print '\n'

    # Get first 20 rows in Files
    print 'Displaying first 20 files'
    result = cur.execute('select * from Files;')
    for x in result.fetchmany(20): print x
    print '\n'

    # Get number of rows in Files
    print 'Displaying total number of files'
    result = cur.execute('select count(*) from Files;')
    print result.fetchall(), '\n'

    # Get total file size
    #print 'Displaying total size of all files'
    #result = cur.execute('select sum(size) from Files;')
    #print result.fetchall(), '\n'


    # Summarize the extension list#
    #conn.text_factory = str
    #result = cur.execute('select * from Files order by year;')
    #extensions = result.fetchall()
    #extensions.sort()
    #summexts, docs = [], []
    #ext, size, itemcount = extensions[0][0].lower(), 0, 0
    #for item in extensions:
    #    pass
        #if item[0].lower() == ext:
        #    ext, size, itemcount = item[0].lower(), size + float(item[1][6]), itemcount + 1
        #else:
        #    summexts.append((ext, size, itemcount))
        #    ext, size, itemcount = item[0].lower(), item[1], 1

    # capture last item
    #summexts.append((ext, size, itemcount))
    #summexts.sort()

    #for item in summexts:
        #ext = item[0]

        #documents = ['ade', 'adp', 'mpd', 'mde', 'mpc', 'mpp', 'mpv', 'vdx', 'mpx', 'vsl', 'vst', 'vsw',
        #        'vsx', 'vtx', 'dvi', 'eps', 'jnt', 'latex', 'pm', 'pm5', 'ps', 'pt5', 'rtx', 'tex', 'xml',
        #        'pdf', 'doc', 'dot', 'htm', 'html', 'mht', 'one', 'rtf', 'txt', 'xml', 'ppz', 'pot', 'pps',
        #        'ppt', 'xls', 'xlw', 'csv', 'tsv', 'wks', 'xlb', 'xlc', 'xll', 'xlm', 'xls', 'xlw', 'eml',
        #        'msg', 'vcf', 'vcard', 'ics', 'vcs']

        #videos = ['asf', 'asx', 'avi', 'awm', 'cmv', 'm1v', 'mmm', 'mov', 'mp2', 'mpa', 'mpe', 'mpeg',
        #        'mpg', 'mpv2', 'mwf', 'qt', 'vue', 'wmv', 'wvx']

        #images = ['3ds', 'a11', 'ai', 'ani', 'anm', 'art', 'b_w', 'b&w', 'b1n', 'b8', 'bga', 'bit', 'bld',
        #        'bm', 'cdf', 'cdr', 'cmp', 'cps', 'cvs', 'dib', 'dip', 'dcx', 'dkb', 'dw2', 'dwg', 'fh3',
        #        'fh4', 'fit', 'flc', 'fli', 'gcd', 'gif', 'gl', 'gsd', 'hrf', 'hs2', 'hsi', 'iax','ica',
        #       'jas', 'jff', 'jpc', 'icb', 'jpe', 'jpeg', 'jpg', 'jtf', 'lbm', 'mpt', 'msp', 'nc', 'neo',
        #        'pct', 'pcx', 'pda', 'pdd', 'pgm', 'pix', 'png', 'ppm', 'psd', 'pse', 'qdv', 'rgb', 'rif',
        #       'rip', 'rix', 'rl4', 'rl8', 'sg1', 'tif', 'tiff', 'van', 'vda', 'vdr', 'wmf', 'xif', 'xpm']

        #audio = ['aac', 'aif', 'aiff', 'amf', 'au', 'cda', 'dfs', 'dss', 'far', 'm3u', 'mid', 'midi', 'mp3',
        #        'mus', 'okt', 'p16', 'psm', 'ra', 'ram', 'rmi', 's3m', 'snd', 'sng', 'stm', 'ult', 'uw',
        #        'voc', 'wav', 'wma', 'xm', 'xmi']

        #executables = ['exe', 'msi', 'com']

        #Others = ['acf', 'aifc', 'ascx', 'asm', 'asp', 'aspx', 'bmp', 'cab', 'cpl', 'cs', 'css', 'cur',
        #       'def', 'dic', 'emf', 'gz', 'hhc', 'ico', 'idq', 'ivf', 'ivf', 'jfif', 'lnk', 'mapiipm.Note',
        #        'mda', 'mp2v', 'odc', 'pl', 'rle', 'scd', 'tar', 'tgz', 'tsp', 'wax', 'wbk', 'sch', 'wiz',
        #        'wm', 'wmp', 'wmx', 'wmz', 'wri', 'wsz', 'wtx', 'xlk', 'z', 'zip', 'bat', 'c', 'cmd', 'cpp',
        #        'cxx', 'Dif', 'disco', 'h', 'hpp', 'hxx', 'idl', 'inc', 'inf', 'inx', 'js', 'nws', 'pl', 'ppa',
        #        'pwz', 'rc', 'reg', 'resx', 'slk', 'url', 'vbs', 'xla', 'xld', 'xlt', 'xlv', 'xsl']

        #if ext in documents: docs.append(ext)




    #conn.close()
    return result, conn, cur


# ==================================================================
# Remember google query : 'using python to navigate filesystem'
# ==================================================================
result, conn, cur = fnRunTests()
fltfinish = float(time.clock())
print ('Completed in %f seconds') %(fltfinish - fltstart)