import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from pydicom.data import get_testdata_files
import pydicom
from os import system, getcwd, makedirs, walk, sep, pardir, remove
from os.path import exists, join, normpath
import shutil
import sys
import glob, shutil 


DIRROBEX = join(getcwd(), "ROBEX")


def robex(inDir):
    # output run robex
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_validation", "output_robex")):
        makedirs(join(inpreviousdir, "output_validation", "output_robex"))

    _, _, images = next(walk(inDir))
    for i in images:
        if(".nii.gz" in i):
            command = "cd {} && ./runROBEX.sh {} {}"
            system(command.format(DIRROBEX, join(inDir, i), join(inDir, i.split(".")[0]+'_robex.nii.gz' )))
            
            shutil.move(join(inDir, i.split(".")[0]+'_robex.nii.gz' ), join(inpreviousdir,"output_validation","output_robex"))


def deLIS(inDir, delisRepoPath, containerID):
    #output DeLIS 
    #command = "docker run -d --rm -it --mount type=bind,src={},dst=/data emilyesme/tf_delis"
    #system(command.format(delisRepoPath))
    # To run DeLIS comment imports: nibabel, numpy, matplotlib, pydicom, pydicom.data, 	can be run with ROBEX, but not wir rigid registration, to run rigid registration uncomment the imports
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_validation", "output_DeLIS")):
        makedirs(join(inpreviousdir, "output_validation", "output_DeLIS"))

    outputRobexDir = join(inpreviousdir,"output_validation","output_robex")
    _, _, images = next(walk(outputRobexDir))
    print('a copiar robex output')
    for i in images:
        if("_robex.nii.gz" in i):
            print('de ', join(outputRobexDir, i))
            print('a ', delisRepoPath)
            shutil.copy(join(outputRobexDir, i), delisRepoPath)
            command2 = " docker exec -it {} python /data/run_delis.py -b {} -o {}"
            print(command2.format(containerID, join("data",i), "/data"))
            system(command2.format(containerID, join("data",i), "/data"))
            if (exists(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz")) and exists(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz"))):
                command3 = "chmod -R 777 {}"
                system(command3.format(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz")))
                system(command3.format(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz")))
                shutil.move(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz"), join(inpreviousdir,"output_validation","output_DeLIS"))
                shutil.move(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz"), join(inpreviousdir,"output_validation","output_DeLIS"))
            os.remove(join(delisRepoPath, i))

    


def rigidRegistration(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_validation", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_validation", "output_FLIRT_images"))

    if not exists(join(inpreviousdir, "output_validation", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_validation", "output_FLIRT_mat"))
       
    root, _, images = next(walk(join(inpreviousdir, "atlas")))
    refImage = ""
    aux = -1

    for i in images:
        aux=+1
        if (".hdr" in i):
            refImage = images[aux]
            del images[aux]
            
            
    print(images)
    for i in images:
        if (".nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_validation", "output_FLIRT_images", i.split(".")[0]+"_rigid.nii.gz"),
            join(inpreviousdir, "output_validation", "output_FLIRT_mat", i.split(".")[0]+"_rigid")))


def main():
    
    inDir = join("/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/validationImages")
    #root, dirs, _ = next(walk(inDir))

    # output general dir 
    if not exists(join(normpath(inDir + sep +  pardir) , "output_validation")):
        makedirs(join(normpath(inDir + sep +  pardir) , "output_validation"))
    
    #print("Ejecuta Robex")
    #robex(inDir)

    #print("Ejecuta DeLIS")
    #/home/marthox/Documents/Vale_tesis/DeLIS/data
    #10c5a17e3844
    #deLIS('/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/test',
          #"/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/DeLIS/data/", "515608025efe")

    print("Ejecuta FLIRT")
    rigidRegistration(inDir)


main()
