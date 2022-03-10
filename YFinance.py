import datetime
import yfinance as yf
import pandas as pd
import time
class YFinance():
    def __init__(self, ticker) -> None:
        self.ticker = ticker
    #
    def getLast5Days(self): # returns a dictionary with the ticker name as key and dataframe as value.
        result = {}
        s = yf.download(tickers=self.ticker, period='5d', interval='1m')
        s = s.tz_localize(None) # This is to set the time format.
        s.to_excel(f"./Stocks/{self.ticker}/Minute.xlsx", index=True)
        #s.to_excel(f"Stocks/{self.ticker}/Final1.xlsx", index=True)
    #
    def getLast60Days(self):
        result = yf.download(tickers=self.ticker, period='60d', interval='2m')
        result = result.tz_localize(None) # This is to set the time format.
        result.to_excel(f"./Stocks/{self.ticker}/TwoMinute.xlsx", index=True)
        #result.to_excel(f"Stocks/{self.ticker}/Final60.xlsx", index=True)
        time.sleep(1)
    #
    def getHighLow(self):
        historical = yf.download(tickers=self.ticker, period="6mo", interval="1d")
        historical.to_excel(f"./Stocks/{self.ticker}/HighLow.xlsx", index=False)
        self.updateStatistic()
    # 
    def getOptionDates(self):
        return yf.Ticker(self.ticker).options # returns (date0, date1 --- date_n)
    #    
    def getCallOptionChain(self, date):
        s = yf.Ticker(self.ticker).option_chain(date).calls
        #s.plot()
        return s
    #    
    def getPutOptionChain(self, date):
        return yf.Ticker(self.ticker).option_chain(date).puts
    #
    def updateStatistic(self):
            df = pd.DataFrame()
            main = pd.read_excel(f"./Stocks/{self.ticker}/HighLow.xlsx")["Open"].describe().to_json(indent=0)
            self.writeJson(main, f"./Stocks/{self.ticker}/Statistic.json")
    # writes json_status to fileName.json
    def writeJson(self, json_status, fileName):
        with open(fileName, "w") as statusFile:
            statusFile.write(json_status)
            statusFile.close()
    # Not sure if this is going to be needed.
    def joinData(self, n):
        f1 = pd.read_excel(f"Stocks/{self.ticker}/Final{n}.xlsx")
        f2 = pd.read_excel(f"Stocks/{self.ticker}/{self.ticker}_{n}m.xlsx")
        f3 = f1.append(f2)
        f3.drop_duplicates() # last added.
        f3.to_excel(f"Stocks/{self.ticker}/{self.ticker}Final{n}.xlsx", index=False)

if __name__ == "__main__":
    Y = YFinance("AAPL")
    d = str(datetime.datetime.now())[:10]
    print(Y.getCallOptionChain(Y.getOptionDates()[0]))