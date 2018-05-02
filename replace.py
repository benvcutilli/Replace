import re
from subprocess import check_output
from sys import argv

# This file replaces the in-text keys from InText [2]. Please look at
# that reference for citations. The following regular expression is from there
# (although I typed it from memory), so see letter (C) in its intext.py for
# information about it.
r = re.compile("\^\^\^([a-z]+)\^\^\^")

# The following regular expression is just for the JSON files described by
# point (A) in intext.py; this is for the keys in "intextcitations" and
# "referenceorder":
s = re.compile('"([a-z]+)"')

# n holds the new keys, which will be generated from [2]'s
# tagcreator.py
n = {}

# This does the replacement of the key in all files, including [2]'s
# JSON file ((A) in intext.py), and the code after the loop (up to "STOP"
# indicator) replaces the keys for the array "referenceorder" and
# "intextcitations" object in that same JSON file.

# Path to tagcreator.py from [2]:
p = "tagcreator.py"
def newtag(capture):
    c = capture.group(1)
    if c not in n:
        # Calling [2]'s tagcreator.py in order to get a new key to swap
        # in for the old key. These keys are used in tags and keys, respectively
        # discussed in [2]'s intext.py's (C) and (A).
        n[c] = check_output(["python", p], universal_newlines=True).strip()
    return "^^^" + n[c] + "^^^"

def newkey(capture):
    c = capture.group(1)
    # OK: if c not in n:
        # Calling [2]'s tagcreator.py in order to get a new key to swap
        # in for the old key. These keys are used in tags and keys, respectively
        # discussed in [2]'s intext.py's (C) and (A).
        # OK: n[c] = check_output(["python", p], universal_newlines=True).strip()
    if c in n:
        return '"' + n[c] + '"'
    else:
        return '"' + c + '"'

for filename in argv[1:]:
    oldFile = open(filename)
    newFile = open("m" + filename, "w")
    # Switching the keys in a file that is meant to be put through
    # intext.py [2]
    newFile.write( r.sub(newtag, oldFile.read()) )
    newFile.close()
    oldFile.close()

oldFile = open("m"+argv[1])
# The JSON file from (A) of intext.py [2] needs to have replaced the
# keys in the object "intextcitations" and array "referenceorder" with the keys
# we created (or a new key if the key hadn't been encountered before)
j = s.sub(newkey, oldFile.read())
oldFile.close()
newFile = open("m"+argv[1], "w")
newFile.write(j)
newFile.close()

pairsFile = open("pairs", "w")
for k in n:
    pairsFile.write(k + " " + n[k] + "\n")
pairsFile.close()

################### STOP ###################
