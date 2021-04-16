from os import system, getcwd, makedirs, walk, sep, pardir
from os.path import exists, join, normpath
import shutil
import sys
import nibabel as nib
import numpy as np
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
        if(".nifti.img" in i):
            command = "cd {} && ./runROBEX.sh {} {}"
            system(command.format(DIRROBEX, join(inDir, i), join(inDir, i.split(".")[0]+'_robex.nii.gz' )))
            
            shutil.move(join(inDir, i.split(".")[0]+'_robex.nii.gz' ), join(inpreviousdir,"output_atlas","output_robex"))

def affineRegistration(inDir):

    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    _, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_robex")))

    refImage = images[0]
    del images[0]

    outputRobexDir = join(inpreviousdir,"output_atlas","output_robex")


    for i in images:
        if ("_robex.nii.gz" in i):

            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(outputRobexDir, i), join(outputRobexDir, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", i.split(".")[0]+'_affine.nii.gz' ),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", i.split(".")[0]+'_affine')))


def average(affineDir):
    
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
    nib.save(nib.Nifti1Image(initImageData, initImage.affine, initImage.header), join(getcwd(),'averagepro_affine_delis_normmi.nii'))


def main():
    
    inDir = join("/mnt/d/brain_atlas_script/testImages")
    #root, dirs, _ = next(walk(inDir))

    # output general dir 
    if not exists(join(normpath(inDir + sep +  pardir) , "output_atlas")):
        makedirs(join(normpath(inDir + sep +  pardir) , "output_atlas"))
    
    print("Ejecuta Robex")
    robex(inDir)

    print("Ejecuta FLIRT")
    affineRegistration(inDir)

    print("Promedia")
    #print(join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images"))
    average(join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images"))



main()
