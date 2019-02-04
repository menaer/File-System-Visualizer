import time, sqlite3, calendar
from UserDict import DictMixin
from ordereddict import OrderedDict

# ---------------------------------------------------------------------------

class DBManager(object):

    def __init__(self, name):
        # Initialize variables and create the db/file connection:
        self.conn = sqlite3.connect(name) # update later to check if db exists
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

        # Get a raw list of all files in the selected harddisk
        result = self.cur.execute('select * from Files;')
        self.master = result.fetchall()
        self.selectionhistory = {}
        #self.raw = {0:self.master[0:]}

# ---------------------------------------------------------------------------

class dateNavMgr(object):
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
            self.query = None
            self.raw = self.selectionhistory[self.level]

        elif query == 'fwd':
            if self.level < 3: self.level += 1
            self.query = None
            self.raw = self.selectionhistory[self.level]

        elif query == 'rst':
            self.level = 0
            self.query = None
            self.raw = self.selectionhistory[self.level]

        else:
            self.level += 1
            self.query = query

        data = self.getData(self.level, self.raw, self.query)
        self.refreshWindows(data, self.level)

    def refreshWindows(self, data, level):
        selection = self.selectionhistory[level]
        query = self.queryhistory[level]
        print query
        self.parent.subbook.subbook.dpanel.win.reload(data, self.level)

        print 'DateNavigator: No of files = %d' %len(selection)
        self.parent.resultwin.reload(selection)

    def getData(self, level, raw, query=None):
        if level == 0: data = self.getlvl0data(raw, query)
        elif level == 1: data = self.getlvl1data(raw, query)
        elif level == 2: data = self.getlvl2data(raw, query)
        elif level == 3: data = self.getlvl3data(raw, query)
        elif level == 4: data = self.getlvl4data(raw, query)
        return data

    def updateRaw(self, newraw):
        self.raw = newraw.copy()
        del newraw

    def getlvl0data(self, raw, query=None):
        '''Level zero presents each year with total file sizes
            raw data for this method should be the master list of files'''

        if query != None:
            selection = raw[query]
            # save the raw data for this level for reverse navigation
            self.selectionhistory[self.level] = selection[0:]
            self.queryhistory[self.level] = query
        else:
            selection = raw

        # Iterate through the master list and group files by year
        newraw = OrderedDict({})
        print len(selection), type(selection)
        for file in selection:
            year = file[5]
            try: newraw[year].append(file)
            except: newraw[year] = [file]

        # Get an empty copy of the years for that data dictionary
        data = newraw.copy()
        for year in data: data[year] = 0
        temp = data.items()
        temp.sort()
        temp.reverse()
        data = OrderedDict(temp)

        # Iterate through the raw list and group the data by year
        for pair in newraw.iteritems():
            year = pair[0]
            files = pair[1]
            for file in files:
                data[year] += file[4]

        # Save the raw that level 1 will use to sort itself out
        self.updateRaw(newraw)
        return data

    def getlvl1data(self, raw, query=None):
        '''Level one presents each month with total file sizes
             raw data for this method should be a list of files for each year'''

        if query != None:
            query = int(query)
            selection = raw[query]

            # save the raw data and query for this level for reverse navigation
            self.selectionhistory[self.level] = selection[0:]
            self.queryhistory[self.level] = query
        else:
            selection = raw

        data = OrderedDict([('Jan', 0), ('Feb', 0), ('Mar',0),
                            ('Apr',0), ('May',0), ('Jun',0),
                            ('Jul',0), ('Aug',0), ('Sep',0),
                            ('Oct',0), ('Nov',0), ('Dec',0)])

        newraw =  OrderedDict([('Jan', []), ('Feb', []), ('Mar',[]),
                            ('Apr',[]), ('May',[]), ('Jun',[]),
                            ('Jul',[]), ('Aug',[]), ('Sep',[]),
                            ('Oct',[]), ('Nov',[]), ('Dec',[])])
        for file in selection:
            month = file[6]
            data[month] += file[4] # increment the size
            newraw[month].append(file) # Append the file to its month in the new rawdata


        # Save the raw that level 2 will use to sort itself out
        self.updateRaw(newraw)
        return data

    def getlvl2data(self, raw, query=None):
        '''Level two presents each week in a month with total file sizes
            raw data for this method should be a list of files for each month'''

        if query != None:
            selection = raw[query]

            # save the raw data for this level for reverse navigation
            self.selectionhistory[self.level] = selection[0:]
            self.queryhistory[self.level] = query
            year = self.queryhistory[self.level-1]
        else:
            selection = raw
            query = self.queryhistory[self.level]
            year =  self.queryhistory[self.level-1]


        monthkey = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,
                    'May':5, 'Jun':6, 'Jul':7, 'Aug':8,
                    'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

        month = monthkey[query]
        data, newraw = {}, OrderedDict({})

        # get a 'list' of weeks in the month (each week is a list of days !!)
        weeks = calendar.monthcalendar(year, month)
        for i in range(len(weeks)):
            data[i+1] = 0 # initalize the week:size dictionary
            newraw[i+1] = []

        # match the days to each week above and group the sizes
        for file in selection:
            day = file[7]
            size = file[4]
            for week in weeks:
                if week.__contains__(day):
                    data[weeks.index(week)+1] += size
                    newraw[weeks.index(week)+1].append(file)
        newraw[98] = year
        newraw[99] = month

        # Save the raw that level 3 will use to sort itself out
        self.updateRaw(newraw)
        return data

    def getlvl3data(self, raw, query=None):
        '''Level three presents each day in a week with total file sizes.
            raw data for this method should be a list of files for the week'''

        if query != None:
            query = int(query) # hack, investigate if you've got time
            selection = raw[query]

            # save the raw data for this level for reverse navigation
            self.selectionhistory[self.level] = selection[0:]
            self.queryhistory[self.level] = query

        else:
            selection = raw
            query = self.queryhistory[self.level]

        # Need month key one more time
        monthkey = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,
                'May':5, 'Jun':6, 'Jul':7, 'Aug':8,
                'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        year, month =  self.queryhistory[self.level-2],  self.queryhistory[self.level-1]
        month = monthkey[month]

        calmonth = calendar.monthcalendar(year, month)
        week = calmonth[query-1][0:] # slice it just to be on the safe side
        days = {}
        data = {}
        # get the weeks in the month

        for i in range(len(week)):
            data[week[i]] = 0 # initalize the day:size dictionary

        # match the days to each week above and group the sizes
        for file in selection:
            day1 = file[7]
            size = file[4]
            for day in week:
                if day1 == day:
                    data[day] += size

        # Save the raw that level 2 will use to sort itself out
        #self.updateRaw(newraw)
        return data

    def getlvl4data(self, raw, query):
        pass

    def initializevars(self, data, parentwin):
        self.query = 0
        self.queryhistory = {}
        self.raw = {0:data[0:]}
        self.selectionhistory = {}
        self.level = -1
        self.parent = parentwin

# ---------------------------------------------------------------------------

class sizeNavMgr(object):
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
            self.raw = self.mgr.selectionhistory[self.level]

        elif query == 'fwd':
            if self.level < len(self.queryhistory)-1: self.level += 1
            self.query = self.queryhistory[self.level]
            self.raw = self.mgr.selectionhistory[self.level]

        else:
            self.level += 1
            self.queryhistory[self.level] = query
            for item in self.queryhistory:
                if item > self.level: self.queryhistory.pop(item)
            self.query = query

        data = self.getData(self.level, self.raw, self.query)
        self.refreshWindows(data, self.level)
        return data

    def refreshWindows(self, data, level):
        raw = self.selectionhistory[level]
        print '\n\n'
        print self.queryhistory
        query = self.queryhistory[level]
        selection = raw[query]

        self.parent.subbook.subbook.spanel.win.reload(data, self.level)
        print 'SizeNavigator: No of files = %d' %len(selection)
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
        if len(selection) <= 1:
            #print 'Length of selection is:', len(selection)
            #print 'Selection data is:', selection
            # Can't go further - Rollback
            print 'Cannot go further.... Please select another range'
            pop = self.queryhistory.pop(self.level)
            print 'Popped %s. History now: %s' %(str(pop), str(self.queryhistory))

            self.level -= 1
            self.query = self.queryhistory[self.level]
            raw = self.selectionhistory[self.level]
            selection = raw[self.query]

        # Iterate through the master list and get max/min sizes
        newraw = OrderedDict({})
        smax, smin = selection[0][4], selection[0][4]

        for file in selection:
            size = file[4]
            if size > smax:
                smax = size
            elif size < smin:
                smin = size

        smax += 10 #Hack to ensure biggest file falls into the mix
        #print 'Length of selection is:', len(selection)
        #if self.level > 0: print 'Selection data is:', selection
        #print 'Min = %f, Max = %f' %(smin, smax), '\n\n'

        # Create the bins with size ranges
        bincount = 15.00
        binsize = (smax - smin)/bincount
        low = smin
        bindata = OrderedDict({}) # captures the number of files per bin
        binlimits = OrderedDict({}) # holds the upper size limit for each bin

        for bin in range(int(bincount)):
            high = low + binsize
            label = '%f-%f' %(low, high)
            binlimits[label] = high
            low = high

        # Reiterate and get the no of files per bin
        newraw = binlimits.copy() # raw data for use in next level
        bindata = binlimits.copy()
        for bin in newraw: newraw[bin] = [] # empty the copy
        for bin in bindata: bindata[bin] = 0 # empty the copy

        #print 'Binlimits: %s' %str(binlimits)
        for file in selection:
            size = file[4]
            for bin in binlimits:
                if size <= binlimits[bin]:
                    newraw[bin].append(file)
                    bindata[bin] += 1
                    break   # sue me


        # Iterate through the raw list and group the data by year
        data = bindata.copy()

        # save the raw data for this level for reverse navigation
        self.selectionhistory[self.level] = raw.copy()

        # Save the raw that level 1 will use to sort itself out
        self.updateRaw(newraw)
        #print '\n\nData for this run: ,', data
        return data

    def initializevars(self, data, parentwin):
        self.query = 0
        self.queryhistory = {}
        self.raw = {0:data[0:]}
        self.selectionhistory = {}
        self.level = -1
        self.parent = parentwin

# ---------------------------------------------------------------------------

if __name__ == '__main__':
    fltstart = float(time.clock())
    mgr = DBManager('Magee.db')
    dwin = dateNavMgr(None, mgr)
    fltfinish = float(time.clock())
    print('Completed in %f seconds') %(fltfinish - fltstart)
    raw_input('Press enter to exit::')