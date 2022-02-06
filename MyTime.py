import time, datetime
import json
from StockDB import *



# loads the last date, data was collected from yf.
def loadJson(fPath, name):
    if type(name) is list:
        result = []
        for n in name:
            with open(fPath(n), "r") as statusFile:
                result.append(json.load(statusFile))
                statusFile.close()
        return result
    with open(fPath(name), "r") as statusFile:
        me = json.load(statusFile)
        statusFile.close()
        return me

currentDate = loadJson(lambda name: name, "currentDate.json")

def getDigits( num):
    if (num / 10) < 1:
        return "0"+str(num)
    return str(num)

#
def getStringOfDate(date):
    res = "" + str(date.year) + "-" + getDigits(date.month) + "-" + getDigits(date.day) + " 16:00:00.000000"
    return res

#
def dateAddition(fileName):
    if fileName == "date60":
        day60 = datetime.datetime.fromisoformat(currentDate["date60"]) + datetime.timedelta(60)
        currentDate[fileName] = getStringOfDate(day60)
    elif fileName == "date7":
        day7 = datetime.datetime.fromisoformat(currentDate["date7"]) + datetime.timedelta(7)
        currentDate[fileName] = getStringOfDate(day7)
    else:
        print(f"Wrong date file: <{fileName}>")

#    
def looper(self):
    day = time.strftime('%A')
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    week2 = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    today = datetime.date.today().ctime().split(" ")
    print('ctime:', today)
    time.sleep(604800)

# updates the status.json that keeps track of the dates for gathering data from yf.
def updateStatus(currentDate, fileName):
    #status = {"date7": "2021-08-21 16:00:00.000000","date60": "2022-10-13 16:00:00.000000"}
    dateAddition(fileName)
    json_status = json.dumps(currentDate, indent=4)
    writeJson(json_status, "currentDate.json")
    currentDate = loadJson(lambda name: name, "currentDate.json")

def writeJson(json_status, fileName):
    with open(fileName, "w") as statusFile:
        statusFile.write(json_status)
        statusFile.close()

# Calculates the difference between the next date and now, and then sleep for the result.
def sleepTime(fileName):
    day = datetime.datetime.fromisoformat(currentDate[fileName]) - datetime.datetime.now()
    seconds = day.total_seconds()
    print(f"Sleeping for : {seconds}")
    time.sleep(seconds)


def getDate():
    return loadJson(lambda name: name, "currentDate.json")