

def dosegment(word, t):
    values = []
    word = word.lower()
    root = t.root

    for letter in word:
        try:
            root = root.nodes[letter]
            value = root.values
            if value: values.append(value[0])
        except KeyError:
            index = len(values[-1])
            segment = word[index:]
            print 'Key error for letter %s at index %d' %(letter, word.find(letter))
            print 'New segment created:', segment
            extra = dosegment(segment, t)
            print extra
            for item in extra: values.append(item)
            break

    return values