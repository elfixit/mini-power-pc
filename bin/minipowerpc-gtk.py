
import sys, os
try:
    from minipowerpc.gui import GUI
except:
    sys.path.append(os.path.abspath('../.'))
    from minipowerpc.gui import GUI

# If this is run stand alone execute the following after the 'if'
# If this class is imported into another program the code after the 'if' will
# not run. This makes the code more flexible.
if __name__ == "__main__":
    gui = GUI() # create an instance of our class

