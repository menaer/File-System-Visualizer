import os, fnmatch, sqlite3, time
fltstart = float(time.clock())

print ('Running database tests')

def dodbstuff():
    conn = sqlite3.connect('InvIndex.db')
    cur = conn.cursor()
    comm = cur.execute
    comm('PRAGMA synchronous=OFF')
    #comm('PRAGMA synchronous=NORMAL')

    return comm, cur, conn

def createlists():
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

    images = ['.img', '.3ds', '.a11', '.ai', '.ani', '.anm', '.art', '.b_w', '.b&w', '.b1n',
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


def processfile(lists, ext):
    for item in lists:
        extensions = lists[item]
        try:
            extensions.index(ext)
            filetype = item
            break   # sue me
        except:
            filetype = 'others'

    return filetype


def end(comm, cur, conn):
    del comm
    cur.close()
    conn.close()


if __name__ == '__main__':
    try:
        end(comm, cur, conn)
    except: pass

    comm, cur, conn = dodbstuff()
    lists = createlists()
    result = comm("select fileid, extension, type from files").fetchall()

    for item in range(10):
        print result[item]

    for dfile in result:
        fileid = dfile[0]
        extension = dfile[1]
        filetype = processfile(lists, extension)
        command = "update Files set type='"'%s'"' where fileid=%d" %(filetype, fileid)
        #print fileid, extension, filetype, command
        comm(command)


    check = comm("select fileid, extension, type from files").fetchall()
    conn.commit()

    #print '\n\n'
    for item in range(50):
        print check[item]
