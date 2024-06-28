import sys
import os
import datetime
import pathlib
import shutil
import csv


def getFiles(directory):
    files = [f for f in pathlib.Path(directory).iterdir() if f.is_file()]
    return files


def writeDataToCsv(data, fileName):
    currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    directory = outputFileName = os.path.join(os.getcwd(), "output")
    if not os.path.exists(directory):
        os.mkdir(directory)

    outputFileName = os.path.join(
        directory, ("{time}_{file}").format(time=currentTime, file=fileName)
    )

    with open(outputFileName, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["jobName", "sourceFileName", "targetFileName", "sNode"],
        )

        writer.writeheader()
        writer.writerows(data)

    return outputFileName


def extractScriptToCsv(directory):
    fileContents = []

    for f in getFiles(directory):
        # Read file content
        with open(f, "r") as fp:
            # content = fp.read()
            lines = fp.readlines()

            # Find keywords "SNODE=", "&FR", "&TO"
            sNodeKeywordResults = list(
                filter(lambda c: str(c).find("SNODE=") > -1, lines)
            )
            frKeywordResults = list(filter(lambda c: str(c).find("&FR") > -1, lines))
            toKeywordResults = list(filter(lambda c: str(c).find("&TO") > -1, lines))

            fileContents.append(
                {
                    "jobName": pathlib.Path(f).stem,
                    "sourceFileName": (
                        frKeywordResults[0].strip() if len(frKeywordResults) > 0 else ""
                    ),
                    "targetFileName": (
                        toKeywordResults[0].strip() if len(toKeywordResults) > 0 else ""
                    ),
                    "sNode": (
                        sNodeKeywordResults[0].strip()
                        if len(sNodeKeywordResults) > 0
                        else ""
                    ),
                }
            )

    writeDataToCsv(fileContents, "direct-connect-extracted.csv")

    # print(("FileName: {file}").format(file=f.stem))


if len(sys.argv) > 1 and sys.argv[1] != "":
    extractScriptToCsv(sys.argv[1])
    print("Extract Direct Connect Script successful.")
