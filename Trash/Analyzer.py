import wx, os, time
import sqlite3

''' This module contains two classes
    class 1 is a db manager which accesses the index and holds rawdata for other classes to use
    class 2 is a prototype of the type-window manager. It gets raw data from manager and analyses it.
'''

class DbManager(object):
    def __init__(self):

        # Initialize variables and create the db/file connection:
        self.conn = sqlite3.connect('InvIndex.db')
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        #print 'Database connection established ...'

        # Get a raw list of all files in the selected harddisk
        result = self.cur.execute('select * from Files order by year;')
        self.rawlist = result.fetchall()


class TypeWinManager(object):
    def __init__(self, mgr):
        rawlist = mgr.rawlist

        # Summarize extensions to get level one data
        self.raw = rawlist[0:]
        lvl1raw = rawlist[0:]

        self.lvl1data, docs = [], []
        ext, size, itemcount = self.raw[0][3].lower(), 0, 0

        for item in self.raw:
            if item[3].lower() == ext:
                ext, size, itemcount = item[3].lower(), size + float(item[4]), itemcount + 1
            else:
                #self.summexts.append((ext, size, itemcount))
                self.lvl1data.append((ext, size))
                ext, size, itemcount = item[3].lower(), item[4], 1

        # capture last item
        #self.summexts.append((ext, size, itemcount))
        self.lvl1data.append((ext, size))
        self.lvl0data = self.getlevel0data(self.lvl1data)

    def getlevel0data(self, rawdata):
        documents = ['ade', 'adp', 'mpd', 'mde', 'mpc', 'mpp', 'mpv', 'vdx', 'mpx', 'vsl', 'vst', 'vsw',
                'vsx', 'vtx', 'dvi', 'eps', 'jnt', 'latex', 'pm', 'pm5', 'ps', 'pt5', 'rtx', 'tex', 'xml',
                'pdf', 'doc', 'dot', 'htm', 'html', 'mht', 'one', 'rtf', 'txt', 'xml', 'ppz', 'pot', 'pps',
                'ppt', 'xls', 'xlw', 'csv', 'tsv', 'wks', 'xlb', 'xlc', 'xll', 'xlm', 'xls', 'xlw', 'eml',
                'msg', 'vcf', 'vcard', 'ics', 'vcs']

        videos = ['asf', 'asx', 'avi', 'awm', 'cmv', 'm1v', 'mmm', 'mov', 'mp2', 'mpa', 'mpe', 'mpeg',
                'mpg', 'mpv2', 'mwf', 'qt', 'vue', 'wmv', 'wvx']

        images = ['3ds', 'a11', 'ai', 'ani', 'anm', 'art', 'b_w', 'b&w', 'b1n', 'b8', 'bga', 'bit', 'bld',
                'bm', 'bmp', 'cdf', 'cdr', 'cmp', 'cps', 'cvs', 'dib', 'dip', 'dcx', 'dkb', 'dw2', 'dwg', 'fh3',
                'fh4', 'fit', 'flc', 'fli', 'gcd', 'gif', 'gl', 'gsd', 'hrf', 'hs2', 'hsi', 'iax','ica', 'ico',
               'jas', 'jff', 'jpc', 'icb', 'jpe', 'jpeg', 'jpg', 'jtf', 'lbm', 'mpt', 'msp', 'nc', 'neo',
                'pct', 'pcx', 'pda', 'pdd', 'pgm', 'pix', 'png', 'ppm', 'psd', 'pse', 'qdv', 'rgb', 'rif',
               'rip', 'rix', 'rl4', 'rl8', 'sg1', 'tif', 'tiff', 'van', 'vda', 'vdr', 'wmf', 'xif', 'xpm']

        audio = ['aac', 'aif', 'aiff', 'amf', 'au', 'cda', 'dfs', 'dss', 'far', 'm3u', 'mid', 'midi', 'mp3',
                'mus', 'okt', 'p16', 'psm', 'ra', 'ram', 'rmi', 's3m', 'snd', 'sng', 'stm', 'ult', 'uw',
                'voc', 'wav', 'wma', 'xm', 'xmi']

        executables = ['exe', 'msi', 'com']

        others = ['acf', 'aifc', 'ascx', 'asm', 'asp', 'aspx', 'cab', 'cpl', 'cs', 'css', 'cur',
               'def', 'dic', 'emf', 'gz', 'hhc', 'idq', 'ivf', 'ivf', 'jfif', 'lnk', 'mapiipm.Note',
                'mda', 'mp2v', 'odc', 'pl', 'rle', 'scd', 'tar', 'tgz', 'tsp', 'wax', 'wbk', 'sch', 'wiz',
                'wm', 'wmp', 'wmx', 'wmz', 'wri', 'wsz', 'wtx', 'xlk', 'z', 'zip', 'bat', 'c', 'cmd', 'cpp',
                'cxx', 'Dif', 'disco', 'h', 'hpp', 'hxx', 'idl', 'inc', 'inf', 'inx', 'js', 'nws', 'pl', 'ppa',
                'pwz', 'rc', 'reg', 'resx', 'slk', 'url', 'vbs', 'xla', 'xld', 'xlt', 'xlv', 'xsl']

        types = (documents, videos, images, audio, executables, others)
        docs, vids, imgs, songs, progs, misc = 0,0,0,0,0,0

        # Documents
        docexts = []
        for item in rawdata:
            extension = item[0]
            size = item[1]

            try: types[0].index(extension); docs += size;   #Documents
            except: pass
            try: types[1].index(extension); vids += size;   #Videos
            except: pass
            try: types[2].index(extension); imgs += size;   #Images
            except: pass
            try: types[3].index(extension); songs += size;  #Audio
            except: pass
            try: types[4].index(extension); progs += size;  #Executables
            except: pass
            try: types[5].index(extension); misc += size; docexts.append(extension)   #Others
            except: pass

        #Scale the data
        sizes = [docs, vids, imgs, songs, progs, misc]
        return sizes


class DateWinManager(object):
    def __init__(self, mgr):
        self.raw = mgr.rawlist[0:]
        # Remove negative dates
        #for item in self.raw:
            #if item[4]<0: self.raw.pop(self.raw.index(item))

        # Sort on year
        #self.raw.sort(key=lambda x: x[4])

        # Iterate through the raw list and group the data by year
        self.years, self.files, temp = {},{},[]
        year = self.raw[0][5]
        size = 0
        for item in self.raw:
            if item[5] == year:
                #size += item[4]
                temp.append(item)
            else:
                #self.years[year] = size
                self.files[year] = temp
                year = item[5]
                #size = item[4]
                temp = []
                temp.append(item)

        #Handle last item
        #self.years[year] = size
        self.files[year] = temp

    def getlevel0data(self, rawdata):
        pass


if __name__ == '__main__':

    fltstart = float(time.clock())
    mgr = DbManager()
    #typemgr = TypeWinManager(mgr)
    datemgr = DateWinManager(mgr)
    fltfinish = float(time.clock())
    print ('Completed in %f seconds') %(fltfinish - fltstart)
    raw_input('Press enter to exit::')