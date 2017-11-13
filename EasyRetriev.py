# -*- coding: utf-8 -*-
    # -------------------------------------------------- #
    #  Jeff Zhao
    #  11/10/3017
    #
    #  A simple example script to perform both a flat start and
    #  a dynamic simulation
    #
    #  folked from http://www.whit.com.au/blog/2011/08/designing-easier-subsystem-data/
    #
    #  To run from Python
    #
    #  Requires Python 2.7 and PSS�E 33
    #      -or- Python 2.5 and PSS�E 32
    # -------------------------------------------------- #

import itertools
import operator
import psspy

def subsystem_info(name, attributes, sid=-1, inservice=True):
    """
    Return the requested attributes from PSSE subsystem for the
    given subsystem id (sid) and subsystem element name.

    e.g. to retrieve bus attributes "NAME", "NUMBER" and "PU"

        subsystem_info('bus', ["NAME", "NUMBER", "PU"], -1, True)

    'bus','NAME', 'NUMBER', etc. are predefined by PSSE sybsytem API

    sid is the subsystem id. -1 is the default value and means all elemens are
    selected

    inservicemeans list only information for service lements if set to True (default)
    """

    name = name.lower()
    gettypes = getattr(psspy, 'a%stypes' % name)
    apilookup = {
            'I': getattr(psspy, 'a%sint' % name),
            'R': getattr(psspy, 'a%sreal' % name),
            'X': getattr(psspy, 'a%scplx' % name),
            'C': getattr(psspy, 'a%schar' % name),
    }

    result = []
    attr_types = operator.itemgetter(0)

    ierr, attr_types = gettypes(attributes)

    for k, group in itertools.groupby(zip(attr_types,attributes), lambda x: x[0]):
        func = apilookup[k]
        strings = list(zip(*group)[1])
        irr, res = func(sid, flag=1 if inservice else 2, string=strings)
        result.extend(res)

    return zip(*result)

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

    # Import PSS/E default
    _i = psspy.getdefaultint()
    _f = psspy.getdefaultreal()
    _s = psspy.getdefaultchar()
    redirect.psse2py()

    # -------------------------------------------------- #
    # initiate
    psspy.psseinit(2000)	# 2000 bus at most, this number can be changed
    # Load and solve the powerflow case
    psspy.case(sav_case)

    # -------------------------------------------------- #
    # the way PSSE provided to retrieve system information
    ierr, busnumbers = psspy.abusint(sid=-1, string="NUMBER")
    ierr, busnames = psspy.abuschar(sid=-1, string="NAME")
    print zip(busnumbers[0],busnames[0])
    busindex = busnumbers[0].index(3001)
    name = busnames[0][busindex]
    print '3001:', name

    # -------------------------------------------------- #
    # show how the subsystem_info function work
    businfo = subsystem_info('bus', ['NUMBER', 'TYPE', 'NAME', 'PU', 'SHUNTACT'])
    print businfo
