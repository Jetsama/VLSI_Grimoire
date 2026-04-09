


# types of codeblocks
# System Verilog
# Python?
# Javascript
# schematic


# types of exports
# html
# html + js
# pdf
# 
import os

def build_book():
    """ 
    Go through entire repository, creating book in output directory
    given the format requested.
    """

    d = '.'
    folders = [os.path.join(d, o) for o in os.listdir(
        d) if os.path.isdir(os.path.join(d, o))]
    
    folders.sort() #TODO more modular sorting/organization?
    
    for folder in folders:
        # create a page per README.md?
        if os.path.isfile(folder + '/README.md'):
            with open(folder + '/README.md', "r") as originalMarkdown:
                fileString = originalMarkdown.read()
                
        pass
    pass

def build_page():

    pass
# for folder in folders:
#     if os.path.isfile(folder + '/README.md'):


if __name__ == "__main__":
    build_book()