from os import getcwd, makedirs, system
import nibabel as nib
import numpy as np
import glob, shutil, pydicom
import matplotlib.pyplot as plt
from pydicom.data import get_testdata_files

from os.path import exists, join

########################################################

def average(imagesDir):
    initImage = nib.load(imagesDir[0])
    initImageData = initImage.get_fdata()
    imagesDir.remove(imagesDir[0])

    # promedio general dada la cantidad de imagenes 
    for index, imageDir in enumerate(imagesDir):
        nextImage = nib.load(imageDir).get_fdata()
        initImageData = ((initImageData[:,:,:] * (index + 1) ) + nextImage[:,:,:]) / (index + 2)
    nib.save(nib.Nifti1Image(initImageData, initImage.affine, initImage.header), join(getcwd(),'averagepro_rigid_pil1.nii'))

#######################################################

def flirt(path, files):

    if not exists(join(path, "1.originals")):
        makedirs(join(path, "1.originals"))

    if not exists(join(path, "2.flirt_mat")):
        makedirs(join(path, "2.flirt_mat"))

    for f in files:
        if ("converted_PIL.nii" in f):
            shutil.move(join(path, f), join(path, "1.originals"))
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear"
            system(command.format(join(path, "1.originals", f),
                                  join(path, "refimage.nii"),
                                  join(path, f.split(".")[0]+"_rigid_pil1.nii.gz"),
                                  join(path, f.split(".")[0]+".mat")))
            shutil.move(
                join(path, f.split(".")[0]+"_flirt.mat"), join(path, "2.flirt_mat"))


ACTUAL_DIRECTORY = getcwd()
imagesDir = glob.glob(join(ACTUAL_DIRECTORY, "**", "*converted_PIL.nii"), recursive=True)
average(imagesDir)

