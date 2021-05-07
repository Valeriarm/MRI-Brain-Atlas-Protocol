import os
import nibabel as nib
import numpy as np
from os import system, getcwd, makedirs, walk, sep, pardir, remove
from os.path import exists, join, normpath
import shutil
import sys
import glob, shutil, pydicom
import matplotlib.pyplot as plt
from pydicom.data import get_testdata_files

DIRROBEX = join(getcwd(), "ROBEX")


def robex(inDir):
    # output run robex
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_atlas", "output_robex")):
        makedirs(join(inpreviousdir, "output_atlas", "output_robex"))

    _, _, images = next(walk(inDir))
    for i in images:
        if(".nii.gz" in i):
            command = "cd {} && ./runROBEX.sh {} {}"
            system(command.format(DIRROBEX, join(inDir, i), join(inDir, i.split(".")[0]+'_robex.nii.gz' )))
            
            shutil.move(join(inDir, i.split(".")[0]+'_robex.nii.gz' ), join(inpreviousdir,"output_atlas","output_robex"))


def deLIS(inDir, delisRepoPath, containerID):
    #output DeLIS 
    #command = "docker run -d --rm -it --mount type=bind,src={},dst=/data emilyesme/tf_delis"
    #system(command.format(delisRepoPath))

    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_atlas", "output_DeLIS")):
        makedirs(join(inpreviousdir, "output_atlas", "output_DeLIS"))

    outputRobexDir = join(inpreviousdir,"output_atlas","output_robex")
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
                shutil.move(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz"), join(inpreviousdir,"output_atlas","output_DeLIS"))
                shutil.move(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz"), join(inpreviousdir,"output_atlas","output_DeLIS"))
            os.remove(join(delisRepoPath, i))


def affineRegistration(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", i.split(".")[0]+"_affine.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", i.split(".")[0]+"_affine")))


def average(inDir, affineDir):
    inpreviousdir = normpath(inDir + sep +  pardir)
    _, _, images = next(walk(affineDir))
    #print(join(affineDir, images[0]))
    initImage = nib.load(join(affineDir, images[0]))
    initImageData = initImage.get_fdata()
    #print(initImageData)
    images.remove(images[0])

    # promedio general dada la cantidad de imagenes 
    for index, image in enumerate(images):
        nextImage = nib.load(join(affineDir, image)).get_fdata()
        initImageData = ((initImageData[:,:,:] * (index + 1) ) + nextImage[:,:,:]) / (index + 2)
    nib.save(nib.Nifti1Image(initImageData, initImage.affine, initImage.header), join(inpreviousdir, 'output_atlas','averagepro_affine_delis_corratio.nii.gz'))


def main():
    
    inDir = join("/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/images")
    #root, dirs, _ = next(walk(inDir))

    # output general dir 
    if not exists(join(normpath(inDir + sep +  pardir) , "output_atlas")):
        makedirs(join(normpath(inDir + sep +  pardir) , "output_atlas"))
    
    print("Ejecuta Robex")
    #robex(inDir)

    print("Ejecuta DeLIS")
    #/home/marthox/Documents/Vale_tesis/DeLIS/data
    #10c5a17e3844
    #deLIS('/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/test',
    #      "/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/DeLIS/data/", "515608025efe")

    print("Ejecuta FLIRT")
    affineRegistration(inDir)

    print("Promedia")
    print(join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images"))
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images"))



main()
