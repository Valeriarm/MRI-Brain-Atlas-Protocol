from os import system, getcwd, makedirs, walk, rename, remove
from os.path import exists, isfile, join, sep
import shutil
import sys
import getopt
import nibabel as nib
from scipy.stats import mode
import numpy as np
from run_intensity import run_intensity_delis


ALLOWED_EXTENSIONS = {'nii.gz', 'nii'}


# allowed_files: string -> boolean
# check if the file path has the allowed extensions


def allowed_file(file):
    extension = ".".join(file.split(".")[1:])
    print(extension)
    return extension in ALLOWED_EXTENSIONS


def main():
    baselineFile = ''
    outputDir = ''

    try:
        myopts, args = getopt.getopt(sys.argv[1:], "b:s:o:")
    except getopt.GetoptError as e:
        print(str(e))
        print("""Usage: %s 
        -b path to MRI T1-w scan (nii or nii.gz file)
        -o output directory""" % sys.argv[0])
        sys.exit(2)

    for option, argument in myopts:
        if ((option == "-b") and isfile(argument) and allowed_file(argument)):
            baselineFile = argument
        elif ((option == "-s") and (argument in ISMETHODS)):
            isMethod = argument
        elif ((option == "-o") and exists(argument)):
            outputDir = argument
        else:
            print("""Usage: %s  
        -b path to MRI T1-w scan (nii or nii.gz file)
        -o output directory""" % sys.argv[0])
            break

    run_intensity_delis(baselineFile, outputDir)


if __name__ == "__main__":
    main()
