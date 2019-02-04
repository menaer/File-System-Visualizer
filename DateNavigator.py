from UserDict import DictMixin
from ordereddict import OrderedDict
import calendar, wx

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
            self.level = self.mgr.navshistory[self.mgr.historypoint][0]
            self.query = None

        elif query == 'update':
            if self.level < 0: self.level += 1 # handle first pass update
            self.query = None

            # prepare global newraw shell for mgr iteration to populate
            self.preprocess()
            return

        else:
            self.level += 1
            self.query = query

        if self.level <= 3:
            # prepare global newraw shell for mgr iteration to populate
            self.preprocess()

            # check the local raw data and select the data for this query
            selection = self.getselection(self.query)

            # Pass the selection to the datamanager for iteration
            self.mgr.iteriselection(selection, 1) # 1 = DateNavigator's call-sign
        else:
            # Roll back because I only want up to level 1
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
            self.newraw = OrderedDict({})

        elif self.level == 1:
            if self.query: self.query = int(self.query)
            self.data = OrderedDict([('Jan', 0), ('Feb', 0), ('Mar',0),
                                ('Apr',0), ('May',0), ('Jun',0),
                                ('Jul',0), ('Aug',0), ('Sep',0),
                                ('Oct',0), ('Nov',0), ('Dec',0)])

            self.newraw =  OrderedDict([('Jan', []), ('Feb', []), ('Mar',[]),
                                ('Apr',[]), ('May',[]), ('Jun',[]),
                                ('Jul',[]), ('Aug',[]), ('Sep',[]),
                                ('Oct',[]), ('Nov',[]), ('Dec',[])])

        elif self.level == 2:
            if self.query: key = self.query
            else: key = self.queryhistory[self.level]
            year = self.queryhistory[self.level-1]
            monthkeys = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,
                        'May':5, 'Jun':6, 'Jul':7, 'Aug':8,
                        'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

            month = monthkeys[key]
            self.data, self.newraw = OrderedDict({}), OrderedDict({})

            # get a 'list' of weeks in the month (each week is a list of days !!)
            self.weeks = calendar.monthcalendar(year, month)
            for i in range(len(self.weeks)):
                self.data[i+1] = 0 # initalize the week:no_of_files dictionary
                self.newraw[i+1] = [] # initalize the week:no_of_files dictionary

        elif self.level == 3:
            if self.query: self.query = query = int(self.query)
            else: query = self.queryhistory[self.level]

            # Need month key one more time
            monthkey = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,
                    'May':5, 'Jun':6, 'Jul':7, 'Aug':8,
                    'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
            year, month =  self.queryhistory[self.level-2],  self.queryhistory[self.level-1]
            month = monthkey[month]

            calmonth = calendar.monthcalendar(year, month)
            self.week = calmonth[query-1][0:] # slice it just to be on the safe side
            self.data = OrderedDict({})
            self.newraw = OrderedDict({})

            # get the weeks in the month
            for i in range(len(self.week)):
                self.data[self.week[i]] = 0 # initalize the day:size dictionary
                self.newraw[self.week[i]] = []

        elif self.level == 4:
            print 'End of the line Boss !!!'
            if self.query:
                self.level -= 1
                self.query = None

            # Empty the outputs of level 3
            for i in range(len(self.week)):
                self.data[self.week[i]] = 0 # initalize the day:size dictionary
                self.newraw[self.week[i]] = []

        else:
            print 'DateNavigator: Error in preprocess ...'

    def processfile(self, dfile):
        if self.level == 0:
            year = dfile[7]
            try: self.newraw[year].append(dfile)
            except: self.newraw[year] = [dfile]

        elif self.level == 1:
            month = dfile[8]
            self.newraw[month].append(dfile) # Append the file to its month in the new rawdata

        elif self.level == 2:
            day = dfile[9]
            for week in self.weeks:
                if week.__contains__(day):
                    self.newraw[self.weeks.index(week) + 1].append(dfile)

        elif self.level == 3:
            day1 = dfile[9]
            for day in self.week:
                if day1 == day:
                    self.newraw[day].append(dfile)

        elif self.level == 4: data = self.getlvl4data(query)

    def postprocess(self):
        if self.level == 0:
            # Get an empty copy of the years for the data dictionary
            self.data = self.newraw.copy()
            for year in self.data:
                self.data[year] = 0 # enpty the copyto get shell for data
            temp = self.data.items() # extract key value pairs in a list of tuples
            temp.sort() # sort the extract
            temp.reverse() # reverse the sorted extract
            self.data = OrderedDict(temp) # recreate a dictionary using the new sorted key-value pairs list

            # Iterate through the raw list and group the data by year
            for year in self.newraw:
                self.data[year] = len(self.newraw[year]) # i.e. no_of-files

        elif self.level == 1:
            for month in self.data:
                self.data[month] = len(self.newraw[month]) # i.e. no_of-files

        elif self.level == 2:
            for week in self.data:
                self.data[week] = len(self.newraw[week]) # i.e. no_of-files

        elif self.level == 3:
            for day in self.data:
                self.data[day] = len(self.newraw[day]) # i.e. no_of_files
        else:
            pass

        # Label processing before calling the visualizer
        for item in self.queryhistory:
            if item == 0: query = 'All'
            else: query = str(self.queryhistory[item])
            tag = self.leveltags[item]
            self.labels[item] = [tag, query]

        self.refreshWindows(self.data, self.level, self.labels)

    def refreshWindows(self, data, level, labels):
        self.mgr.sbook.dpanel.win.reload(data, level, labels)

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
        if curr: prev = curr - 1
        else: prev = curr

        self.mgr.datequeryhist.append(query)
        self.queryhistory[self.level] = query
        self.selectionhistory[self.mgr.historypoint] = selection[0:]

        # update the manager's query history here
        dquery, squery, tquery = self.mgr.navsqueryhistory[prev]
        dquery = []
        for item in self.queryhistory:
             step = self.queryhistory[item]
             dquery.append(step)

        self.mgr.navsqueryhistory[curr] = (dquery, squery, tquery)

    def initializevars(self, mgr):
        self.query = 0
        self.type = 'd'
        self.queryhistory = {}
        self.raw = {0:mgr.master[0:]}
        self.selectionhistory = mgr.selectionhistory
        self.level = -1
        self.mgr = mgr
        self.leveltags = ['Date Modified', 'Year', 'Month', 'Week', 'Day', 'Hour']
        self.labels = {}

# ---------------------------------------------------------------------------
