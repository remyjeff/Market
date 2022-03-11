from YFinance import *
import time

def scan():
    lst = []
    with open("NYSE", "r") as f:
        for l in f:
            s = l.strip()
            # print(yf.Ticker(s).info["volume"])
            Y = YFinance(s)
            lst.append(Y)
    return lst


def volumeScanner(lst):
    result = []
    for l in lst:
        if (l.getInfo()["averageVolume"] <= l.getInfo()["volume"] * 1.025):
            print(l.ticker, " has high volume. CHECK NEWS OUTLETS.")
            result.append(l.ticker)
    return result

if __name__ == "__main__":
    while(True):
        volumeScanner(scan())
        time.sleep(300)
