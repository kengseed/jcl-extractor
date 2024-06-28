import sys
import os
import datetime
import pathlib
import shutil
import csv


def getFiles(directory):
    files = [f for f in pathlib.Path(directory).iterdir() if f.is_file()]
    return files


def moveFile(sourceFileName, sourceFilePath, targetDirectory):
    # Check source file is exist
    if not os.path.exists(sourceFilePath):
        return ""

    # Create directory is not exist
    directory = os.path.join(sourceFilePath, targetDirectory)
    if not os.path.exists(directory):
        os.mkdir(directory)

    # Move file to target directory
    shutil.move(sourceFilePath, os.path.join(directory, sourceFileName))
    return sourceFileName


def moveFilesByCsvList(csvBaseFile, sourceDirectory, targetDirectory):
    with open(csvBaseFile, newline="") as file:
        reader = csv.reader(file, delimiter=",")

        for row in reader:
            if reader.line_num > 1:
                sourceFile = os.path.join(sourceDirectory, row[1])

                movedFile = moveFile(row[1], sourceFile, targetDirectory)
                if len(movedFile) > 0:
                    print(("Moved {file} success").format(file=movedFile))


def listFileNames(directory):
    fileNames = []
    for f in getFiles(directory):
        fileNames.append(os.path.basename(f) + "\n")

    outputFile = os.path.join(directory, "file-list.txt")
    with open(outputFile, "w") as fp:
        fp.writelines(fileNames)


# moveFilesByCsvList(sys.argv[2], sys.argv[1], sys.argv[3])
# listFileNames(sys.argv[1])
print("All Operation Successful.")
