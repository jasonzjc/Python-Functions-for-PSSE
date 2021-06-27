# -*- coding: utf-8 -*-
# -------------------------------------------------- #
#  Jeff Zhao
#  10/31/2017
#
#  A simple example script to perform both a flat start and
#  a dynamic simulation
#
#  To run from Python 
#
#  Requires Python 2.7 and PSS�E 33 
#      -or- Python 2.5 and PSS�E 32 
# -------------------------------------------------- #

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
# configure the solver
psspy.fnsl(
	options1 = 0,
	options5 = 0
)
# sikve the power flow case
iVal = psspy.solved()
if iVal == 0:
	print "Met convergence tolerance"
elif iVal == 1:
    print "The iteration limit exceeded"
elif iVal > 1:
    print "Blown up or others"

# ------------------------------------------------- #	
# Dynamic Simulation
# Convert gen & load
# convert generators
ierr = psspy.cong(0)

# convert load
for i in [1,2,3]:
    ierr = psspy.conl(0, 1, i, [0, 0], [100, 0, 0, 100])[0]

# save converted case
psspy.save(r'{0}\savnw_C.sav'.format(example_path))

# Load dynamics
ierr = psspy.dyre_new([_i, _i, _i, _i], dyr_case, _s, _s, _s)



# Set output channels
psspy.chsb(sid = 0, all = 1, status = [-1, -1, -1, 1, 12, 0])
#

# Save snapshot
psspy.snap(sfile = r'{0}\PythonDynTest.snp'.format(example_path))

# Initialize and run the dynamic scenario
psspy.strt(option = 0, outfile = out_file)
psspy.run(0,1,0,0,0)

# 3-phase fault on bus 151 (default bus fault is a 3phase and there is no bus 151)
psspy.dist_bus_fault(ibus = 151)

# Run to 3 cycles
time = 3.0/60.0
psspy.run(0,1+time,0,0,0)

# Clear fault (assuming only part of bus faults)
psspy.dist_clear_fault()
psspy.dist_branch_trip(ibus = 151, jbus = 201, id = '1')

# Run to 10 seconds
time = 10
psspy.run(0,time,0,0,0)

# Export channel data to Excel
dyntools.CHNF.xlsout(dyntools.CHNF(out_file), 
                     channels = '', 
                     show = 'True',
                     xlsfile = 'out.xls',
                     sheet = '',
                     overwritesheet = True)