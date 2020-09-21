import sys
from pathlib import PurePosixPath, Path
import re

'''
Establishing file paths, open files
'''
mymdPath = PurePosixPath(Path.cwd() / sys.argv[1])
mymd = open(mymdPath, "r")

# Slice the directory where the mymd file is located.
mymdDir = mymdPath.parent
# Slice the file name
name = mymdPath.name

askingPath = "/home/addem/Desktop/asking"

template = open(Path(askingPath + "/html/notes/noteTemplate.html"), "r")

html = open(dir / (name[:-4] + ".html"), "w")

'''
Write the HTML top matter
'''

def relativeTOabsolutePATH(line):
    '''
    Replaces any hrefs with absolute paths identified above.
    '''
    # for every href
    for match in re.findall('href="(.+?)"', line):
        print(line[:10])
        # the address it should have is relative to the folder holding the mymd
        addy = Path.resolve(mymdDir / match[6:-1]))
        line.replace(match, addy)
    return line

# Lines 1 to 11 copy over
for i in range(10):
    line = relativeTOabsolutePATH(template.readline())
    html.write(line)
# Line 12 insert title
mymdLine = mymd.readline()
if not (mymdLine[:8] == 'Title - '):
    print("\nTitle not formatted properly.  It should look like 'Title - ...'")
htmlLine = '    <title>' + mymdLine[8:] + '</title>'
html.write(htmlLine)
template.readline()
# lines 13 to 63
for i in range(51):
    line = relativeTOabsolutePATH(template.readline())
    html.write(line)

'''
Process the mymd
'''
while

'''
Close it up!
'''
template.close()
html.close()
mymd.close()
