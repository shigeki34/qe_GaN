#!/usr/local/bin/python3
import sys,math,subprocess

# pwout2xtl.py
# made by mkanzaki@me.com
# 2015/01/07: put in my wiki page
# 2016/08/25: revised to include non-optimized file
# 2017/06/24: add to open by Vesta
# 2019/06/29: to Python3 by 2to3
# 2020/02/10: bug fix (cell parameters are too long, round is used)
# 2021/01/29: relax was considered
# Utility code for Quantum-Espsresso and Vesta.
# This code converts pw.x output (optimization) to .xtl file,
# which can be read by Vesta.
# pw.x output must be optimization (vc-relax or relax) run
# Usage:
# >./pwout2xtl.py test.out
# When optimization was failed, this code will use last optimized structure
# (but not fully optimized one) instead, and prints out warning.
# Then test.out.xtl will be produced.
# Open it with Vesta.

mat1 = [0.0 for i in range(3)]
mat2 = [0.0 for i in range(3)]
mat3 = [0.0 for i in range(3)]
cell = ['' for i in range(4)]
celldm = [0.0 for i in range(7)]

# conversion for radian 
rd = math.pi/180.0
# conversion factor for atomic unit to angstrom 
bohr = 0.5291772108

# reading output file
# check xtl file name is given or not
if len(sys.argv) == 1:
	print('No optimization output file name provided!')
	print('for example: > ./pwout2xtl.py test.out')
	exit()
try:
	file1 = open(sys.argv[1],'r')
	base = sys.argv[1]
except IOError as xxx_todo_changeme:
	(errno, msg) = xxx_todo_changeme.args
	print('Optimization output file open error!')
	exit()
		
# Get .out file name
# Open output file for .xtl
f2 = base + '.xtl'
file2 = open(f2,'w')

# read all lines into all_lines
all_lines = file1.readlines()
file1.close()

# check whether relax or vc-relax run?
vcrelax = 0
for i in range(0,len(all_lines)):
	ftext = all_lines[i]
	if 'CELL_PARAMETERS' in ftext :  # it means vc-relax run
		vcrelax = 1
		break
# extract ibrav number, defined in input file
ibrav = 1 # initial cubic p
for i in range(0,len(all_lines)):
	ftext = all_lines[i]
	if 'bravais-lattice index' in ftext :  # ibrav defined in input file
		break
tmp = ftext.strip()
tmp = tmp.split(' ')
while tmp.count('') > 0:
	tmp.remove('')
ibrav = int(tmp[3]) # obtained ibrav

# extract cell parameters for relax calculation, for vc-relax skip here
if vcrelax == 0: # if this is relax run, get cell parameters
	for i in range(0,len(all_lines)):
		ftext = all_lines[i]
		if 'celldm' in ftext :
			break
	cell1 = all_lines[i].strip()
	cell2 = all_lines[i+1].strip()
	lcell1 = cell1.split(' ')
	while lcell1.count('') > 0:
		lcell1.remove('')
	lcell2 = cell2.split(' ')
	while lcell2.count('') > 0:
		lcell2.remove('')
	celldm[1] = float(lcell1[1]) # index start from 1 (= QE's celldm(1:6))
	celldm[2] = float(lcell1[3])
	celldm[3] = float(lcell1[5])
	celldm[4] = float(lcell2[1])
	celldm[5] = float(lcell2[3])
	celldm[6] = float(lcell2[5])
	if ibrav == 1 or ibrav == 2 or ibrav == 3 or ibrav == -3 : # cubic
		cella = celldm[1]*bohr
		cellb = cella
		cellc = cella
		alpha = 90.0
		beta = 90.0
		gamma = 90.0
	elif ibrav == 4: # hexagonal
		cella = celldm[1]*bohr
		cellb = cella
		cellc = cella*celldm[3]
		alpha = 90.0
		beta = 90.0
		gamma = 120.0
	elif ibrav == 5 or ibrav == -5: # trigonal
		cella = celldm[1]*bohr
		cellb = cella
		cellc = cella
		alpha = math.acos(celldm[4])/rd
		beta = alpha
		gamma = alpha
	elif ibrav == 6 or ibrav == 7: # tetragonal
		cella = celldm[1]*bohr
		cellb = cella
		cellc = celldm[3]*cella
		alpha = 90.0
		beta = 90.0
		gamma = 90.0
	elif ibrav == 8 or ibrav == 9 or ibrav == -9 or ibrav == 91 or ibrav == 10 or ibrav == 11 : # orthorhombic	
		cella = celldm[1]*bohr
		cellb = celldm[2]*cella
		cellc = celldm[3]*cella
		alpha = 90.0
		beta = 90.0
		gamma = 90.0
	elif ibrav == 12 or ibrav == 13: # monoclinic unique axis c
		cella = celldm[1]*bohr
		cellb = celldm[2]*cella
		cellc = celldm[3]*cella
		alpha = 90.0
		beta = 90.0
		gamma = math.acos(celldm[4])/rd
	elif ibrav == -12 or ibrav == -13: # monoclinic unique axis b
		cella = celldm[1]*bohr
		cellb = celldm[2]*cella
		cellc = celldm[3]*cella
		alpha = 90.0
		beta = math.acos(celldm[5])/rd
		gamma = 90.0
	elif ibrav == 14: # triclinic
		cella = celldm[1]*bohr
		cellb = celldm[2]*cella
		cellc = celldm[3]*cella
		alpha = math.acos(celldm[4])/rd
		beta = math.acos(celldm[5])/rd
		gamma = math.acos(celldm[6])/rd
	elif ibrav == 0: # ibrav = 0 this is special case, and need to read following crystal axes matrix 
		axes1 = all_lines[i+4].strip()
		axes2 = all_lines[i+5].strip()
		axes3 = all_lines[i+6].strip()
		laxes1 = axes1.split(' ')
		while laxes1.count('') > 0:
			laxes1.remove('')
		laxes2 = axes2.split(' ')
		while laxes2.count('') > 0:
			laxes2.remove('')
		laxes3 = axes3.split(' ')
		while laxes3.count('') > 0:
			laxes3.remove('')
		for j in range(0,3): # reading matrix
			mat1[j] = float(laxes1[j+3])
			mat2[j] = float(laxes2[j+3])
			mat3[j] = float(laxes3[j+3])
		cella = math.sqrt(mat1[0]*mat1[0]+mat1[1]*mat1[1]+mat1[2]*mat1[2])
		cellb = math.sqrt(mat2[0]*mat2[0]+mat2[1]*mat2[1]+mat2[2]*mat2[2])
		cellc = math.sqrt(mat3[0]*mat3[0]+mat3[1]*mat3[1]+mat3[2]*mat3[2])
		alpha = math.acos((mat2[0]*mat3[0]+mat2[1]*mat3[1]+mat2[2]*mat3[2])/(cellb*cellc))/rd
		beta = math.acos((mat1[0]*mat3[0]+mat1[1]*mat3[1]+mat1[2]*mat3[2])/(cella*cellc))/rd
		gamma = math.acos((mat1[0]*mat2[0]+mat1[1]*mat2[1]+mat1[2]*mat2[2])/(cella*cellb))/rd
		cella = celldm[1]*bohr*cella
		cellb = celldm[1]*bohr*cellb
		cellc = celldm[1]*bohr*cellc

ix = 0
if vcrelax == 1:
	for i in range(0,len(all_lines)):
		ftext = all_lines[i]
		if 'Final enthalpy' in ftext :  # this is also new from 6.5
			ftext = all_lines[i+1]			
			if 'Begin final' in ftext :
				ix = i+3  # for previous version 
			else:
				ix = i+5  # needed for 6.7.0
	if ix == 0: # "Final" not found, then check last structure
		print('Optimization of this run failed. Last structure is used!') 
		for i in reversed(range(0,len(all_lines))):
			ftext = all_lines[i]
			if 'CELL_PARAMETERS' in ftext :
				ix = i
				#print(str(ix))
				break
	else: # optimization successful
		ftext = all_lines[ix]
		if 'density' in ftext: # Density added for newer version
			ix  = ix + 2 # newer version
		else:
			ix = ix + 1 # older version

	#print(ftext)

	# now ix is pointing a line with "CELL_PARAMETERS ..."
	# get cell parameters (alat)
	ftext = all_lines[ix].strip()
	s = ftext.index('alat=')+5
	t = ftext.index(')')
	alat = float(ftext[s:t])
	# reading cell matrix
	cell[0] = all_lines[ix+1].strip()
	list = cell[0].split(' ')
	while list.count('') > 0:
		list.remove('')
	for i in range(0,3):
		mat1[i] = float(list[i])
	cell[1] = all_lines[ix+2].strip()
	list = cell[1].split(' ')
	while list.count('') > 0:
		list.remove('')
	for i in range(0,3):
		mat2[i] = float(list[i])
	cell[2] = all_lines[ix+3].strip()
	list = cell[2].split(' ')
	while list.count('') > 0:
		list.remove('')
	for i in range(0,3):
		mat3[i] = float(list[i])
	# cell parameters calculation
	cella = math.sqrt(mat1[0]*mat1[0]+mat1[1]*mat1[1]+mat1[2]*mat1[2])
	cellb = math.sqrt(mat2[0]*mat2[0]+mat2[1]*mat2[1]+mat2[2]*mat2[2])
	cellc = math.sqrt(mat3[0]*mat3[0]+mat3[1]*mat3[1]+mat3[2]*mat3[2])
	alpha = math.acos((mat2[0]*mat3[0]+mat2[1]*mat3[1]+mat2[2]*mat3[2])/(cellb*cellc))/rd
	beta = math.acos((mat1[0]*mat3[0]+mat1[1]*mat3[1]+mat1[2]*mat3[2])/(cella*cellc))/rd
	gamma = math.acos((mat1[0]*mat2[0]+mat1[1]*mat2[1]+mat1[2]*mat2[2])/(cella*cellb))/rd
	cella = alat*bohr*cella
	cellb = alat*bohr*cellb
	cellc = alat*bohr*cellc
# end for vc-relax 
else: # for relax
	ix = 0
	for i in range(0,len(all_lines)):
		ftext = all_lines[i]
		if 'Final energy' in ftext :  # in relax, "energy" not "enthalpy"
			ix = i+3
	if ix == 0: # "Final" not found, then check last structure
		print('Optimization of this run failed. Last structure is used!') 
		for i in reversed(range(0,len(all_lines))):
			ftext = all_lines[i]
			if 'ATOMIC_POSITIONS' in ftext :
				ix = i
#	ix = ix + 1 # now pointing start position of coordinate

# Write title and cell to .xtl file
file2.write('TITLE ' + 'Produced from pw.x calculation: ' + base + '\n')
file2.write('CELL\n')
file2.write(' ' + str(round(cella,5)) + ' ' + str(round(cellb,5)) + ' ' + str(round(cellc,5)) + ' ' + str(round(alpha,5)) + ' ' + str(round(beta,5)) + ' ' + str(round(gamma,5)) + '\n')   
# find atomic positions
if vcrelax == 1:
	ix = ix + 5 # line containing "ATOMIC_POSITIONS ..."
# write atomic positions
file2.write('SYMMETRY NUMBER 1\n')
file2.write('SYMMETRY LABEL  P1\n')
file2.write('ATOMS\n')
file2.write('NAME         X           Y           Z\n')
while True:
	ix = ix + 1
	ftext = all_lines[ix]
	if ('End final coordinates' in ftext) or (ftext == '\n'):
		break
	else:
		file2.write(ftext)
# write EOF line
file2.write('EOF\n')
file2.close()
#cmd = "open -a VESTA" + " " + f2 
#subprocess.call(cmd,shell=True)
exit()
