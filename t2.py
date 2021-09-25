# Raw Package
import pandas as pd
import time, datetime
import os, errno
import subprocess, json, sys, path
from robin import Robin
import yfinance as yf
from multiprocessing import Process
from YFinance import YFinance

class Nasdaq:
    def __init__(self):
        self.stocks = ["TSLA", "AAPL", "PLTR", "ACB", "TLRY", "RTX", "BA", "NFLX", "SPY", "FSLY", "JKS", "PLUG", "FCEL"]
        self.counter = 0
        self.currentDate = self.loadJson(lambda name: name, "currentDate.json")
        self.start()
    #
    def getDigits(self, num):
        if (num / 10) < 1:
            return "0"+str(num)
        return str(num)
    #
    def getStringOfDate(self, date):
        res = "" + str(date.year) + "-" + self.getDigits(date.month) + "-" + self.getDigits(date.day) + " 16:00:00.000000"
        return res
    #
    def dateAddition(self, fileName):
        if fileName == "date60":
            self.day60 = datetime.datetime.fromisoformat(self.currentDate["date60"]) + datetime.timedelta(60)
            self.currentDate[fileName] = self.getStringOfDate(self.day60)
        elif fileName == "date7":
            self.day7 = datetime.datetime.fromisoformat(self.currentDate["date7"]) + datetime.timedelta(7)
            self.currentDate[fileName] = self.getStringOfDate(self.day7)
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
    #
    def makeNewFolder(self, folder):
        if type(folder) is list:
            for f in folder:
                try:
                    os.makedirs("Stocks/"+f)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
        else:
            try:
                os.makedirs("Stocks/"+folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
    #
    def renameFiles(self, s):
        for name in self.stocks:
            old_name = r""+name + "/" + name + ".csv"
            new_name = r""+name + "/" + name + "_" +str(s) + "m.csv"
            if os.path.isfile(new_name):
                print("The file already exists")
            else:
                os.rename(old_name, new_name)
    #
    def newFiles(self, first, last, extension):
        if type(first) is list:
            for file in first:
                f = open(file + "/" + file + last + extension, "x")
                f.close()
        else:
            f = open(first + "/" + first + last + extension, "x")
            f.close() 
    #
    def deleteOldFiles(self, s): # s is the minute reference.
        for name in self.stocks:
            p1 = f"Stocks/{name}/{name}_2m.xlsx"
            p2 = f"Stocks/{name}/{name}_1m.xlsx"
            if os.path.exists(p1):
                os.remove(p1)
            if os.path.exists(p2):
                os.remove(p2)
            else:
                print(f"{p2} does not exist!")
    # git commands
    def runIt(self, *args):
        return subprocess.check_call(['git'] + list(args))
    # loads the last date, data was collected from yf.
    def loadJson(self, fPath, name):
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
    # writes json_status to fileName.json
    def writeJson(self, json_status, fileName):
        with open(fileName, "w") as statusFile:
            statusFile.write(json_status)
            statusFile.close()
    # updates the status.json that keeps track of the dates for gathering data from yf.
    def updateStatus(self, fileName):
        #status = {"date7": "2021-08-21 16:00:00.000000","date60": "2022-10-13 16:00:00.000000"}
        self.dateAddition(fileName)
        json_status = json.dumps(self.currentDate, indent=4)
        self.writeJson(json_status, "currentDate.json")
    # Calculates the difference between the next date and now, and then sleep for the result.
    def sleepTime(self, fileName):
        day = datetime.datetime.fromisoformat(self.currentDate[fileName]) - datetime.datetime.now()
        seconds = day.total_seconds()
        print(f"Sleeping for : {seconds}")
        time.sleep(seconds)
    # returns a list of dataframe made from the excel sheets from all of the stocks.
    def filter(self, price, statistic):
        lessThanMean = [price[i] < statistic[i]["mean"] for i in range(len(self.stocks))]
        lessThan50 = [price[i] < statistic[i]["50%"] for i in range(len(self.stocks))]
        greaterThan75 = [price[i] > statistic[i]["75%"] for i in range(len(self.stocks))]
        lessThan50By5Percent = [price[i] < (statistic[i]["50%"]*0.95) for i in range(len(self.stocks))]
        for i in range(len(self.stocks)):
            if lessThan50By5Percent[i]:
                print(f"{self.stocks[i]} :: STRONG BUY :: CHECK RECENT NEWS!")
                continue
            elif lessThan50[i]:
                print(f"{self.stocks[i]} :: MODERATE BUY :: CHECK RECENT NEWS!")
                continue
            elif lessThanMean[i]:
                print(f"{self.stocks[i]} :: BUY :: CHECK RECENT NEWS!")
                continue
            elif greaterThan75[i]:
                print(f"{self.stocks[i]} :: STRONG SELL :: CHECK RECENT NEWS!")
                continue
            else:
                print(f"{self.stocks[i]} :: STRONG SELL :: CHECK RECENT NEWS!")
    #
    def averageDiff(self, extension):
        arr = {}
        for name in self.stocks:
            path = "temp/"+name+extension #f"{name}/{name}{extension}"
            if "xlsx" in extension:
                df = pd.read_excel(path)
            else:
                df = pd.read_csv(path)
            diff = 0
            count = 0
            streak = 0
            streakArr = []
            for i in range(len(df)):
                diff += df["High"][i] - df["Low"][i]
                if (df["Close"][i] - df["Open"][i]) > 0:
                    count += 1
                    streak += 1
                else: 
                    count -= 1
                    streakArr.append(streak)
                    streak = 0
                #print(f"{df['High'][i]} - {df['Low'][i]}", df["High"][i] - df["Low"][i])
            arr[name] = {"averageDiff":diff / len(df), "count":count, "streak": sum(streakArr)/len(streakArr)}
        return arr
    #
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
    #
    def run(self, name):
        #R = Robin()
        while(True):
            print(f"Running {name} Thread!")
            self.sleepTime(name)
            i = 2
            if (name == "date7"):
                #R.signIn()
                for name in self.stocks:
                    M1 = YFinance(name)
                    M1.getLast5Days()
                    M1.joinData(1)
                    M1.getHighLow()
                    pass
            else:
                for name in self.stocks:
                    M1 = YFinance(name)
                    M1.getLast60Days()
                    M1.joinData(60)
                    pass
            self.deleteOldFiles(i)
            
            self.clear()
            #price = R.getLatestPrice(self.stocks)
            #statistic = self.loadJson(lambda n : f"Stocks/{n}/{n}_Statistic.json", self.stocks)
            #self.filter(price, statistic)
            #R.signOut()
        
            #self.runIt("add", ".")
            #self.runIt("commit", "-m", f"This is the {self.counter}th saving data.")
            self.counter += 1
            break
    #
    def start(self):
        print(f"Running Start.")
        try:
            p0 = Process(target=self.run, args=('date7',))
            p0.start()
            p1 = Process(target=self.run, args=('date60',))
            p1.start()
        except:
            print("Error: Unable to start thread.")
if __name__ == '__main__':
    N1 = Nasdaq()


