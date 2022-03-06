# import pandas as pd
# from StockDB import create_connection, dateValidation
# from StockDB import execute_query

# def readExcel(id, filePath):
#     connection = create_connection("localhost", "root", "", "STOCK_MARKET")
#     df = pd.read_excel(filePath)
#     result = []
#     if (not dateValidation(df["Datetime"][d].strftime("%x"))):
#         inserting = f"""
#             INSERT INTO DATES(Date)
#             VALUES
#             ('{d}');
#             """
#         execute_query(connection, inserting)

#     for d in df.index:
#         if d != 0:
#             #print(df["Datetime"][d], df["Open"][d], df["High"][d], df["Low"][d], df["Close"][d], df["Volume"][d])
#             RESULT = f"""({id}, '{df["Datetime"][d]}', {df["Open"][d]}, {df["High"][d]}, {df["Low"][d]}, {df["Close"][d]}, {df["Volume"][d]})"""
#             result.append(RESULT)
#     return result

# if __name__ == "__main__":
#     readExcel()