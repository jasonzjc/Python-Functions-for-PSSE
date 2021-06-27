# -*- coding: utf-8 -*-
# -------------------------------------------------- #
#  Jeff Zhao
#  11/01/2017
#
#  turn off the output of PSS/E or redirect it to a log file or an object
#
#  Originally from http://www.whit.com.au/blog/2012/03/silencing-psse-output/
#  and https://psspy.org/psse-help-forum/question/93/silencing-psse-stdout/
#
#  To run from Python
#
#  Requires Python 2.7 and PSS�E 33
#      -or- Python 2.5 and PSS�E 32
# -------------------------------------------------- #

from __future__ import with_statement
from contextlib import contextmanager
import sys
import os

# the contextmanager helps to automatically close the file opened by the open function after when you exit the scope
@contextmanager
def silence(file_object=None):
    """
    Discard stdout (i.e. write to null device) or
    optionally write to given file-like object.
    """
    if file_object is None:
        file_object = open(os.devnull, 'w')
    # save the original sys.stdout
    old_stdout = sys.stdout
    try:
        # set sys.stdout to a new value
        sys.stdout = file_object
        # halt the function at this point and the tasks n the with statement operates
        yield file_object
    finally:
        # reassigns the original sys.stdout
        sys.stdout = old_stdout

if __name__ == '__main__':
    # Directory paths - adjust these to match your installation - check doc_path for API info
    psse_version = 33
    # r' means python raw string, in which backslash is backslash
    doc_path = r'C:\Program Files (x86)\PTI\PSSE{0}\DOCS'.format(psse_version)
    bin_path = r'C:\Program Files (x86)\PTI\PSSE{0}\PSSBIN'.format(psse_version)
    example_path = r'C:\Users\jzhao27\Google Drive\SoftwareProjects\PSSE\Practice\PracPython'   # Edit as desired

    # File paths
    sav_case = r'{0}\savnw.sav'.format(example_path)

    # -------------------------------------------------- #
    pssbin_path = bin_path

    # Call up PSS/E from Python
    sys.path.append(pssbin_path)
    os.environ['PATH'] = (pssbin_path + ';' + os.environ['PATH'])
    import psspy, redirect, dyntools, pssplot

	# it's very important to redirect PSS/E to Python
	# if not, stdout will e captured for everything exceept PSS/E
    import redirect
    redirect.psse2py()
	
	# Silence Type
	# 0. silence all outputs
	# 1. silence all outputs but restore them in a log file
	# 2. silence all output and put them in a StringIO object, release them as required
    SilenceType = 0
    if SilenceType == 0:
	
        # silence all outputs
        print "Choose Silence Type 0: silence all outputs\n"
        with silence():
            psspy.psseinit(10000)
	        # Load and solve the powerflow case
            ierr = psspy.case(sav_case)
            iVal = psspy.solved()

    elif SilenceType == 1:
	
        # redirect output into the log file
        print "Choose Silence Type 1: silence all outputs and restore them in 'psse_logfile.log'\n"
        psse_log = open('psse_logfile.log', 'w')
        with silence(psse_log):
          psspy.psseinit(10000)
	      # Load and solve the powerflow case
          ierr = psspy.case(sav_case)
          iVal = psspy.solved()

    elif SilenceType == 2:
	
        # writing to file-like object
        print "Choose Silence Type 2: silence all outputs and restore them in a StringIO object. Print out the outputs later.\n"
        import StringIO
        stdout = StringIO.StringIO()
        with silence(stdout):
          psspy.psseinit(10000)
          # Load and solve the powerflow case
          ierr = psspy.case(sav_case)
          iVal = psspy.solved()

        print "Program finished. Up to now there should be no output printed yet.\n"
        raw_input("Press Enter to print the outputs: \n")

        # retrieving the output from the StringIO object.
        print stdout.getvalue()