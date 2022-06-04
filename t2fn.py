import os
import datetime

class TimestampFileRenamer:
    signature = "#+#"
    debugoutputs = False
    fileextensions = ""
    simulation = False

    def __init__(self, fileextensions, debugoutputs = False, simulation = False):
        self.fileextensions = fileextensions.split(" ")
        self.debugoutputs = debugoutputs
        self.simulation = simulation
        self.debugprint(f"{self} created.")

    def debugprint(self, *text):
        if self.debugoutputs:
            for x in text:
                print(x, end='')
                print()
        return

    def timestamp2string(self, timestamp):
        mstamp = datetime.datetime.fromtimestamp(timestamp)
        return str(mstamp).replace(" ", "#").replace(":", "_")

    def renamefile(self, targetfile, newname):
        os.rename(targetfile, newname)

    def run(self):
        for file in os.listdir():
            for fe in self.fileextensions:
                if file.endswith(fe) and not file.startswith(self.signature):
                    fullpath = os.path.abspath(file)
                    self.debugprint("\n"+fullpath)

                    atime = os.path.getatime(fullpath) # last access
                    mtime = os.path.getmtime(fullpath) # last modification
                    ctime = os.path.getctime(fullpath) # last creation time [win] or metadata modification [lin]
                    mintime = min(atime, mtime, ctime) # the "earliest"

                    self.debugprint("mtime: "+str(mtime) + "\nctime: "+str(ctime) + "\natime: "+str(atime))
                    self.debugprint(f"min equals {mintime}")

                    mstamp = self.timestamp2string(mintime)
                    
                    newfilename = self.signature + mstamp + f".{fe}"
                    self.debugprint(f"{file} --> {newfilename}")
                    if not self.simulation:
                        self.renamefile(file, newfilename)
                        print(f"<file '{file}' renamed to '{newfilename}'>")
                    else:
                        print(f"<file '{file}' NOT renamed to '{newfilename}'>")
                    break
        print("ok")
