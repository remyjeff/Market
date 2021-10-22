import pandas as pd

def readExcel(filePath):
    df = pd.read_excel(filePath)
    result = []
    for d in df.index:
        if d != 0:
            #print(df["Datetime"][d], df["Open"][d], df["High"][d], df["Low"][d], df["Close"][d], df["Volume"][d])
            RESULT = f"""(1, '{df["Datetime"][d]}', {df["Open"][d]}, {df["High"][d]}, {df["Low"][d]}, {df["Close"][d]}, {df["Volume"][d]})"""
            result.append(RESULT)
    return result


if __name__ == "__main__":
    readExcel()