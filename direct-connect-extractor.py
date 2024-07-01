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
    contentResult = content.strip().replace("\\", "")

    if contentResult.endswith("-"):
        contentResult = contentResult[0 : len(contentResult) - 1].strip()
        if contentResult.strip().endswith("||"):
            contentResult = contentResult[0 : len(contentResult) - 2].strip()

    return contentResult


def cleanupContent(content: str, index: int) -> str:
    # Replace &FR
    contentResult = content.strip().replace(("&FR{index}=").format(index=index), "")
    # contentResult = contentResult.strip().replace(
    #     ("&FR{index}=\'").format(index=index), ""
    # )

    # Replace &TO
    contentResult = contentResult.strip().replace(
        ("&TO{index}=").format(index=index), ""
    )
    # contentResult = contentResult.strip().replace(
    #     ("&TO{index}=\\'").format(index=index), ""
    # )

    return generalCleanupContent(contentResult)


def extractScriptToCsv(directory):
    fileContents = []

    # Looping files
    for f in getFiles(directory):
        # Read file content
        with open(f, "r") as fp:
            # content = fp.read()
            lines = fp.readlines()

            # Find keywords "PNODE=" (Excluded comment lines)
            pNodeKeywordResults = list(
                filter(
                    lambda c: str(c).find("PNODE=") > -1
                    and not str(c).strip().startswith("//")
                    and not str(c).strip().startswith("/*"),
                    lines,
                )
            )
            # Find keywords "SNODE=" (Excluded comment lines)
            sNodeKeywordResults = list(
                filter(
                    lambda c: str(c).find("SNODE=") > -1
                    and not str(c).strip().startswith("//")
                    and not str(c).strip().startswith("/*"),
                    lines,
                )
            )
            # Find keywords "&FR" (Excluded comment lines)
            frKeywordResults = list(
                filter(
                    lambda c: str(c).find("&FR") > -1
                    and not str(c).strip().startswith("//")
                    and not str(c).strip().startswith("/*"),
                    lines,
                )
            )
            # Find keywords "&TO" (Excluded comment lines)
            toKeywordResults = list(
                filter(
                    lambda c: str(c).find("&TO") > -1
                    and not str(c).strip().startswith("//")
                    and not str(c).strip().startswith("/*"),
                    lines,
                )
            )

            # Looping &FR keywords
            for i in range(len(frKeywordResults)):
                fileContents.append(
                    {
                        "jobName": pathlib.Path(f).stem,
                        "sourceFileName": cleanupContent(frKeywordResults[i], i + 1),
                        "targetFileName": cleanupContent(toKeywordResults[i], i + 1),
                        "pNode": (
                            generalCleanupContent(pNodeKeywordResults[0])
                            if len(pNodeKeywordResults) > 0
                            else ""
                        ),
                        "sNode": (
                            generalCleanupContent(sNodeKeywordResults[0])
                            if len(sNodeKeywordResults) > 0
                            else ""
                        ),
                    }
                )

    # Write to CSV file
    writeDataToCsv(fileContents, "direct-connect-extracted.csv")


if len(sys.argv) > 1 and sys.argv[1] != "":
    extractScriptToCsv(sys.argv[1])
    print("Extract Direct Connect Script successful.")
