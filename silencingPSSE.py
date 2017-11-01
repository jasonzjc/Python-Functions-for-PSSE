# -*- coding: utf-8 -*-
# -------------------------------------------------- #
#  Jeff Zhao
#  11/01/3017
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
        yield
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
    dyr_case = r'{0}\savnw.dyr'.format(example_path)
    out_file = r'{0}\example.out'.format(example_path)  # Edit as desired

    # -------------------------------------------------- #
    pssbin_path = bin_path

    # Call up PSS/E from Python
    import sys, os
    sys.path.append(pssbin_path)
    os.environ['PATH'] = (pssbin_path + ';' + os.environ['PATH'])
    import psspy, redirect, dyntools, pssplot

    # silence all outputs
    with silence():
      psspy.psseinit(10000)

    # redirect output into the log file
    import redirect
    redirect.psse2py()

    psse_log = open('psse_logfile.log', 'w')
    with silence(psse_log):
      psspy.psseinit(10000)

    # writing to file-like object
    import StringIO
    stdout = StringIO.StringIO()
    with silence(stdout):
        psspy.save('2013-system-normal.sav')

    print "This isn't redirected"

    # retrieving the output from the StringIO object.
    print stdout.getvalue()
