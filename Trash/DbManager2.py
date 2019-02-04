import time, sqlite3, calendar
from UserDict import DictMixin
from ordereddict import OrderedDict
#from collections import OrderedDict

mydict = OrderedDict()
class DBManager(object):

    def __init__(self, name):
        # Initialize variables and create the db/file connection:
        self.conn = sqlite3.connect(name) # update later to check if db exists
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

        # Get a raw list of all files in the selected harddisk
        result = self.cur.execute('select * from Files;')
        self.master = result.fetchall()


class SizeNavMgr(object):
    """ A parent class that generates master data for use in size navigation.
    This object can only work after a database manager has been created.
    The main activity here is to group the master data by size and then navigate
    the data based on queries from visulization window.
    """

    def __init__(self, parent, mgr):

        # Initialize variables
        self.initializevars(mgr.master, parent)

    # ------------------------------------------------------
    # Methods

    def respond(self, query=None):
        '''accepts input from the parent parent and responds by
            returning the appropriate data'''

        # Choose the appropriate method and get new data
        if query == 'back':
            if self.level > 0: self.level -= 1
            self.query = self.queryhistory[self.level]
            self.raw = self.rawhistory[self.level]

        elif query == 'fwd':
            if self.level < len(self.queryhistory)-1: self.level += 1
            self.query = self.queryhistory[self.level]
            self.raw = self.rawhistory[self.level]

        else:
            self.level += 1
            self.queryhistory[self.level] = query
            self.query = query

        #print self.query
        #print self.queryhistory
        data = self.getData(self.level, self.raw, self.query)
        #self.refreshWindows(data, self.level)
        return data

    def refreshWindows(self, data, level):
        raw = self.rawhistory[level]
        query = self.queryhistory[level]
        selection = raw[query]

        self.parent.vizwin.reload(data, self.level)
        print 'No of files = %d' %len(selection)
        self.parent.resultwin.reload(selection)

    def getData(self, level, raw, query=None):
        data = self.getlvl0data(raw, query)
        return data

    def updateRaw(self, newraw):
        self.raw = newraw.copy()

    def getlvl0data(self, raw, query=False):
        '''Level zero presents each year with total file sizes
            raw data for this method should be the master list of files'''

        selection = raw[query]

        # Iterate through the master list and get max/min sizes
        newraw = OrderedDict({})
        smax, smin = selection[0][4], selection[0][4]

        for file in selection:
            size = file[4]
            if size > smax:
                smax = size
            elif size < smin:
                smin = size

        # Create the bins with size ranges
        bincount = 10
        binsize = (smax - smin)/10.00
        low = smin
        bindata = OrderedDict({}) # captures the number of files per bin
        binlimits = OrderedDict({}) # holds the upper size limit for each bin

        for bin in range(bincount):
            high = low + binsize
            label = '%f-%f' %(low, high)
            binlimits[label] = high
            low = high

        # Reiterate and get the no of files per bin
        newraw = binlimits.copy() # raw data for use in next level
        bindata = binlimits.copy()
        for bin in newraw: newraw[bin] = [] # empty the copy
        for bin in bindata: bindata[bin] = 0 # empty the copy

        for file in selection:
            size = file[4]
            for bin in binlimits:
                if size < binlimits[bin]:
                    newraw[bin].append(file)
                    bindata[bin] += 1
                    break   # sue me

        print smin, smax, '\n'
        for item in binlimits: print item
        print '\n'
        if self.level > 0: print selection

        # Iterate through the raw list and group the data by year
        data = bindata.copy()

        # save the raw data for this level for reverse navigation
        self.rawhistory[self.level] = raw.copy()

        # Save the raw that level 1 will use to sort itself out
        self.updateRaw(newraw)
        return data

    def initializevars(self, data, parentwin):
        self.query = 0
        self.queryhistory = {}
        self.raw = {0:data[0:]}
        self.rawhistory = {}
        self.level = -1
        self.parent = parentwin

if __name__ == '__main__':
    fltstart = float(time.clock())
    mgr = DBManager('Magee.db')
    dwin = dateNavMgr(None, mgr)
    fltfinish = float(time.clock())
    print('Completed in %f seconds') %(fltfinish - fltstart)
    raw_input('Press enter to exit::')