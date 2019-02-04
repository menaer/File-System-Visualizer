from UserDict import DictMixin
from ordereddict import OrderedDict

# ---------------------------------------------------------------------------

class sizeNavMgr(object):
    """ A parent class that generates master data for use in size navigation.
    This object can only work after a database manager has been created.
    The main activity here is to group the master data by size and then navigate
    the data based on queries from visulization window.
    """

    def __init__(self, mgr):

        # Initialize variables
        self.initializevars(mgr)

    # ------------------------------------------------------
    # Methods

    def respond(self, query=None):
        '''accepts input from the parent parent and responds by
            returning the appropriate data'''

        # Choose the appropriate method and get new data
        if query == 'back' or query == 'fwd' or query == 'rst':
            self.level = self.mgr.navshistory[self.mgr.historypoint][1]
            self.query = None

        elif query == 'update':
            self.query = None
            if self.level < 0: self.level += 1 # hand first pass update

            # For SizeNavigator only: perform some pre-processing
            self.preprocess()

        else:
            self.level += 1
            query = self.labelmap[query]
            self.queryhistory[self.level] = query # Pls remove the other one (in updatemgr) not this one
            self.query = query

            # check the local raw data and select the data for this query
            selection = self.getselection(query)

            # for SizeNavigator only: perform some pre-processing
            self.preprocess()

            # Pass the selection to the datamanager for iteration
            self.mgr.iteriselection(selection, 2) # 2 = SizeNavigator's call-sign

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
            smin, smax = self.limits[self.level][0], self.limits[self.level][1]
        else:
            query = self.queryhistory[self.level]
            smin, smax = self.processQuery(query)
            self.limits[self.level] = (smin, smax)

        smax += 10 #Hack to ensure biggest file falls into the mix

        # Create the bins with size ranges
        bincount = 10.00
        binsize = (smax - smin)/bincount
        low = smin
        self.bindata = OrderedDict({}) # captures the number of files per bin
        self.binlimits = OrderedDict({}) # holds the upper size limit for each bin

        for bin in range(int(bincount)):
            high = low + binsize
            label = '%f-%f' %(low, high)
            self.binlimits[label] = high
            low = high

        # Reiterate and get the no of files per bin
        self.newraw = self.binlimits.copy() # raw data for use in next level
        self.bindata = self.binlimits.copy()
        for bin in self.newraw: self.newraw[bin] = [] # empty the copy
        for bin in self.bindata: self.bindata[bin] = 0 # empty the copy

    def processfile(self, dfile):
        size = dfile[6]
        for hbin in self.binlimits:
            if size <= self.binlimits[hbin]:
                self.newraw[hbin].append(dfile)
                break   # sue me

    def postprocess(self):
        for hbin in self.newraw:
            self.bindata[hbin] = len(self.newraw[hbin])

        # Convert the labels and save a mapping
        data = self.processDataQueries(self.bindata)

        # Label processing before calling the visualizer
        for item in self.queryhistory:
            query = self.queryhistory[item]
            if item == 0: query = 'All'
            else: query = self.convertQuery(query)
            tag = 'Size Range'
            self.labels[item] = [tag, query]

        self.refreshWindows(data, self.level, self.labels)

    def convertQuery(self, query):
        query = query.split('-')
        low, high = float(query[0]), float(query[1])
        hunit, lunit = 'b', 'b'
        temp = [(1073741824,'Gb'), (1048576,'Mb'), (1024,'Kb')]
        sizes = OrderedDict(temp)

        for item in sizes:
            if high > item and hunit == 'b':
                high = high/item
                hunit = sizes[item]
            if low > item and lunit =='b':
                low = low/item
                lunit = sizes[item]

        low, high = round(low,2), round(high,2)
        return '> '+str(low)+lunit+'\n to \n'+str(high)+hunit

    def processQuery(self, query):
        query = query.split('-')
        low, high = float(query[0]), float(query[1])

        return (low, high)

    def processDataQueries(self, data):
        self.labelmap = OrderedDict({})
        newdata = OrderedDict({})
        for label in data:
            newlabel = self.convertQuery(label)
            self.labelmap[newlabel] = label

        for label in self.labelmap:
            datum = data[self.labelmap[label]]
            newdata[label] = datum
        return newdata

    def refreshWindows(self, data, level, labels):
        self.mgr.sbook.spanel.win.reload(data, level, labels)

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
            self.limits.pop(item)

        self.mgr.historypoint += 1
        curr = self.mgr.historypoint
        prev = curr - 1

        # update the manager's query history here
        dquery, squery, tquery = self.mgr.navsqueryhistory[prev]
        squery = query
        self.mgr.navsqueryhistory[curr] = (dquery, squery, tquery)

        self.selectionhistory[self.mgr.historypoint] = selection[0:]
        self.mgr.sizequeryhist.append(query)
        self.queryhistory[self.level] = query

    def initializevars(self, mgr):
        self.query = 0
        self.type = 's'
        self.queryhistory = {0:'All'}
        self.raw = {0:mgr.master[0:]}
        self.selectionhistory = mgr.selectionhistory
        self.level = -1
        self.mgr = mgr
        self.labels = {}
        self.limits = {}

        selection = self.raw[0]
        smax, smin = selection[0][6], selection[0][6]
        for dfile in selection:
            size = dfile[6]
            if size > smax:
                smax = size
            elif size < smin:
                smin = size

        self.limits[0] = (smin, smax)

# ---------------------------------------------------------------------------
