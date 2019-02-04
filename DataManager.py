from UserDict import DictMixin
from ordereddict import OrderedDict
from SizeNavigator import sizeNavMgr
from DateNavigator import dateNavMgr
from TypeNavigator import typeNavMgr
import sqlite3, time, calendar, wx, gc

# ---------------------------------------------------------------------------

class DBManager(object):

    def __init__(self, parent, name):
        # Initialize variables and create the db/file connection:
        self.parent = parent
        self.conn = sqlite3.connect(name) # update later to check if db exists
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

        # Get a raw list of all files in the selected harddisk
        result = self.cur.execute('select * from Files;')
        self.master = result.fetchall()
        self.initvars()
        self.createnavs()

        '''# note: panel names are:
        ---------------------------------------
        mgr.srchpanel = search window
        mgr.rstpanel = results window
        mgr.mpanel = main window
        mgr.dspanel = datesize window
        mgr.mdlpanel = middle window
        mgr.sbook = notebook in middle window'''

    def createnavs(self):
        self.snav = sizeNavMgr(mgr=self)
        self.dnav = dateNavMgr(mgr=self)
        self.tnav = typeNavMgr(mgr=self)

    def updatenavs(self, caller, msg=''):
        navs = {1:'DateNavigator', 2:'SizeNavigator', 3:'TypeNavigator', 4:'Back', 5:'Forward'}
        queries = {1:self.dnav.query,2:self.snav.query,3:0}

        if caller == 1: # request from dnav
            self.snav.respond('update')
            self.tnav.respond('update')
            self.navshistory[self.historypoint] = [self.dnav.level, self.snav.level, self.tnav.level]

        elif caller == 2: # request from snav
            self.tnav.respond('update')
            self.dnav.respond('update') # always call dnav last to be on the safe side
            self.navshistory[self.historypoint] = [self.dnav.level, self.snav.level, self.tnav.level]

        elif caller == 3: # request from tnav
            self.snav.respond('update')
            self.dnav.respond('update') # always call dnav last to be on the safe side
            self.navshistory[self.historypoint] = [self.dnav.level, self.snav.level, self.tnav.level]

        elif caller == 4:
            print '\nDataManager: recieved a back command'
            if self.historypoint > 0: self.historypoint -= 1
            self.snav.respond('back')
            self.tnav.respond('back')
            self.dnav.respond('back') # always call dnav last to be on the safe side

        elif caller == 5:
            print '\nDataManager: recieved a forward command'
            if self.historypoint < len(self.selectionhistory)- 1: self.historypoint += 1
            self.snav.respond('fwd')
            self.tnav.respond('fwd')
            self.dnav.respond('fwd') # always call dnav last to be on the safe side

        elif caller == 6:
            print '\nDataManager: recieved a reset command'
            if self.historypoint > 0: self.historypoint = 0
            self.searchstring = None
            self.snav.respond('rst')
            self.tnav.respond('rst')
            self.dnav.respond('rst') # always call dnav last to be on the safe side
            self.sbook.SetSelection(0)

        elif caller == 7:
            self.searchstring = msg.lower()
            if len(self.searchstring.strip(' ')) == 0:
                self.searchstring = None

            print '\nDataManager: recieved a search string', msg
            self.snav.respond('update')
            self.tnav.respond('update')
            self.dnav.respond('update') # always call dnav last to be on the safe side
        else:
            print 'Error: All update requests were skipped...'

        print 'DataManager: Navs History = ', self.navshistory
        print 'DataManager: Navs Query History = ', self.navsqueryhistory
        print 'DataManager: Current levels = ', self.dnav.level, self.snav.level, self.tnav.level
        print 'DataManager: History Point = ', self.historypoint

    def updateresults(self, selection, occurrences=None):
            self.rstpanel.reload(selection, occurrences)
            self.sbar.SetStatusText("   No of files: %d" %len(selection))
            # update the sidebar
            dlabel = str(self.dnav.queryhistory[self.dnav.level])
            if dlabel == '0': dlabel = 'All'
            slabel = str(self.snav.queryhistory[self.snav.level])
            tlabel = str(self.tnav.queryhistory[self.tnav.level])
            klabel = self.searchstring
            self.mdlpanel.sidebar.dlabel.SetLabel(dlabel)
            self.mdlpanel.sidebar.slabel.SetLabel(slabel)
            self.mdlpanel.sidebar.tlabel.SetLabel(tlabel)
            if self.searchstring: self.mdlpanel.sidebar.klabel.SetLabel(klabel)
            else: self.mdlpanel.sidebar.klabel.SetLabel('None')

    def iteriselection(self, selection, caller, msg=''):
        selection = selection[0:]
        # Check if there are any keywords and then reduce the selection during the iteration
        fltstart = float(time.clock())

        # call the other navigators to get ready for newrawdata
        self.updatenavs(caller, msg)
        fltfinish = float(time.clock())
        print ('UpdateNavs completed in %f seconds') %(fltfinish - fltstart)

        # Add a command here to call vizwin's draw 'loading viz' method
        # Add the loading viz method near crosshairs
        # Iterate thru the selection an call each navigator to do their bit
        fltstart = float(time.clock())
        myCursor= wx.StockCursor(wx.CURSOR_WATCH)
        self.parent.SetCursor(myCursor)

        dprocess = self.dnav.processfile
        sprocess = self.snav.processfile
        tprocess = self.tnav.processfile
        for dfile in selection:
            dprocess(dfile)
            sprocess(dfile)
            tprocess(dfile)

        fltfinish = float(time.clock())
        print ('Iterations completed in %f seconds') %(fltfinish - fltstart)
        myCursor= wx.StockCursor(wx.CURSOR_ARROW)
        self.parent.SetCursor(myCursor)

        fltstart = float(time.clock())
        self.dnav.updateRaw()
        self.snav.updateRaw()
        self.tnav.updateRaw()

        self.applyfilters()

        self.dnav.postprocess()
        self.snav.postprocess()
        self.tnav.postprocess()

        fltfinish = float(time.clock())
        print ('Post-processing completed in %f seconds') %(fltfinish - fltstart)

    def applyfilters(self):
        print 'Datamanager; Applying filters.....', self.searchstring
        if self.searchstring:
            keywords = self.searchstring.split(' ')

            # Filter DateNavigator's newraw
            raw = self.dnav.newraw.copy()
            results = []
            occurrences = []
            low = str.lower
            for key in raw:
                newselection = []
                selection = raw[key]
                for dfile in selection:
                    name = dfile[2]
                    lower = low(name)
                    occurs = 0
                    contains = False
                    for term in keywords:
                        try:
                            if term in lower:
                                occurs += 1
                                contains = True
                        except:
                            pass
                    if contains:
                        occurrences.append(occurs)
                        results.append(dfile)
                        newselection.append(dfile)
                raw[key] = newselection[0:]
            self.dnav.newraw = raw

            # Filter SizeNavigator's newraw
            raw = self.snav.newraw.copy()
            for key in raw:
                newselection = []
                selection = raw[key]
                for dfile in selection:
                    name = dfile[2]
                    lower = low(name)
                    contains = False
                    for term in keywords:
                        try:
                            if term in lower:
                                contains = True
                        except:
                            pass
                    if contains:
                        newselection.append(file)
                raw[key] = newselection[0:]
            self.snav.newraw = raw

            # Filter TypeNavigator's newraw
            raw = self.tnav.newraw.copy()
            for key in raw:
                newselection = []
                selection = raw[key]
                for dfile in selection:
                    name = dfile[2]
                    lower = low(name)
                    contains = False
                    for term in keywords:
                        try:
                            if term in lower:
                                contains = True
                        except:
                            pass
                    if contains:
                        newselection.append(file)
                raw[key] = newselection[0:]
            self.tnav.newraw = raw

            # Send the new filtered results (obtained fron dnav) to the list window
            self.updateresults(results, occurrences)

        else:
            occurrences = None
            selection = self.selectionhistory[self.historypoint]
            self.updateresults(selection, occurrences)

    def initvars(self):
        self.raw = {0:self.master[0:]}
        self.datequeryhist = []
        self.sizequeryhist = []
        self.typequeryhist = []
        self.historypoint = -1
        self.selectionhistory = {}
        self.navshistory = {0:[0,0,0]}
        self.navsqueryhistory = {0:[0,0,0]}
        self.searchstring = None
# ---------------------------------------------------------------------------


