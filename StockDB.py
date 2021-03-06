import mysql.connector
import pandas as pd
from mysql.connector import Error
# from ReadingExcel import readExcel
 
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query) # error is here.
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def pushDataToDB(stocks, table, fileName):
    connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    for ticker in stocks:
        id = getId(ticker)
        data = readExcel(id, f"./Stocks/{ticker}/{fileName}.xlsx")
        for d in data:
            inserting = f"""
            INSERT INTO {table}(Id, Datetime, Open, High, Low, Close, Volume)
            VALUES
            {d};
            """
            execute_query(connection, inserting)  

def pushStock(stocks):
    connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    for d in stocks:
            inserting = f"""
            INSERT INTO STOCKS(Ticker)
            VALUES
            ('{d}');
            """
            execute_query(connection, inserting)
    print(stocks, " got added to STOCKS")

def getId(name):
    connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    select_stocks = """
    SELECT * FROM STOCKS;"""
    stocks = execute_read_query(connection, select_stocks)
    for user in stocks:
        if name == user[1]:
            return user[0]
    
def isInStocks(name):
    connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    select_stocks = """
    SELECT * FROM STOCKS;"""
    stocks = execute_read_query(connection, select_stocks)
    for user in stocks:
        if name == user[1]:
            return True
    return False

def dateValidation(name):
    connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    select_stocks = """
    SELECT * FROM DATES;"""
    stocks = execute_read_query(connection, select_stocks)
    for user in stocks:
        if (name == user[0]):
            return True
    return False

def readExcel(id, filePath):
    #connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    df = pd.read_excel(filePath)
    result = []
    for d in df.index:
        if d != 0:
            #print(df["Datetime"][d], df["Open"][d], df["High"][d], df["Low"][d], df["Close"][d], df["Volume"][d])
            RESULT = f"""({id}, '{df["Datetime"][d]}', {df["Open"][d]}, {df["High"][d]}, {df["Low"][d]}, {df["Close"][d]}, {df["Volume"][d]})"""
            result.append(RESULT)
    return result

def getDateFormat(stock):
    stocks = stock
    for i in range(len(stocks)):
        temp = list(stocks[i])
        print(temp)
        #print(stock)
        #temp[1] = temp[1].strftime("%Y-%m-%d %H:%M:%S")
        #stocks[i] = tuple(temp)
    return stocks