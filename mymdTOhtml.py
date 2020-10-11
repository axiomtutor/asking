import sys
from pathlib import PurePosixPath, Path
import re

'''
Establishing file paths, open files
'''
mymdPath = PurePosixPath(Path.cwd() / sys.argv[1])
mymd_file = open(mymdPath, "r")

# Slice the directory where the mymd file is located.
mymdDir = mymdPath.parent
# Slice the file name
name = mymdPath.name

askingPath = "/home/addem/Desktop/asking"

template_file = open(Path(askingPath + "/html/notes/noteTemplate.html"), "r")

html_file = open(mymdDir / (name[:-4] + ".html"), "w")

'''
Write the HTML top matter
'''

def relativeTOabsolutePATH(line):
    '''
    Replaces any hrefs with absolute paths identified above.
    '''
    # for every href
    for match in re.findall('href="(.+?)"', line):
        # the address it should have is relative to the folder holding the mymd
        addy = mymdDir / match[6:]
        line.replace(match, str(addy))
    return line

# Lines 1 to 11 of the template copy over
for i in range(10):
    line = relativeTOabsolutePATH(template_file.readline())
    html_file.write(line)
# Line 12 insert title
mymdLine = mymd_file.readline()
if not (mymdLine[:8] == 'Title - '):
    print("\nTitle not formatted properly.  It should look like 'Title - ...'")
htmlLine = '    <title>' + mymdLine[8:] + '</title>'
html_file.write(htmlLine)
template_file.readline()
# lines 13 to 63 copy
for i in range(51):
    print(i)
    line = relativeTOabsolutePATH(template_file.readline())
    html_file.write(line)

'''
Process the mymd
'''
def process_header(line):
    # Number of stars indicates level of header.
    if line[0] == "*":
        htmlLine = "<h"
        if line[1] == "*":
            if line[2] == "*":
                if line[3] == "*":
                    n = 4
                else:
                    n = 3
            else:
                n = 2
        else:
            n = 1
        htmlLine += str(n)+">"
        # Now put everything else in the file, and close header.
        end_index_of_stars = re.search('*+').span[1]
        htmlLine += line[end_index_of_stars+1:]+) + "</h" + str(n) + ">"
    else: # If there are no stars, somehting went wrong.
        raise("process_header applied to a line that doesn't start with *")

def process_button(section):
    # A section is a string of all the text inside a button environment.
    return "process_botton TODO\n"

mymdLine = mymd_file.readline()
while mymdLine:
    if (len(mymdLine) == 0 || mymdLine.isspace()):
        html_file.write("<br>")
    else:
        if mymdLine[0] == "*":
            html_file.write(process_header(mymdLine))
        elif mymdLine[0:2] == "{{":
            section = ""
            level_counter = 0
            while level_counter > 0:
                level_counter += len(re.findall("{", mymdLine)) \
                              - len(re.findall("}", mymdLine))
                section += mymdLine + "\n"
                mymdLine = mymd.readline()
            html_file.write(process_button(section))






'''
Close it up!
'''
template_file.close()
html_file.close()
mymd_file.close()
