import subprocess, json, sys, path
import os, errno


def makeNewFolder(fPath, folder): # Creates new files accepts both a list.
    if type(folder) is list:
        for f in folder:
            try:
                os.makedirs(fPath(f), )
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
    else:
        try:
            os.makedirs(fPath(folder))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def renameFiles(fPath, oldFPath, stocks): # Renaming old files with new ones.
    for name in stocks:
        old_name = oldFPath(name) #r""+name + "/" + name + ".csv"
        new_name = fPath(name)    #r""+name + "/" + name + "_" +str(s) + "m.csv"
        if os.path.isfile(new_name):
            print("The file already exists")
        else:
            os.rename(old_name, new_name)

def newFiles(fPath, name):  # Creates new files from a list of names and file path.
        try:
            for file in name:
                f = open(fPath(file), "x")
                f.close()
        except:
            print("File path does not exit! and names is not a list. --> [names]")

def deleteOldFiles(fPath, names): # fPath is the file path where to delete the files.
    for name in names:
        p1 = fPath(name)
        if os.path.exists(p1):
            os.remove(p1)
        else:
            print(f"{p1} does not exist!")
#
if __name__ == "__main__":
    # makeNewFolder(lambda name : f"Stocks/"+name, ["NVDA"])
    # newFiles(lambda name: f"Stocks/{name}/{name}Final.xlsx", ["NVDA"])
    # deleteOldFiles(lambda name: f"Stocks/{name}/{name}Final.xlsx", ["NVDA"])
    pass