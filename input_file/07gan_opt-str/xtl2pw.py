#!/usr/local/bin/python3
import sys,math

# xtl2pw.py
# made by mkanzaki@me.com
# last update: 2016 01/01
# converted to Python3 by 2to3 2019/06/29
# This code reads an xtl file produced from Vesta, which contains 
# crystal structure data, and writes an input file for pw.x (Quantum-ESPRESSO). The xtl file can be obtained using "fractional coordinate" option for "Export data ..." in Vesta.  
# Usage:
# > ./xtl2pw.py test.xtl vc-relax 1
# first argument is .xtl file name 
# second argument is calulation method: 
# one of followings: "scf" or "vc-relax" or "relax"
# third argument is whether use constraints for atomic positons or not
# 1 to apply constraint; 0 to not. 
#
# .in file produced is not ready to go input file for pw.x.
# You need to modify and check following points for your own runs
#  1) calculation method correct?
#  2) Directories correct? Or change below.
#       pseudopotential directory
psdir = '../pseudo'
#       data directory
outdir = './'
#       wfc directory
wfcdir = './'
#  3) ibarv correct? (P is selected as default)
#  4) celldm() correct?
#  5) ntyp correct?
#  6) ecutwfc & ecutrho should be changed by time-saving vs accuracy consideration
#  7) you may need to read UPF file for adequate ecut parameters
#  8) conv_thr should be changed for your need
#  9) pressure should be changed (kbar unit)
#  10) press_conv_thr should be changed 
#  11) Add cell_dofree = '' if you want to constrain cell shape 
#  12) Atomic species correct?
#  13) You need to choose your favarite pseudopotentials
#  14) or change pseudopotential file name (ps[i]) 
#  15) if they use common name, change "pseudo" below.
pseudo = 'pbesol-n-kjpaw_psl.0.1.UPF'
# change below according to your pseudo directory
#  16) Finally, check K_POINTS, and change them.
#  17) Starting with ! is comment line
#  For atomic species, heavier atoms than Ba are not in  
#   listed in the program. You can add atoms
#   in if - elif block below.
# 

cell = [0.0 for i in range(6)]
#matrix = [[0.0 for j in range(6)] for i in range(6)]
lines = ['' for i in range(500)]
atom = ['' for i in range(500)]
x = [0.0 for i in range(500)]
y = [0.0 for i in range(500)]
z = [0.0 for i in range(500)]
kind = ['' for i in range(20)]
wt = [0.0 for i in range(20)]
ps = ['' for i in range(20)]
tmp = ['' for i in range(1000)]
# reading xtl file
if len(sys.argv) < 4:
	print('Not enough arguments provided!')
	print('For example: > ./xtl2pw.py test.xtl vc-relax 1')
	print('1 for constraints, 0 for no constraints.')
	print('Three arguments are necessary.')
	print('Read header of this code for details.')
	exit()
try:
	file1 = open(sys.argv[1],'r')
except IOError as xxx_todo_changeme:
	(errno, msg) = xxx_todo_changeme.args
	print('xtl file open error!')
	exit()
# read second and third arguments
#print sys.argv[1]
cal = sys.argv[2]
constraint = sys.argv[3]
base = sys.argv[1].replace('.xtl','')
f2 = base + '.in'
file2 = open(f2,'w')

rd = math.pi/180.0
bohr = 0.5291772108

# Get title
title = file1.readline()
#print title
# find CELL line
while True:
	ftext = file1.readline()
	if 'CELL' in ftext :
		break
# Extract cell parameters
ftext = file1.readline()
ftext = ftext.strip()
list = ftext.split(' ')
while list.count('') > 0:
	list.remove('')
for i in range(0,6):
	cell[i] = float(list[i])

# calculate celldm() for input file
celldm2 = cell[1]/cell[0]
celldm3 = cell[2]/cell[0]
celldm1 = cell[0]/bohr
celldm4 = math.cos(cell[3]*rd)
celldm5 = math.cos(cell[4]*rd)
celldm6 = math.cos(cell[5]*rd)

# find CELL line
while True:
	ftext = file1.readline()
	if 'NAME' in ftext :
		break

# read atomic positions 
i = 1
while True:
	lines[i] = file1.readline()
	if 'EOF' in lines[i] :
		break
	else:
		atom[i] = lines[i][0:2].strip(' ')
		tmp = lines[i].strip()
		tmp = tmp.split(' ')
		while tmp.count('') > 0:
			tmp.remove('')
		if tmp[1]=='-0.000000':
			tmp[1]='0.000000'
		if tmp[2]=='-0.000000':
			tmp[2]='0.000000'
		if tmp[3]=='-0.000000':
			tmp[3]='0.000000'
		x[i] = float(tmp[1])
		if (x[i] >= 1.0) or (x[i] < 0.0):
			x[i] = x[i] - math.floor(x[i])
		y[i] = float(tmp[2])
		if (y[i] >= 1.0) or (y[i] < 0.0):
			y[i] = y[i] - math.floor(y[i])
		z[i] = float(tmp[3])
		if (z[i] >= 1.0) or (z[i] < 0.0):
			z[i] = z[i] - math.floor(z[i])
		flag = 0
		for j in range(1,i):
			if i != j:
				if (abs(x[i]-x[j]) < 0.001) and (abs(y[i]-y[j]) < 0.001) and (abs(z[i]-z[j]) < 0.001):	
					flag = 1
		if flag == 0:
			i = i + 1
max = i
print("Number of atoms in unit cell:",max-1) 
# check number of atom types
kind[0] = atom[1]
k = 1
for i in range(1,max):
	match = 0
	for j in range(0,k):
		if atom[i] == kind[j]:				
			match = 1
	if match == 0:
		k = k + 1
		kind[k-1] = atom[i]
natom = k
# atomic weight (better to use external file)
for i in range(0,natom):
	if kind[i] == 'H':
		wt[i] = 1.008
		ps[i] = 'H.pbesol-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'He':
		wt[i] = 4.003
		ps[i] = 'He.pbesol-kjpaw_psl.1.0.0.UPF'
	elif kind[i] == 'Li':
		wt[i] = 6.941
		ps[i] = 'Li.pbesol-s-kjpaw_psl.1.0.0.UPF'
	elif kind[i] == 'Be':
		wt[i] = 9.012
		ps[i] = 'Be.pbesol-n-kjpaw_psl.0.2.UPF'
	elif kind[i] == 'B':
		wt[i] = 10.811
		ps[i] = 'B.pbesol-n-kjpaw_psl.1.0.0.UPF'
	elif kind[i] == 'C':
		wt[i] = 12.011
		ps[i] = 'C.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'N':
		wt[i] = 14.007
		ps[i] = 'N.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'O':
		wt[i] = 15.999
		ps[i] = 'O.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'F':
		wt[i] = 18.998
		ps[i] = 'F.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'Ne':
		wt[i] = 20.180
		ps[i] = 'Ne.pbesol-n-kjpaw_psl.1.0.0.UPF'
	elif kind[i] == 'Na':
		wt[i] = 22.990
		ps[i] = 'Na.pbesol-spn-kjpaw_psl.1.0.0.UPF'
	elif kind[i] == 'Mg':
		wt[i] = 24.305
		ps[i] = 'Mg.pbesol-n-kjpaw_psl.0.3.0.UPF'
	elif kind[i] == 'Al':
		wt[i] = 26.982
		ps[i] = 'Al.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'Si':
		wt[i] = 28.086
		ps[i] = 'Si.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'P':
		wt[i] = 30.974
		ps[i] = 'P.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'S':
		wt[i] = 32.065
		ps[i] = 'S.pbesol-n-kjpaw_psl.0.1.UPF'
	elif kind[i] == 'Cl':
		wt[i] = 35.453
		ps[i] = 'Cl.pbesol-n-kjpaw_psl.0.3.0.UPF'
	elif kind[i] == 'Ar':
		wt[i] = 39.948
		ps[i] = ''
	elif kind[i] == 'K':
		wt[i] = 39.0983
		ps[i] = ''
	elif kind[i] == 'Ca':
		wt[i] = 40.078
		ps[i] = 'Ca.pbesol-spn-kjpaw_psl.0.2.3.UPF'
	elif kind[i] == 'Sc':
		wt[i] = 44.956
		ps[i] = ''
	elif kind[i] == 'Ti':
		wt[i] = 47.867
		ps[i] = 'Ti.pbesol-spn-kjpaw_psl.0.3.1.UPF'
	elif kind[i] == 'V':
		wt[i] = 50.942
		ps[i] = ''
	elif kind[i] == 'Cr':
		wt[i] = 51.996
		ps[i] = ''
	elif kind[i] == 'Mn':
		wt[i] = 54.938
	elif kind[i] == 'Fe':
		wt[i] = 55.845
		ps[i] = ''
	elif kind[i] == 'Co':
		wt[i] = 58.933
		ps[i] = ''
	elif kind[i] == 'Ni':
		wt[i] = 58.693
		ps[i] = ''
	elif kind[i] == 'Cu':
		wt[i] = 63.546
		ps[i] = ''
	elif kind[i] == 'Zn':
		wt[i] = 65.380
		ps[i] = 'Zn.pbesol-dn-kjpaw_psl.0.2.2.UPF'
	elif kind[i] == 'Ga':
		wt[i] = 69.723
		ps[i] = ''
	elif kind[i] == 'Ge':
		wt[i] = 72.640
		ps[i] = ''
	elif kind[i] == 'As':
		wt[i] = 74.922
		ps[i] = ''
	elif kind[i] == 'Se':
		wt[i] = 78.960
		ps[i] = ''
	elif kind[i] == 'Br':
		wt[i] = 79.904
		ps[i] = 'Br.pbesol-dn-kjpaw_psl.0.3.1.UPF'
	elif kind[i] == 'Kr':
		wt[i] = 83.798
		ps[i] = ''
	elif kind[i] == 'Rb':
		wt[i] = 85.468
		ps[i] = ''
	elif kind[i] == 'Sr':
		wt[i] = 87.620
		ps[i] = ''
	elif kind[i] == 'I':
		wt[i] = 126.9045
		ps[i] = 'I.pbesol-n-kjpaw_psl.0.2.UPF'
	elif kind[i] == 'Xe':
		wt[i] = 131.293
		ps[i] = ''
	elif kind[i] == 'Cs':
		wt[i] = 132.901
		ps[i] = ''
	elif kind[i] == 'Ba':
		wt[i] = 137.327
		ps[i] = ''
# add depending on your needs
	else:
		print("Not in default data. You need to add it")
		wt[i] = 10.000
		ps[i] = ''
# write .in file template
file2.write("&control\n")
file2.write("    calculation='" + cal + "' ,\n")
file2.write("    restart_mode='from_scratch' ,\n")
file2.write("    prefix='" + base + "' ,\n")
# change below according to your out directory
file2.write("    outdir = '" + outdir + base + "/' ,\n")
# change below according to your wfc directory
file2.write("    wfcdir = '" + wfcdir + base + "/' ,\n")
# change below according to your pseudo directory
file2.write("    pseudo_dir = '" + psdir + "' ,\n")
file2.write("    disk_io='default' ,\n")
file2.write("    forc_conv_thr= 0.001 ,\n")
file2.write("    verbosity = 'high' ,\n")
file2.write("    nstep = 200 ,\n")
file2.write(' /\n')
file2.write(' &system\n')
if cell[0]==cell[1] and cell[0]==cell[2] and cell[3]==90.0 and cell[4]==90.0 and cell[5]==90.0:
	# cubic ibrav could be 1 or 2 or 3
	file2.write('    ' + 'ibrav= 1 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' \n')
elif cell[0]==cell[1] and cell[0]==cell[2] and cell[3]!=90.0 and cell[3]==cell[4] and cell[3]==cell[5]:
	# trigonal ibrav = 5
	file2.write('    ' + 'ibrav= 5 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(4) = ' + str('%01.8f' % celldm4) + ' ,\n')
elif cell[0]==cell[1] and cell[0]!=cell[2] and cell[3]==90.0 and cell[4]==90.0 and cell[5]==90.0:
	# tetragonal ibrav = 6 or 7
	file2.write('    ' + 'ibrav= 6 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(3) = ' + str('%01.8f' % celldm3) + ' ,\n')
elif cell[0]==cell[1] and cell[0]!=cell[2] and cell[3]==90.0 and cell[4]==90.0 and cell[5]==120.0:
	# hexagonal or trigonal ibrav = 4
	file2.write('    ' + 'ibrav= 4 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(3) = ' + str(celldm3) + ' ,\n')
elif cell[3]==90.0 and cell[4]==90.0 and cell[5]==90.0:
	# orthorhombic ibrav = 8,9,10,11
	file2.write('    ' + 'ibrav= 8 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(2) = ' + str('%02.8f' % celldm2) + ' ,\n')
	file2.write('    ' + 'celldm(3) = ' + str('%02.8f' % celldm3) + ' ,\n')
elif cell[3]==90.0 and cell[4]!=90.0 and cell[5]==90.0:
	# monoclinic ibrav = 12,-12,13 unique b-axis
	file2.write('    ' + 'ibrav= -12 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(2) = ' + str('%02.8f' % celldm2) + ' ,\n')
	file2.write('    ' + 'celldm(3) = ' + str('%02.8f' % celldm3) + ' ,\n')
	file2.write('    ' + 'celldm(5) = ' + str('%02.8f' % celldm5) + ' ,\n')
elif cell[3]==90.0 and cell[4]==90.0 and cell[5]!=90.0:
	# monoclinic ibrav = 12,13 unique c-axis
	file2.write('    ' + 'ibrav= 12 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(2) = ' + str('%02.8f' % celldm2) + ' ,\n')
	file2.write('    ' + 'celldm(3) = ' + str('%02.8f' % celldm3) + ' ,\n')
	file2.write('    ' + 'celldm(4) = ' + str('%02.8f' % celldm6) + ' ,\n')
else:
	# triclinic ibrav = 14
	file2.write('    ' + 'ibrav= 14 ,\n')
	file2.write('    ' + 'celldm(1) = ' + str('%02.8f' % celldm1) + ' ,\n')
	file2.write('    ' + 'celldm(2) = ' + str('%02.8f' % celldm2) + ' ,\n')
	file2.write('    ' + 'celldm(3) = ' + str('%02.8f' % celldm3) + ' ,\n')
	file2.write('    ' + 'celldm(4) = ' + str('%02.8f' % celldm4) + ' ,\n')
	file2.write('    ' + 'celldm(5) = ' + str('%02.8f' % celldm5) + ' ,\n')
	file2.write('    ' + 'celldm(6) = ' + str('%02.8f' % celldm6) + ' ,\n')
file2.write('    nat =  ' + str(max-1) + ' ,\n')
file2.write('    ntyp = ' + str(natom) + ' ,\n')
file2.write('    ecutwfc = 60.0 ,\n')
file2.write('    ecutrho = 360.0 ,\n')
file2.write('!    nosym = .true.\n')
file2.write(' /\n')
file2.write(' &electrons\n')
file2.write('    electron_maxstep = 200 ,\n')
file2.write('    mixing_beta = 0.7 ,\n')
file2.write('!   use smaller conv_thr for better results ,\n')
file2.write('    conv_thr = 1.0d-14 ,\n')
file2.write(' /\n')
# depending on calculation mode, change contents
if cal == 'vc-relax':
	file2.write(' &ions\n')
	file2.write("    ion_dynamics='bfgs' ,\n")
	file2.write(' /\n')
	file2.write(' &CELL\n')
	file2.write("    cell_dynamics = 'bfgs' ,\n")
	file2.write("    press = 0.001,\n")
	file2.write("    press_conv_thr = 0.01 ,\n")
	file2.write("!   cell_dofree = 'xyz' ,\n")
	file2.write(' /\n')
elif cal == 'relax':
	file2.write(' &ions\n')
	file2.write("    ion_dynamics='bfgs' ,\n")
	file2.write(' /\n')
# add your favorite ps
file2.write('ATOMIC_SPECIES\n')
for i in range(1,natom+1):
	if len(kind[i-1])==1:
		tmp1 = ' '
	else:
		tmp1 = ''
	if len(str(wt[i-1])) == 5:
		tmp2 = '  '
	elif len(str(wt[i-1])) == 6:
		tmp2 = ' '
	else:
			tmp2 = ''
	if len(ps[i-1]) <= 1:
		file2.write('  ' + tmp1 + kind[i-1] + '  ' + tmp2 + str(wt[i-1]) + '   ' + kind[i-1] + '.' + pseudo + '\n')
	else:
		file2.write('  ' + tmp1 + kind[i-1] + '  ' + tmp2 + str(wt[i-1]) + '   ' + ps[i-1] + '\n')

file2.write('ATOMIC_POSITIONS crystal\n')
for i in range(1,max):
#	print lines[i].strip()
	tmp2 = ''
	if len(atom[i])==1:
		tmp2 = ' '
	# scf or no constraint specified, constraints are not given
	if cal=='scf' or constraint == '0':
		file2.write(atom[i] + tmp2 + '     ' + str('%01.6f' % x[i]) + '   ' + str('%01.6f' % y[i]) + '   ' + str('%01.6f' % z[i]) +'\n')
	# constraints are given after coordinates (cx,cy,cz)
	else:
		fx = x[i]
		fy = y[i]
		fz = z[i]
		cx = ' 1'
		if fx==0.000 or fx==0.125 or abs(fx-0.166667)<0.00001 or fx==0.250 or abs(fx-0.333333)<0.00001 or fx==0.375 or fx==0.500 or fx==0.625 or abs(fx-0.666666)<0.00001 or fx==0.750 or abs(fx-0.833333)<0.00001 or 	fx==0.875 or fx==1.000:
			cx = ' 0'
		cy = ' 1'
		if fy==0.000 or fy==0.125 or abs(fy-0.166667)<0.00001 or fy==0.250 or abs(fy-0.333333)<0.00001 or fy==0.375 or fy==0.500 or fy==0.625 or abs(fy-0.666666)<0.00001 or fy==0.750 or abs(fy-0.833333)<0.00001 or fy==0.875 or fy==1.000:
			cy = ' 0'
		cz = ' 1'
		if fz==0.000 or fz==0.125 or abs(fz-0.166667)<0.00001 or fz==0.250 or abs(fz-0.333333)<0.00001 or fz==0.375 or fz==0.500 or fz==0.625 or abs(fz-0.666666)<0.00001 or fz==0.750 or abs(fz-0.833333)<0.00001 or fz==0.875 or fz==1.000:
			cz = ' 0'
		file2.write(atom[i] + tmp2 + '     ' + str('%01.6f' % x[i]) + '   ' + str('%01.6f' % y[i]) + '   ' + str('%01.6f' % z[i]) + cx + cy + cz + '\n')
#
file2.write('K_POINTS automatic\n')
# change kmax below to optimize k-points for your default calculations.
# Current value could be small for accurate calculations.
kmax = 25
kx = int(kmax/cell[0])
if kx == 0:
	kx = 1
ky = int(kmax/cell[1])
if ky == 0:
	ky = 1
kz = int(kmax/cell[2])
if kz == 0:
	kz = 1
file2.write(' ' + str(kx) + ' ' + str(ky) + ' ' + str(kz) + ' 1 1 1\n')
file1.close()
file2.close()
