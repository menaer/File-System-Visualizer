import os, fnmatch, sqlite3, time
fltstart = float(time.clock())

def fnRunTests():

    print ('Running database tests')
    conn = sqlite3.connect('InvIndex.db')
    conn.text_factory = str
    cur = conn.cursor()
    #cur.execute('PRAGMA synchronous=NORMAL')

    result = cur.execute('select * from Files;')
    master = result.fetchall()

    #conn.close()
    return master, conn, cur


# ==================================================================
# Remember google query : 'using python to navigate filesystem'
# ==================================================================
result, conn, cur = fnRunTests()
fltfinish = float(time.clock())
print ('Completed in %f seconds') %(fltfinish - fltstart)