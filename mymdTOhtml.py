import sys
from pathlib import PurePosixPath, Path
import re

### Description ###
# This processes a mymd file, which is a .txt file containing my own markup
# which gets translated to HTML.

### Dexcription of mymd ###
# A mymd file is meant to represent notes from a chapter of a textbook.
# It always starts with:
# Title - Author Name - What Goes in <title> tags.
# and then
# * Chapter Number
# * Chapter Title
# and then sections contained in zoom buttons, which themselves can contain
# other zooms which may be subsections, definitions, theorems, exercises, and
# so on.  Sectioning is done entirely by the {{Buton Title} Button content.}
# notation.  Sections semantically tagged, for instance if a section is a
# definition then it can be written
# {{Definition of a *partition*}#def A *partition* is a ...}
# and tags can be stacked.
# {{How do you generalize the ...}#theorem#exercise One way is to ...}
# Inside of any curly braces, text is processed so that *b* transoforms to
# bold, **i** transforms to italics.

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
def process_markup(text):
    # Turn bold and italics marks to HTML
    

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
        remaining_text = line[end_index_of_stars+1:]
        remaining_text = process_markup(remaining_text)
        htmlLine += remaining_text + "</h" + str(n) + ">"
    else: # If there are no stars, somehting went wrong.
        raise("process_header applied to a line that doesn't start with *")

def process_button(section, context):
    # A section is a string of all the text inside a button environment.
    # The context is a list indicating the location, in the sense of a tree
    # with children and siblings, etc.  It is mostly for an id naming scheme.
    out = '<div class="zoomInterface">\n<button aria-expanded="false" class="zoomButton" id="' + ".".join(context) +

    curly_1_index = re.search("{", section).span[1]
    curly_2_index = re.search("{", section[curly_1_index+1:]).span[1]

    for line in section.split("\n"):
        if "}" in line:

    return "process_button TODO\n"

mymdLine = mymd_file.readline()
instance_counter = 0
chapter_counter = 0
new_chapter = true
while mymdLine:
    if (len(mymdLine) == 0 || mymdLine.isspace()):
        html_file.write("<br>")
    else:
        if mymdLine[0] == "*":
            if new_chapter:
                chapter += 1
                new_chapter = false
            html_file.write(process_header(mymdLine))
        elif mymdLine[0:2] == "{{":
            new_chapter = true
            instance_counter += 1
            section = ""
            level_counter = 0
            while level_counter > 0:
                level_counter += len(re.findall("{", mymdLine)) \
                              - len(re.findall("}", mymdLine))
                section += mymdLine + "\n"
                mymdLine = mymd.readline()
            html_file.write(process_button(section, [chapter_counter,instance_counter]))
    mymdLine = mymd.readline()






'''
Close it up!
'''
template_file.close()
html_file.close()
mymd_file.close()
