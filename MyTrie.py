import sqlite3
#
# Class for the node of a tree
#
class TreeNode(object):

    __slots__ = ('nodes', 'children', 'values', 'level') # The attributes this class can have


    def __init__(self):

        # The entry point for this level in the tree
        self.nodes = {}

        # the children of the node
        self.children = {}

        # the values stored in the node
        self.values = []

        # The current level in the tree
        #self.level = level # also doubles as index point in word



    ''' Methods'''
    def insert(self, elements, word):
        ''' Inserts a word into the tree'''
        index = 0
        letter = elements[index]
        elements.pop(index)

        try:
            node = self.nodes[letter] # the check

            if elements:
                node.insert(elements, word)
            else:
                # nothing left to insert. Must be a sub word.
                # therefore, add to values if not already there
                try: node.values.index(word)
                except: node.values.append(word)

        except:
            # create the child node
            node = TreeNode()

            # Insert remaining elements (if any) into the child
            if elements:
                node.insert(elements, word)
            else:
                # end of the line
                # add the word to that child's value list
                node.values.append(word)

            # Add the child to the parent (i.e. this instance)
            self.nodes[letter] = node

        return


#
# Class for a tree.
#
class Tree:

    def __init__(self):

        #self.startlevel = 0
        self.root = TreeNode() # Root is an empty node

    # Insert a word into the tree
    # Everybody must insert from the root node

    def insert(self, word):
        # add the root character to the word
        elements = list(word)
        self.root.insert(elements, word)

    def retrieve(self, elements):

        root = self.root

        for letter in elements:
            nodes = root.nodes
            values = root.values
            print nodes, values
            #root = root.nodes[letter]
            try: root = root.nodes[letter]
            except KeyError:
                print 'Error of the line at %s index position %d', letter, elements.index(letter)

        # Get the last item
        nodes = root.nodes
        values = root.values
        print nodes, values


def dosegment(word, t):
    values = []
    word = word.lower()
    root = t.root
    neword = word

    for letter in word:
        try:
            root = root.nodes[letter]
            value = root.values
            if value: values.append(value[0])
        except KeyError:
            print 'Key error for letter %s at index %d' %(letter, word.find(letter))
            if values:
                index = len(values[-1])
                segment = word[index:]
            else:
                segment = neword
            print 'New segment created:', segment
            extra = dosegment(segment, t)
            print extra
            for item in extra: values.append(item)
            break
        neword = neword[1:]
    return values

def dbconnect(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    return conn, cur


if (__name__ == "__main__"):

    # Delete the tree if it is already in memory
    try: del t
    except: pass


    dbname = 'MyDict.db'
    conn, cur = dbconnect(dbname)

    t = Tree()

    result = cur.execute('select word from dictionary')
    dictionary = result.fetchall()

    for word in dictionary:
        t.insert(word[0].lower())

    cur.close()
    conn.close()

    values = dosegment('cream_ybunny', t)
    print values
