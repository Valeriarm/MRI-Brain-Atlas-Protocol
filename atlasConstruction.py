import nibabel as nib
import numpy as np
from os import system, getcwd, makedirs, walk, sep, pardir, remove
from os.path import exists, join, normpath
import shutil, sys, glob, shutil, os
import matplotlib.pyplot as plt

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

#--------------------------------------------CORRATIO----------------------------------
def corratio_trilinear(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear"))
       
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
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear" ,i.split(".")[0]+"_affine_corratio_trilinear.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear" , i.split(".")[0]+"_affine_corratio_trilinear")))



def corratio_nearestneighbour(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_nearestneighbour")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_nearestneighbour"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_nearestneighbour")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_nearestneighbour"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp nearestneighbour"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_nearestneighbour" ,i.split(".")[0]+"_affine_corratio_nearestneighbour.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_nearestneighbour" ,i.split(".")[0]+"_affine_corratio_nearestneighbour")))

def corratio_sinc(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_sinc")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_sinc"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_sinc")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_sinc"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp sinc"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_sinc" ,i.split(".")[0]+"_affine_corratio_sinc.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_sinc" ,i.split(".")[0]+"_affine_corratio_sinc")))


def corratio_spline(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_spline")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_spline"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_spline")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_spline"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp spline"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_spline" ,i.split(".")[0]+"_affine_corratio_spline.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_spline" ,i.split(".")[0]+"_affine_corratio_spline")))

def corratio_trilinear_noDeLIS(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_noDeLIS")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_noDeLIS"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_noDeLIS")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_noDeLIS"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_robex")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if (".nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_noDeLIS" ,i.split(".")[0]+"_affine_corratio_trilinear_noDeLIS.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_noDeLIS" , i.split(".")[0]+"_affine_corratio_trilinear_noDeLIS")))


#--------------------------------------NORMMI----------------------------------

def normmi_trilinear(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_trilinear"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_trilinear"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_trilinear" ,i.split(".")[0]+"_affine_normmi_trilinear.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_trilinear" , i.split(".")[0]+"_affine_normmi_trilinear")))



def normmi_nearestneighbour(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_nearestneighbour")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_nearestneighbour"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_nearestneighbour")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_nearestneighbour"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    for i in images:
        if ("_delis.nii.gz" in i):
            print(i)
            print(' --')
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp nearestneighbour"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_nearestneighbour" ,i.split(".")[0]+"_affine_normmi_nearestneighbour.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_nearestneighbour" , i.split(".")[0]+"_affine_normmi_nearestneighbour")))

def normmi_sinc(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_sinc")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_sinc"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_sinc")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_sinc"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    for i in images:
        if ("_delis.nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp sinc"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_sinc" , i.split(".")[0]+"_affine_normmi_sinc.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_sinc", i.split(".")[0]+"_affine_normmi_sinc")))


def normmi_spline(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_spline")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_spline"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_spline")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_spline"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]
    del images[0]

    for i in images:
        if ("_delis.nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp spline"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_spline", i.split(".")[0]+"_affine_normmi_spline.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_spline", i.split(".")[0]+"_affine_normmi_spline")))


def normmi_trilinear_noDeLIS(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_trilinear_noDeLIS")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_trilinear_noDeLIS"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_trilinear_noDeLIS")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_trilinear_noDeLIS"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_robex")))

    refImage = images[0]

    del images[0]

    for i in images:
        if (".nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normmi_trilinear_noDeLIS" ,i.split(".")[0]+"_affine_normmi_trilinear_noDeLIS.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normmi_trilinear_noDeLIS" , i.split(".")[0]+"_affine_normmi_trilinear_noDeLIS")))


#--------------------------------------normcorr----------------------------------

def normcorr_trilinear(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normcorr_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normcorr_trilinear"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normcorr_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normcorr_trilinear"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    for i in images:
        if ("_delis.nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normcorr -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "normcorr_trilinear" ,i.split(".")[0]+"_affine_normcorr_trilinear.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "normcorr_trilinear" , i.split(".")[0]+"_affine_normcorr_trilinear")))


#--------------------------------------LEASTSQ----------------------------------

def leastsq_trilinear(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "leastsq_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "leastsq_trilinear"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "leastsq_trilinear")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "leastsq_trilinear"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    for i in images:
        if ("_delis.nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost normcorr -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "leastsq_trilinear" ,i.split(".")[0]+"_affine_leastsq_trilinear.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "leastsq_trilinear" , i.split(".")[0]+"_affine_leastsq_trilinear")))



#-------------------------------------CORRATIO LINEAR 6----------------------------------
def corratio_trilinear_linear6(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear6")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear6"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_linear6")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_linear6"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear6" ,i.split(".")[0]+"_affine_corratio_trilinear_linear6.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_linear6" , i.split(".")[0]+"_affine_corratio_trilinear_linear6")))


#-------------------------------------CORRATIO LINEAR 9----------------------------------
def corratio_trilinear_linear9(inDir):
    #output FLIRT affine Registration
    inpreviousdir = normpath(inDir + sep +  pardir)

    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear9")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear9"))
    
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat"))
        
    if not exists(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_linear9")):
        makedirs(join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_linear9"))
       
    root, _, images = next(walk(join(inpreviousdir, "output_atlas", "output_DeLIS")))

    refImage = images[0]

    del images[0]

    print(images)
    for i in images:
        if ("_delis.nii.gz" in i):
            command = "/usr/local/fsl/bin/flirt -in {} -ref {} -out {} -omat {}.mat -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 9  -interp trilinear"
            system(command.format(join(root, i), join(root, refImage), 
            join(inpreviousdir, "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear9" ,i.split(".")[0]+"_affine_corratio_trilinear_linear9.nii.gz"),
            join(inpreviousdir, "output_atlas", "output_FLIRT_mat", "corratio_trilinear_linear9" , i.split(".")[0]+"_affine_corratio_trilinear_linear9")))



#------------------------------NON-LINEAR----------------------------------------

def nonLinearAtlas(inDir):
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_atlas", "output_ANTS")):
        makedirs(join(inpreviousdir, "output_atlas", "output_ANTS"))

    delisOutputDir = join(inpreviousdir,"output_atlas","output_DeLIS")
    _, _, images = next(walk(delisOutputDir))

    atlasFlirtDir = join(inpreviousdir,"output_validation","output_FLIRT_images")
    _, _, images2 = next(walk(atlasFlirtDir))

    refImage = images2[0]
    
    for i in images:
        if("delis.nii.gz" in i):
            command = "/mnt/d/ANTs/install/bin/antsRegistrationSyNQuick.sh -d 3 -f {} -m {} -o {}"
            system(command.format(join(atlasFlirtDir, refImage), join(delisOutputDir, i), join(inpreviousdir, "output_atlas", "output_ANTS", i.split(".")[0]+"_ants" )))




#-------------------------------AVERAGE------------------------------------------

def average(inDir, affineDir, atlasName):
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
    nib.save(nib.Nifti1Image(initImageData, initImage.affine, initImage.header), join(inpreviousdir, 'output_atlas', atlasName))


def averageNonRigid(inDir, affineDir, atlasName):
    inpreviousdir = normpath(inDir + sep +  pardir)
    _, _, allImages = next(walk(affineDir))

    images = []

    for i in allImages:
        if("antsWarped.nii.gz" in i):
            images.append(i)

    initImage = nib.load(join(affineDir, images[0]))
    initImageData = initImage.get_fdata()
    #print(initImageData)
    images.remove(images[0])

    print(images)

    # promedio general dada la cantidad de imagenes 
   
    for index, image in enumerate(images):
        nextImage = nib.load(join(affineDir, image)).get_fdata()
        initImageData = ((initImageData[:,:,:] * (index + 1) ) + nextImage[:,:,:]) / (index + 2)
    nib.save(nib.Nifti1Image(initImageData, initImage.affine, initImage.header), join(inpreviousdir, 'output_atlas', atlasName))




def main():
    
    inDir = join("/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/images")
    #inDir= join("/mnt/d/MRI-Brain-Atlas-Protocol/images")
    #root, dirs, _ = next(walk(inDir))

    # output general dir 
    if not exists(join(normpath(inDir + sep +  pardir) , "output_atlas")):
        makedirs(join(normpath(inDir + sep +  pardir) , "output_atlas"))
    '''
    print("Ejecuta Robex")
    robex(inDir)

    print("Ejecuta DeLIS")
    deLIS('/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/test',
          "/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/DeLIS/data/", "515608025efe")

    print("Ejecuta FLIRT con las diferentes configuraciones")
    corratio_trilinear(inDir)
    corratio_nearestneighbour(inDir)
    corratio_sinc(inDir)
    corratio_spline(inDir)
    normmi_trilinear(inDir)
    normmi_nearestneighbour(inDir)
    normmi_sinc(inDir)
    normmi_spline(inDir)
    normcorr_trilinear(inDir)
    leastsq_trilinear(inDir)
    

    print("Promedia los atlas prototipos")
    print(join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images"))

    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_trilinear"), "averagepro_affine_delis_corratio_trilinear.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_nearestneighbour"), "averagepro_affine_delis_corratio_nearestneighbour.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_sinc"), "averagepro_affine_delis_corratio_sinc.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_spline"), "averagepro_affine_delis_corratio_spline.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normmi_trilinear"), "averagepro_affine_delis_normmi_trilinear.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normmi_nearestneighbour"), "averagepro_affine_delis_normmi_nearestneighbour.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normmi_sinc"), "averagepro_affine_delis_normmi_sinc.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normmi_spline"), "averagepro_affine_delis_normmi_spline.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normcorr_trilinear"), "averagepro_affine_delis_normcorr_trilinearnii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "leastsq_trilinear"), "averagepro_affine_delis_leastsq_trilinear.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_trilinear_noDeLIS"), "averagepro_affine_corratio_trilinear_noDeLIS.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normmi_trilinear_noDeLIS"), "averagepro_affine_normmi_trilinear_noDeLIS.nii.gz")

    #nonLinearAtlas(inDir)
    

    corratio_trilinear_noDeLIS(inDir)
    normmi_trilinear_noDeLIS(inDir)
    corratio_trilinear_linear6(inDir)
    corratio_trilinear_linear9(inDir)

    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear6"), "averagepro_affine_corratio_trilinear_linear6.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_trilinear_linear9"), "averagepro_affine_corratio_trilinear_linear9.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "corratio_trilinear_noDeLIS"), "averagepro_affine_corratio_trilinear_noDeLIS.nii.gz")
    average(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_FLIRT_images", "normmi_trilinear_noDeLIS"), "averagepro_affine_normmi_trilinear_noDeLIS.nii.gz")

    

    #averageNonRigid(inDir, join(normpath(inDir + sep +  pardir) , "output_atlas", "output_ANTS"), "averagepro_affine_corratio_trilinear_noLinear.nii.gz")
    '''


main()
