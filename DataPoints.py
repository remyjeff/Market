# Raw Package
import pandas as pd
import time, datetime
import os, errno
import subprocess, json, sys
from FileManagement import makeNewFolder, newFiles
from MyTime import *
import yfinance as yf
from multiprocessing import Process, Lock
from YFinance import YFinance
from StockDB import *
import rds_config
from pushToAWSDB import AwsResource

class Nasdaq:
    def __init__(self, listName):
        self.stocks = self.read(listName) #["NVDA", "TSLA", "AAPL", "PLTR", "ACB", "TLRY", "RTX", "BA", "NFLX", "SPY", "FSLY", "JKS", "PLUG", "FCEL", "FB"]
        #self.insertStockIfNotInTable()
        self.counter = 0
        currentDate = getDate()
        self.lock = False
        #self.run("date7")
        #self.weekStatistic()
        self.start()
        #dateValidation("02/02/22")
    # # git commands
    def runIt(self, *args):
        return subprocess.check_call(['git'] + list(args))
    #
    def read(self, listName):
        lst = []
        with open("stocklist", 'r') as file:
            for line in file:
                lst.append(line.strip("\n"))
        return lst
    #
    def insertStockIfNotInTable(self):
        for name in self.stocks:
            if not isInStocks(name):
                pushStock([name])
                makeNewFolder(lambda name : f"Stocks/"+name, [name])
                newFiles(lambda name: f"Stocks/{name}/Minute.xlsx", [name])
                newFiles(lambda name: f"Stocks/{name}/TwoMinute.xlsx", [name])
                newFiles(lambda name: f"Stocks/{name}/HighLow.xlsx", [name])  
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
    def weekStatistic(self):
        #R = Robin() #TODO robinhood api is not working.
        price = [x*x+100 for x in range(20)]#R.getLatestPrice(self.stocks)
        statistic = loadJson(lambda n : f"Stocks/{n}/Statistic.json", self.stocks)
        self.filter(price, statistic)
    #
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
    # reads all of the excel files and combines into a single. might have to check the datetime format.
    def getAllExcel(self, event, fileName):
        A = AwsResource(event)
        Id = {}
        for n in A.readTable({"table":"STOCKS"}):
            Id[n[1]] = n[0]
        result = []
        for ticker in self.stocks:
            result.append(readExcel(Id[ticker], f"./Stocks/{ticker}/{fileName}.xlsx"))
        A.close()
        return result
    #
    def run(self, name):
        while(True):
            print(f"Running {name} Thread!")
            #sleepTime(name)
            event = {
                "rds_host" : "market.cucrygetviqs.us-east-1.rds.amazonaws.com",
                "name": rds_config.db_username,
                "password": rds_config.db_password,
                "db_name": rds_config.db_name,
                "table": "",
                "data": []
            }
            i = 2
            if (name == "date7"):
                for n in self.stocks:
                    M1 = YFinance(n)
                    M1.getLast5Days()
                    M1.getHighLow()
                #pushDataToDB(self.stocks, "MINUTE", "Minute")
                event["table"] = "MINUTE"
                event["data"] = self.getAllExcel(event, "Minute")
            else:
                i = 1
                for n in self.stocks:
                    M2 = YFinance(n)
                    M2.getLast60Days()
                #pushDataToDB(self.stocks, "TWO_MINUTE", "TwoMinute")
                event["table"] = "TWO_MINUTE"
                event["data"] = self.getAllExcel("TwoMinute")
            AWS = AwsResource(event, None)
            AWS.lambda_handler(event, None)
            AWS.close()
            AWS = None
            # I have to push these files into the database first before I do anything else.
            #self.deleteOldFiles(i)
            print("Updating next date for : ", name)
            while(self.lock):
                print("Lock is on!")
                time.sleep(3)
            self.lock = True
            updateStatus(currentDate, name)
            self.lock = False
            self.clear()
        
            self.runIt("add", ".")
            self.runIt("commit", "-m", f"This is the {self.counter}th saving data.")
            self.counter += 1
            print("Done Running: ", name)
    #
    def start(self):
        print(f"Running Start.")
        try:
            p0 = Process(target=self.run, args=('date7',))
            p0.start()
            time.sleep(3)
            p1 = Process(target=self.run, args=('date60',))
            p1.start()
        except:
            print("Error: Unable to start thread.")
if __name__ == '__main__':
    N1 = Nasdaq("stocklist")
    #N1.weekStatistic() # TODO : need to reimplement this function.


