import sys
import os
import datetime
import pathlib
import shutil
import re
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
            fieldnames=[
                "jobName",
                "sourceFileName",
                "targetFileName",
                "pNode",
                "sNode",
            ],
        )

        writer.writeheader()
        writer.writerows(data)

    return outputFileName


def generalCleanupContent(content: str):
    # contentResult = content.strip().replace("\\", "")
    contentResult = content.strip()

    if contentResult.endswith("-"):
        contentResult = contentResult[0 : len(contentResult) - 1].strip()

    return contentResult


def sourceTargetCleanupContent(contents: list[str], mainIndex: int) -> str:
    # Replace &FR
    contentResult = re.sub(r"&FR\d+=", "", contents[mainIndex].strip())

    # Replace &TO
    contentResult = re.sub(r"&TO\d+=", "", contentResult.strip())

    contentResult = generalCleanupContent(contentResult)

    # Check endswith '||' (Have next lines)
    if contentResult.strip().endswith("||"):
        contentResult = contentResult[0 : len(contentResult) - 2].strip()
        contentResult = contentResult + generalCleanupContent(contents[mainIndex + 1])

        if contentResult.strip().endswith("||"):
            contentResult = contentResult[0 : len(contentResult) - 2].strip()
            contentResult = contentResult + generalCleanupContent(
                contents[mainIndex + 2]
            )

            if contentResult.strip().endswith("||"):
                contentResult = contentResult[0 : len(contentResult) - 2].strip()
                contentResult = contentResult + generalCleanupContent(
                    contents[mainIndex + 3]
                )

    return contentResult


def extractScriptToCsv(directory):
    fileContents = []

    # Looping files
    for f in getFiles(directory):
        # Read file content
        with open(f, "r") as fp:
            # content = fp.read()
            lines = fp.readlines()

            # Find keywords "&FR" (Excluded comment lines)
            frKeywordIndexes = list(
                filter(
                    lambda i: lines[i].find("&FR") > -1
                    and not lines[i].strip().startswith("//")
                    and not lines[i].strip().startswith("/*"),
                    range(len(lines)),
                )
            )

            # Find keywords "&TO" (Excluded comment lines)
            toKeywordIndexes = list(
                filter(
                    lambda i: lines[i].find("&TO") > -1
                    and not lines[i].strip().startswith("//")
                    and not lines[i].strip().startswith("/*"),
                    range(len(lines)),
                )
            )

            # Find keywords "PNODE=" (Excluded comment lines)
            pNodeKeywordIndexes = list(
                filter(
                    lambda i: lines[i].find("PNODE=") > -1
                    and not lines[i].strip().startswith("//")
                    and not lines[i].strip().startswith("/*"),
                    range(len(lines)),
                )
            )

            # Find keywords "SNODE=" (Excluded comment lines)
            sNodeKeywordIndexes = list(
                filter(
                    lambda i: lines[i].find("SNODE=") > -1
                    and not lines[i].strip().startswith("//")
                    and not lines[i].strip().startswith("/*"),
                    range(len(lines)),
                )
            )

            # Looping &FR keywords
            variableIndex = 1
            for mainIndex in frKeywordIndexes:
                fileContents.append(
                    {
                        "jobName": pathlib.Path(f).stem,
                        "sourceFileName": sourceTargetCleanupContent(lines, mainIndex),
                        "targetFileName": sourceTargetCleanupContent(
                            lines, toKeywordIndexes[variableIndex - 1]
                        ),
                        "pNode": (
                            generalCleanupContent(lines[pNodeKeywordIndexes[0]])
                            if len(pNodeKeywordIndexes) > 0
                            else ""
                        ),
                        "sNode": (
                            generalCleanupContent(lines[sNodeKeywordIndexes[0]])
                            if len(sNodeKeywordIndexes) > 0
                            else ""
                        ),
                    }
                )
                print(
                    ("Extract script:{script} success..").format(
                        script=pathlib.Path(f).stem
                    )
                )
                if variableIndex < len(frKeywordIndexes):
                    variableIndex += 1

    # Write to CSV file
    writeDataToCsv(fileContents, "direct-connect-extracted.csv")


if len(sys.argv) > 1 and sys.argv[1] != "":
    extractScriptToCsv(sys.argv[1])
    print("Extract all scripts successful.")
