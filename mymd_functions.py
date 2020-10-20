import re

def relativeTOabsolutePATH(line, mymdDir):
    '''
    Replaces any hrefs that have relative paths with hrefs that use absolute paths.  The line is a single line of HTML text (possibly containing tags
    which are not yet closed).  The mymdDir is a pathlib Path object,
    representing the path to the mymd file.
    '''
    # for every href
    for match in re.findall('href="(.+?)"', line):
        # the address it should have is relative to the folder holding the mymd
        addy = mymdDir / match[6:]
        line.replace(match, str(addy))
    return line

def process_header(line):
    '''
    The header of any mymd file is located after the title information, and is
    marked by a line starting with a *.  Multiple lines can be marked in
    sequence but after the first section zoom, everything that follows must be
    the content of the page and not a header.  The header is intended to be the highest level text header at the top of the page, usually a chapter number and title.  The line is a string of such text.
    '''
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

def process_markup(section):
    '''
    A section is a string of markdown text with line-break characters separating lines.  Processing this involves (1) turning *example text* into
    italics "example text", (2) turning **example text** into bold "example
    text", and (3) turning line-breaks into <br><br>.
    '''
    # Find all double-star matches first.  These are not immediately
    # preceeded by a non-whitespace character.  After any potential white
    # space a bold environment is inaugurated by "**" followed by zero or more
    # non-stars, followed by two stars, matched as small as possible.  For the
    # replacement, the first pair of double-stars is replaced by "<b>" and the
    # second pair by "</b>".
    double_star_pattern = "((\s|\A)+\*\*(!\*)*\*\*)?"
    replace_pattern = "\1<b>\4</b>"
    test_text = "Here's some **text to bold**."

    return re.sub(double_star_pattern, replace_pattern, test_text)

print(process_markup(""))
