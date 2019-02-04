from UserDict import DictMixin
from ordereddict import OrderedDict
import calendar, wx

# ---------------------------------------------------------------------------

class typeNavMgr(object):
    """ A parent class that generates master data for use in date navigation.
    This object can only work after a database manager has been created.
    The main activity here is to group the master data by year and then navigate
    the data based on queries from visulization windows.
    """

    '''This bit is retained for future reference (took forever to get this info)
        # Remove negative dates
        for item in self.raw:
        if item[4]<0: self.raw.pop(self.raw.index(item))

        # Sort on year
        self.raw.sort(key=lambda x: x[4])'''

    def __init__(self, mgr):

        # Initialize variables
        self.initializevars(mgr)

    # ------------------------------------------------------
    # Methods

    def respond(self, query=None):
        '''accepts input from the parent parent and responds by
            returning the appropriate data'''
        print 'TypeNavigator: recieved a %s command .....' %query
        # Choose the appropriate method and get new data
        if query == 'back' or query == 'fwd' or query == 'rst':
            self.level = self.mgr.navshistory[self.mgr.historypoint][2]
            self.query = None

        elif query == 'update':
            if self.level < 0: self.level += 1 # handle first pass update
            self.query = None

            # prepare global newraw shell for mgr iteration to populate
            self.preprocess()

        else:
            self.level += 1
            self.query = query
            self.queryhistory[self.level] = query

            if self.level <= 1:
                # prepare global newraw shell for mgr iteration to populate
                self.preprocess()

                # check the local raw data and select the data for this query
                selection = self.getselection(self.query)

                # Pass the selection to the datamanager for iteration
                self.mgr.iteriselection(selection, 3) # 3 = TypeNavigator's call-sign

            else:
                # Roll back because I only want up to level 1
                self.queryhistory.pop(self.level)
                self.level -= 1


    def getselection(self, query):
        # Check the raw data
        if query == None:
            selection = self.selectionhistory[self.mgr.historypoint]
        else:
            selection = self.raw[query]
            self.updatemgr(query, selection)
        return selection

    def preprocess(self):
        if self.level == 0:
            # Define shell for the newraw and data
            self.newraw = OrderedDict([('doc',[]), ('vid',[]), ('pic',[]), ('aud',[]), ('exe',[]), ('others',[])])
            self.data = OrderedDict([('doc',0), ('vid',0), ('pic',0), ('aud',0), ('exe',0), ('others',0)])

        elif self.level == 1:
            query = self.queryhistory[self.level]
            # Define shell for the newraw and data
            self.newraw = OrderedDict([(query, [])])
            self.data = OrderedDict([(query, 0)])

        elif self.level > 1:
            self.level -= 1

    def processfile(self, dfile):
        if self.level == 0:
            filetype = dfile[4]
            self.newraw[filetype].append(dfile)
        elif self.level == 1:
            filetype = dfile[4]
            self.newraw[filetype].append(dfile)

    def postprocess(self):
        for item in self.newraw:
            self.data[item] = len(self.newraw[item])

        # Label processing before calling the visualizer
        for item in self.queryhistory:
            if item == 0: query = 'All'
            else: query = self.queryhistory[item]
            tag = 'File-Type'
            self.labels[item] = [tag, query]

        self.refreshWindows(self.data, self.level, self.labels)

    def refreshWindows(self, data, level, labels):
        self.mgr.sbook.tpanel.win.reload(data, level, labels)

    def getdata(self, level, query=None):
        if level == 0: data = self.getlvl0data(query)
        elif level == 1: data = self.getlvl1data(query)
        elif level == 2: data = self.getlvl2data(query)
        elif level == 3: data = self.getlvl3data(query)
        elif level == 4: data = self.getlvl4data(query)
        return data

    def updateRaw(self):
        self.raw = self.newraw.copy()

    def updatemgr(self, query, selection):

        # Clear old selections from history
        cache = []
        for item in self.selectionhistory:
            if item > self.mgr.historypoint: cache.append(item)
        for item in cache:
            self.selectionhistory.pop(item)
            self.mgr.navsqueryhistory.pop(item)

        # Clear old queries from history
        cache = []
        for item in self.queryhistory:
            if item > self.level: cache.append(item)
        for item in cache:
            self.queryhistory.pop(item)
            self.labels.pop(item)

        self.mgr.historypoint += 1
        curr = self.mgr.historypoint
        prev = curr - 1

        # update the manager's query history here
        dquery, squery, tquery = self.mgr.navsqueryhistory[prev]
        tquery = query
        self.mgr.navsqueryhistory[curr] = (dquery, squery, tquery)

        self.mgr.typequeryhist.append(query)
        self.queryhistory[self.level] = query
        self.selectionhistory[self.mgr.historypoint] = selection[0:]

    def updatenavs(self):
        self.mgr.updatenavs(1)

    def getlvl0data(self, query=None):
        '''Level zero presents each year with total file sizes
            raw data for this method should be the master list of files'''

        if query != None:
            selection = self.mgr.master
            self.updatemgr(query, selection, 1)
        else:
            selection = self.selectionhistory[self.mgr.historypoint]

        # Define shell for the data
        newraw = OrderedDict([('doc',[]), ('vid',[]), ('pic',[]), ('aud',[]), ('exe',[]), ('others',[])])
        data = OrderedDict([('doc',0), ('vid',0), ('pic',0), ('aud',0), ('exe',0), ('others',0)])

#------------------------------------------------------------------------
        # Iterate through the master list and group files by year
        for dfile in selection:
            filetype = dfile[4]
            newraw[filetype].append(dfile)
            data[filetype] = data[filetype] + 1
#-------------------------------------------------------------------------

        # Save the raw that level 1 will use to sort itself out
        self.updateRaw(newraw)
        return data

    def initializevars(self, mgr):
        self.query = 0
        self.type = 't'
        self.queryhistory = {0:'All'}
        self.raw = []
        self.selectionhistory = mgr.selectionhistory
        self.level = -1
        self.mgr = mgr
        self.labels = {}
        self.fpass = True
        self.documents = ['ade', 'adp', 'mpd', 'mde', 'mpc', 'mpp', 'mpv', 'vdx', 'mpx', 'vsl', 'vst', 'vsw',
                'vsx', 'vtx', 'dvi', 'eps', 'jnt', 'latex', 'pm', 'pm5', 'ps', 'pt5', 'rtx', 'tex', 'xml',
                'pdf', 'doc', 'dot', 'htm', 'html', 'mht', 'one', 'rtf', 'txt', 'xml', 'ppz', 'pot', 'pps',
                'ppt', 'xls', 'xlw', 'csv', 'tsv', 'wks', 'xlb', 'xlc', 'xll', 'xlm', 'xls', 'xlw', 'eml',
                'msg', 'vcf', 'vcard', 'ics', 'vcs']

        self.videos = ['asf', 'asx', 'avi', 'awm', 'cmv', 'm1v', 'mmm', 'mov', 'mp2', 'mpa', 'mpe', 'mpeg',
                'mpg', 'mpv2', 'mwf', 'qt', 'vue', 'wmv', 'wvx']

        self.images = ['3ds', 'a11', 'ai', 'ani', 'anm', 'art', 'b_w', 'b&w', 'b1n', 'b8', 'bga', 'bit', 'bld',
                'bm', 'bmp', 'cdf', 'cdr', 'cmp', 'cps', 'cvs', 'dib', 'dip', 'dcx', 'dkb', 'dw2', 'dwg', 'fh3',
                'fh4', 'fit', 'flc', 'fli', 'gcd', 'gif', 'gl', 'gsd', 'hrf', 'hs2', 'hsi', 'iax','ica', 'ico',
               'jas', 'jff', 'jpc', 'icb', 'jpe', 'jpeg', 'jpg', 'jtf', 'lbm', 'mpt', 'msp', 'nc', 'neo',
                'pct', 'pcx', 'pda', 'pdd', 'pgm', 'pix', 'png', 'ppm', 'psd', 'pse', 'qdv', 'rgb', 'rif',
               'rip', 'rix', 'rl4', 'rl8', 'sg1', 'tif', 'tiff', 'van', 'vda', 'vdr', 'wmf', 'xif', 'xpm']

        self.audio = ['aac', 'aif', 'aiff', 'amf', 'au', 'cda', 'dfs', 'dss', 'far', 'm3u', 'mid', 'midi', 'mp3',
                'mus', 'okt', 'p16', 'psm', 'ra', 'ram', 'rmi', 's3m', 'snd', 'sng', 'stm', 'ult', 'uw',
                'voc', 'wav', 'wma', 'xm', 'xmi']

        self.executables = ['exe', 'msi', 'com']

        self.others = ['acf', 'aifc', 'ascx', 'asm', 'asp', 'aspx', 'cab', 'cpl', 'cs', 'css', 'cur',
               'def', 'dic', 'emf', 'gz', 'hhc', 'idq', 'ivf', 'ivf', 'jfif', 'lnk', 'mapiipm.Note',
                'mda', 'mp2v', 'odc', 'pl', 'rle', 'scd', 'tar', 'tgz', 'tsp', 'wax', 'wbk', 'sch', 'wiz',
                'wm', 'wmp', 'wmx', 'wmz', 'wri', 'wsz', 'wtx', 'xlk', 'z', 'zip', 'bat', 'c', 'cmd', 'cpp',
                'cxx', 'Dif', 'disco', 'h', 'hpp', 'hxx', 'idl', 'inc', 'inf', 'inx', 'js', 'nws', 'pl', 'ppa',
                'pwz', 'rc', 'reg', 'resx', 'slk', 'url', 'vbs', 'xla', 'xld', 'xlt', 'xlv', 'xsl']

# ---------------------------------------------------------------------------