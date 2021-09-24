import nibabel as nib
import numpy as np
from os import system, getcwd, makedirs, walk, sep, pardir, remove
from os.path import exists, join, normpath
import shutil, sys, glob, shutil, os
import matplotlib.pyplot as plt

def flirt(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_prototype_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_prototype_images"))
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_prototype_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_prototype_mat"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas")))

    atlasFlirtDir = join(inpreviousdir,"output_validation","output_FLIRT_images")
    _, _, images2 = next(walk(atlasFlirtDir))

    refImage = images2[0]

    for i in images:
        if (".nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear"
            system(command.format(join(root, i), join(atlasFlirtDir, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_prototype_images", i.split(".")[0]+"_rigid.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_prototype_mat", i.split(".")[0]+"_rigid")))

def main():
    
    inDir= join("/mnt/d/MRI-Brain-Atlas-Protocol/images")

    # output general dir 
    if not exists(join(normpath(inDir + sep +  pardir) , "output_atlas")):
        makedirs(join(normpath(inDir + sep +  pardir) , "output_atlas"))
    
    flirt(inDir)

main()