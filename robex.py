from os import system, getcwd, makedirs, walk
from os.path import exists, join
import shutil
import sys

actualdir = getcwd()

root, dirs, files = next(walk(actualdir))
for d in dirs:
	_, _, images = next(walk(join(actualdir, d)))
	for i in images:
		print(i)
		if (".img" in i):
			print("entro")
			command = 'cd {} && ../../ROBEX/runROBEX.sh {} {} && cd ..'
			print(command.format(d,i,i.split(".")[0]+'_robex.nii.gz'))
			system(command.format(d,i,i.split(".")[0]+'_robex.nii.gz'))
			
