import sqlite3, os

def dbconnect(txtDbName):
    conn = sqlite3.connect(txtDbName)
    cur = conn.cursor()
    return conn, cur

def dbclose(conn, cur):
    conn.commit()           # Save (commit) the changes
    cur.close()                 # Close the cursor if you're are done with it
    conn.close()                # Close the database
    return

def dropTables(tableNames, cursor):
    for table in tableNames:
        try:
            cursor.execute('drop table %s' %table)
            print 'Dropped %s' %table
        except:
            pass
    return

def cleanLine(word):
    # This is a comment
    word = word.strip("\n").lower()
    if len(word.split()) > 1: return False # No spaces allowed
    if len(word.split('.')) > 1: return False # No dots allowed
    if len(word.split('-')) > 1: return False # No hyphens allowed
    #if len(word.split('\'')) > 1 or len(word.split('"')) > 1: return False # No inverted quotes allowed
    if word.isalpha(): return word # No numbers allowed
    return False

def clearStopWords(cur):
    file = open('StopWords.txt', 'r')
    result = cur.execute('select count (*) from dictionary')
    print 'Before stopwords: ', result.fetchall()
    for word in file:
        word = word.strip("\n")
        cur.execute('delete from dictionary where word="%s"' %word)

    result = cur.execute('select count (*) from dictionary')
    print 'After stopwords: ', result.fetchall()
    file.close()
    return

def createDict(cur):
    cur.execute('create table dictionary (wordID integer primary key, word text)')
    rawdict = open('Dictionary.txt', 'r')
    count = 0
    for line in rawdict:
        clean = cleanLine(line)
        count += 1
        if clean: cur.execute('insert into dictionary(word) values("%s")' %clean)
        #if clean: print 'clean'
    rawdict.close()
    print count
    return

try: dbclose(conn, cur)
except: pass
dbName = 'MyDict.db'
conn, cur = dbconnect(dbName)
tableNames = ['dictionary']
dropTables(tableNames, cur)
createDict(cur)
conn.commit()
clearStopWords(cur)
conn.commit()


