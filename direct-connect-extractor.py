import sys
import pathlib


def getFiles(directory):
    files = [f for f in pathlib.Path(directory).iterdir() if f.is_file()]
    return files


def extractScriptToCsv(directory):
    for f in getFiles(directory):
        # Read file content
        with open(f, "r") as fp:
            # content = fp.read()
            lines = fp.readlines()

            results = list(filter(lambda c: str(c).find("&FR") > -1, lines))

            print(("FileName: {file}").format(file=f.stem))


if len(sys.argv) > 1 and sys.argv[1] != "":
    extractScriptToCsv(sys.argv[1])
    print("Extract Direct Connect Script successful.")
