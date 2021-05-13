import os
import nibabel as nib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pydicom.data import get_testdata_files
import pydicom
from os import system, getcwd, makedirs, walk, sep, pardir, remove
from os.path import exists, join, normpath
import shutil, sys, glob, shutil, scipy, math


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

    #docker exec -it 515608025efe python /data/run_delis.py -b /data/icbm452_atlas_air12_sinc.hdr -o /data

def deLISAtlas(inDir, delisRepoPath, containerID):
    # To run DeLIS comment imports: nibabel, numpy, matplotlib, pydicom, pydicom.data, 	can be run with ROBEX, but not wir rigid registration, to run rigid registration uncomment the imports
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_validation", "output_DeLIS_atlas")):
        makedirs(join(inpreviousdir, "output_validation", "output_DeLIS_atlas"))

    atlasDir = join(inpreviousdir,"atlas")
    _, _, images = next(walk(atlasDir))
    print('a copiar atlas output')
    for i in images:
        if(".nii.gz" in i):
            print('de ', join(atlasDir, i))
            print('a ', delisRepoPath)
            shutil.copy(join(atlasDir, i), delisRepoPath)
            command2 = " docker exec -it {} python /data/run_delis.py -b {} -o {}"
            print(command2.format(containerID, join("data",i), "/data"))
            system(command2.format(containerID, join("data",i), "/data"))
            if (exists(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz")) and exists(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz"))):
                command3 = "chmod -R 777 {}"
                system(command3.format(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz")))
                system(command3.format(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz")))
                shutil.move(join(delisRepoPath,i.split(".")[0]+"_seg.nii.gz"), join(inpreviousdir,"output_validation","output_DeLIS_atlas"))
                shutil.move(join(delisRepoPath,i.split(".")[0]+"_delis.nii.gz"), join(inpreviousdir,"output_validation","output_DeLIS_atlas"))
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
        if ("icbm452_atlas_air12_sinc.nii.gz" in i):
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


def nonRigidRegistration(inDir):

    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_validation", "output_ANTS")):
        makedirs(join(inpreviousdir, "output_validation", "output_ANTS"))

    delisOutputDir = join(inpreviousdir,"output_validation","output_DeLIS")
    _, _, images = next(walk(delisOutputDir))

    refImage = images[0]

    atlasDir = join(inpreviousdir,"output_validation","output_DeLIS_atlas")
    _, _, images2 = next(walk(atlasDir))

    atlasFlirtDir = join(inpreviousdir,"output_validation","output_FLIRT_images")
    _, _, images3 = next(walk(atlasFlirtDir))
    
    for i in images2:
        if("sinc_delis.nii.gz" in i):
            for j in images:
                if("delis.nii.gz" in i):
                    command = "/mnt/d/ANTs/install/bin/antsRegistrationSyNQuick.sh -d 3 -f {} -m {} -o {}"
                    system(command.format(join(delisOutputDir, j), join(atlasDir, i), join(inpreviousdir, "output_validation", "output_ANTS", i.split(".")[0]+j.split(".")[0]+"_ants" )))
    
    for i in images3:
        if("_rigid.nii.gz" in i):
            for j in images:
                if("delis.nii.gz" in j):
                    command = "/mnt/d/ANTs/install/bin/antsRegistrationSyNQuick.sh -d 3 -f {} -m {} -o {}"
                    system(command.format(join(delisOutputDir, j), join(atlasFlirtDir, i), join(inpreviousdir, "output_validation", "output_ANTS", i.split(".")[0]+j.split(".")[0]+"_ants" )))


def createJacobian(inDir):
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_validation", "output_jacobian")):
        makedirs(join(inpreviousdir, "output_validation", "output_jacobian"))

    antsDir = join(inpreviousdir,"output_validation","output_ANTS")
    _, _, images = next(walk(antsDir))

    for i in images:
        if("InverseWarp.nii.gz" in i):
            command = "/mnt/d/ANTs/install/bin/CreateJacobianDeterminantImage 3 {} {} 1"
            system(command.format(join(antsDir, i), join(inpreviousdir, "output_validation", "output_jacobian", i.split(".")[0]+"_jacobian.nii.gz" )))


def jacobianIntegration(inDir):
    
    inpreviousdir = normpath(inDir + sep +  pardir) 

    if not exists(join(inpreviousdir, "output_validation", "output_jacobian_integration")):
        makedirs(join(inpreviousdir, "output_validation", "output_jacobian_integration"))

    #Aca estan las imagenes de validacion 
    delisOutputDir = join(inpreviousdir,"output_validation","output_DeLIS")
    _, _, delisImages = next(walk(delisOutputDir))
    
    #aca estan los jacobianos creados con la inversa
    jacobianDir = join(inpreviousdir,"output_validation","output_jacobian")
    _, _, jacobianImages = next(walk(jacobianDir))

    '''
    #recorro las imagenes de prueba y obtengo la mascara (matriz booleana)
    aux = -1

    for j in jacobianImages:
        aux =aux+1
        if (j.split("-")[1] in delisImages[math.floor(aux/2)]):
            if("_delis.nii.gz" in delisImages[math.floor(aux/2)]):

                img = nib.load(join(delisOutputDir, delisImages[math.floor(aux/2)]))
                imageRef = np.array(img.dataobj)
                imageMask = imageRef>0

                imgJ = nib.load(join(jacobianDir, j))
                imageJ = np.array(imgJ.dataobj)
                
                for k in range (len(imageMask)):
                    for l in range(len(imageMask[0])):
                        if(not imageMask[k][l].all):
                            imageJ[k][l]= 0
                            imageRef[k][l]= 0

        new_image = nib.Nifti1Image(imageJ, affine=np.eye(4))
        nib.save(new_image, join(inpreviousdir, "output_validation", "output_jacobian_integration", j.split(".")[0]+"_integration.nii.gz" ))
        file = open(join(inpreviousdir, "output_validation", "output_jacobian_integration",j.split(".")[0]+".txt"), "w")
        file.write("\n" + delisImages[math.floor(aux/2)].split(".")[0] + "\n" + j.split("-")[0] + "\n" + str(np.sum(np.abs(imageJ))) + "\n" + str(np.sum(np.abs(imageRef))) + "\n" + str(np.sum(np.abs(imageJ))/np.sum(np.abs(imageRef))))
        del j
        #print(np.sum(np.abs(imageJ))/np.sum(np.abs(imageRef)))
    
    '''
    aux=0
    for j in jacobianImages:
                aux=aux+1

    for i in delisImages:
        if("_delis.nii.gz"):
            img = nib.load(join(delisOutputDir, i))
            imageRef = np.array(img.dataobj)
            imageMask = imageRef>0

            print("\nEstoy en la imagen" + i+"\n")
        
            print(str(aux))

            for j in range (aux):
                if (i.split(".")[0] in jacobianImages[j]):
                    print("Iteracion " + str(j) + "\nimagen jacobiana: " + jacobianImages[j] + "\nimagenDelis: "+ i)
                    imgJ = nib.load(join(jacobianDir, jacobianImages[j]))
                    imageJ = np.array(imgJ.dataobj)
                    for k in range (len(imageMask)):
                        for l in range(len(imageMask[0])):
                            if(not imageMask[k][l].all):
                                imageJ[k][l]= 0
                                imageRef[k][l]= 0
                    new_image = nib.Nifti1Image(imageJ, affine=np.eye(4))
                    nib.save(new_image, join(inpreviousdir, "output_validation", "output_jacobian_integration", jacobianImages[j].split(".")[0]+"_integration.nii.gz" ))
                    file = open(join(inpreviousdir, "output_validation", "output_jacobian_integration",jacobianImages[j].split(".")[0]+".txt"), "w")
                    file.write("\n" + i.split(".")[0] + "\n" + jacobianImages[j].split("-")[0] + "\n" + str(np.sum(np.abs(imageJ))) + "\n" + str(np.sum(np.abs(imageRef))) + "\n" + str(np.sum(np.abs(imageJ))/np.sum(np.abs(imageRef))))
                    
    



def main():

    #inDir = join("/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/validationImages")
    inDir2= join("/mnt/d/MRI-Brain-Atlas-Protocol/validationImages")

    # output general dir 
    if not exists(join(normpath(inDir2 + sep +  pardir) , "output_validation")):
        makedirs(join(normpath(inDir2 + sep +  pardir) , "output_validation"))
    
    '''
    print("Ejecuta Robex en imagenes de validacion")
    robex(inDir)

    print("Ejecuta DeLIS en imagenes de validacion")
    deLIS('/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/validationImages', "/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/DeLIS/data/", "515608025efe")

    print("Ejecuta DeLIS en altas")
    deLISAtlas('/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/atlas', "/home/biomarcadores/Escritorio/brainAtlas/brain_atlas_script/DeLIS/data/", "515608025efe")
    

    print("Ejecuta FLIRT entre atlas para normalizacion espacial")
    rigidRegistration(inDir2)
    
    print("Ejecuta ANTs Registration SyN para registro no rigido entre atlas y casos prueba")
    nonRigidRegistration(inDir2)
    
    '''

    #print("Ejecuta ANTs CreateJacobian para obtener la imagen del determinante jacobiano")
    #createJacobian(inDir2)

    

    print("Integra el jacobiano con la imagen de referecia")
    jacobianIntegration(inDir2)

    


main()

