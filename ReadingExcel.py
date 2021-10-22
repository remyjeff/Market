import pandas as pd

def readExcel():
    df = pd.read_excel('./Stocks/AAPL/Final1.xlsx')
    for d in df.index:
        print(df["Datetime"][d], df["Open"][d], df["High"][d], df["Low"][d], df["Close"][d], df["Volume"][d])
        return f"""(2, {["Datetime"][d]}, {df["Open"][d]}, {df["High"][d]}, {df["Low"][d]}, {df["Close"][d]}, {df["Volume"][d]})"""


if __name__ == "__main__":
    readExcel()