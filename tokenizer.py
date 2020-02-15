import re
import string
# import matplotlib.pyplot as plt
"""
# CS446 Assignment 1: Tokenizer
# Evan Liu 02/02/2020
# Tokenizes the contents of a text file
"""
#------------------------------------------------------------------
# Tokenizer function
#------------------------------------------------------------------
def tokenize(filename):
    stopfilename = "stopwords.txt"
    
    # Read stop words into set from file
    stopfile = open(stopfilename, "r")
    stopset = set()
    for line in stopfile:
        stopset.add(line.strip())
    stopfile.close()

    # Read file into string for tokenization
    myfile = open(filename, "r")
    filestring = myfile.read().lower()
    myfile.close()

    # Regex patterns
    acronymRegex = r'(?<!\w)([a-z])\.'
    puncReplaceRegex = r'[\W_]'

    # STEP 1 - ACRONYMS, ABBREVIATIONS AND PUNCTUATION
    # Clean acronyms (a.c.r.o.n.y.m. -> acronym)
    filestring = re.sub(acronymRegex, r'\1', filestring)
    # Remove apostrophes
    filestring = re.sub('\'', '', filestring)
    # Replace punctuation with whitespace
    filestring = re.sub(puncReplaceRegex, ' ', filestring)
    # Split strings on whitespace to words
    rawWords = filestring.split()

    # STEP 2 - STOPWORDS
    # Change any stopwords to empty string
    newWords = [w for w in rawWords if w not in stopset]
    """
    OLD VERSION
    # Remove empty strings from word list
    index = 0
    while len(words) > index:
        if len(words[index]) == 0:
            words.pop(index)
        else:
            index = index + 1
    """
    
    # Word Set and Graph Data
    graph = dict()
    t = 0
    wordSet = set()
    for w in newWords:
        if w not in wordSet:
            wordSet.add(w)
        graph[t] = len(wordSet)
        t += 1

    # STEP 3 - PORTER STEMMING (See porter_stem() function for process)
    # Stemming words using function porter_stem(word)
    for i in range(0, len(newWords)):
        newWords[i] = porter_stem(newWords[i])

    # Word Set
    stemWordSet = set()
    for w in newWords:
        if w not in stemWordSet:
            stemWordSet.add(w)
            
    # Word count using dictionary
    wordCount = dict()
    for w in newWords:
        wordCount[w] = wordCount.get(w, 0) + 1

    """
    newWords - words after stop word removal
    wordSet - Set of all words before stemming
    stemWordSet - Set of all words after stemming
    wordCount - Dict of words and frequencies
    graph - a dictionary defining vocabulary growth
    """
    
    return newWords, wordSet, stemWordSet, wordCount, graph
#------------------------------------------------------------------
# Porter Stemming Function
#------------------------------------------------------------------
def porter_stem(w):
    vowels = 'aeiou'
    #--------------------------------------------------------------
    # Step 1A
    #--------------------------------------------------------------
    # Replace sses by ss (e.g., stresses → stress).
    if len(w) >= 4 and w[-4:] == 'sses':
        #print(w, "->", w[:-2])
        return w[:-2]
    #--------------------------------------------------------------
    # Delete s if the preceding word part contains a vowel not immediately before the s (e.g., gaps → gap but gas → gas).
    elif len(w) >= 3 and w[-1] == 's' and w[-2] != 's' and w[-2] not in vowels and w[-3] in vowels:
        #print(w, "->", w[:-1])
        return w[:-1]
    #--------------------------------------------------------------
    # Replace ied or ies by i if preceded by more than one letter, otherwise by ie (e.g., ties → tie, cries → cri).
    elif len(w) >= 3 and (w[-3:] == 'ied' or w[-3:] == 'ies'):
        if len(w[:-3]) > 1:
            #print(w, "->", w[:-2])
            return w[:-2]
        else:
            #print(w, "->", w[:-1])
            return w[:-1]
    #--------------------------------------------------------------
    # If suffix is us or ss do nothing (e.g., stress → stress).
    elif len(w) >= 2 and (w[-2:] == 'us' or w[-2:] == 'ss'):
        #print(w, "unchanged")
        return w
    #--------------------------------------------------------------
    # Step 1B
    #--------------------------------------------------------------
    # Replace eed, eedly by ee if it is in the part of the word after the first nonvowel following a vowel (e.g., agreed → agree, feed → feed).
    elif len(w) >= 4 and w[-3:] == 'eed':
        if w[-4] not in vowels:
            for c in w[:-4]:
                if c in vowels:
                    #print(w, "->", w[:-1])
                    return w[:-1]
        else:
            return w
        
    elif len(w) >= 6 and w[-5:] == 'eedly':
        if w[-6] not in vowels:
            for c in w[:-6]:
                if c in vowels:
                    #print(w, "->", w[:-3])
                    return w[:-3]
        else:
            return w
    #--------------------------------------------------------------
    # Delete ed, edly, ing, ingly if the preceding word part contains a vowel, and
    # then if the word ends in at, bl, or iz add e (e.g., fished → fish, pirating →
    # pirate), or if the word ends with a double letter that is not ll,ss, or zz, remove
    # the last letter (e.g., falling → fall, dripping → drip), or if the word is short, add
    # e (e.g., hoping → hope).
    
    # Ends in 'ed'
    elif (len(w) >= 3 and w[-2:] == 'ed'):
        # Root word is the word minus 'ed'
        root = w[:-2]
        if len(root) >= 2:
            # If root word ends in 'at', 'bl', or 'iz'
            if root[-2:] == 'at' or root[-2:] == 'bl' or root[-2:] == 'iz':
                # Add 'e'
                return root + 'e'
            # If root ends with two of the same letter that aren't 'll', 'ss', or 'zz'
            elif root[-2] == root[-1] and root[-2:] != 'll' and root[-2:] != 'ss' and root[-2:] != 'zz':
                # Delete the last letter
                # print(w, "->", root, "->", root[:-1])
                return root[:-1]
            else:
                return root
    # Ends in 'edly'
    elif len(w) >=5 and w[-4:] == 'edly':
        # Root word is the word minus 'edly'
        root = w[:-4]
        if len(root) >= 2:
            # If root word ends in 'at', 'bl', or 'iz'
            if root[-2:] == 'at' or root[-2:] == 'bl' or root[-2:] == 'iz':
                # Add 'e'
                return root + 'e'
            # If root ends with two of the same letter that aren't 'll', 'ss', or 'zz'
            elif root[-2] == root[-1] and root[-2:] != 'll' and root[-2:] != 'ss' and root[-2:] != 'zz':
                # Delete the last letter
                # print(w, "->", root, "->", root[:-1])
                return root[:-1]
            else:
                return root
    # Ends in 'ing'
    elif len(w) >=4 and w[-3:] == 'ing':
        # Root word is the word minus 'ing'
        root = w[:-3]
        if len(root) >= 2:
            # If root word ends in 'at', 'bl', or 'iz'
            if root[-2:] == 'at' or root[-2:] == 'bl' or root[-2:] == 'iz':
                # Add 'e'
                return root + 'e'
            # If root ends with two of the same letter that aren't 'll', 'ss', or 'zz'
            elif root[-2] == root[-1] and root[-2:] != 'll' and root[-2:] != 'ss' and root[-2:] != 'zz':
                # Delete the last letter
                # print(w, "->", root, "->", root[:-1])
                return root[:-1]
            else:
                return root
    # Ends in 'ingly'
    elif len(w) >= 6 and w[-5:] == 'ingly':
        # Root word is the word minus 'ingly'
        root = w[:-5]
        if len(root) >= 2:
            # If root word ends in 'at', 'bl', or 'iz'
            if root[-2:] == 'at' or root[-2:] == 'bl' or root[-2:] == 'iz':
                # Add 'e'
                return root + 'e'
            # If root ends with two of the same letter that aren't 'll', 'ss', or 'zz'
            elif root[-2] == root[-1] and root[-2:] != 'll' and root[-2:] != 'ss' and root[-2:] != 'zz':
                # Delete the last letter
                # print(w, "->", root, "->", root[:-1])
                return root[:-1]
            else:
                return root
    return w
#------------------------------------------------------------------

###################################################################
# MAIN
###################################################################
#------------------------------------------------------------------
# Part A Output: One term per line
#------------------------------------------------------------------
input_name_a = "tokenization-input-part-A.txt"
words, wordSet, stemWordSet, wordCount, graph = tokenize(input_name_a)

file_a = open("tokenized.txt", "w")
for w in words:
    file_a.write(w + '\n')
file_a.close()

#------------------------------------------------------------------
# Part B Output: Terms and Frequencies
#------------------------------------------------------------------
input_name_b = "tokenization-input-part-B.txt"
words, wordSet, stemWordSet, wordCount, graph = tokenize(input_name_b)

# Dictionary for top words
top200 = dict()
# While less than 200 words added
while len(top200) < 200:
    # Max value of word frequency
    value = max(wordCount.values())
    # Key(s) of max value
    keys = [key for key, v in wordCount.items() if v == value]
    
    # For all keys of max value (in case there's more than one)
    # Add them to top200, while popping them from wordCount
    # Increment x
    for k in keys:
        top200[k] = wordCount.get(k)
        wordCount.pop(k)

file_b = open("terms.txt", "w")
for k in top200:
    line = k + " " + str(top200.get(k))
    file_b.write(line + '\n')
file_b.close()

"""
# GRAPHING
x = []
y = []

for i in range(0, len(graph)):
    x.append(i)
    y.append(graph.get(i))

plt.plot(x, y)
plt.show()
"""
