import mysql.connector
from mysql.connector import Error
from ReadingExcel import readExcel
 
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
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
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
        data = readExcel(f"./Stocks/{ticker}/{fileName}.xlsx")
        for d in data:
            inserting = f"""
            INSERT INTO {table}(Id, Datetime, Open, High, Low, Close, Volume)
            VALUES
            {d};
            """
            execute_query(connection, inserting)  
    #select_stocks = "SELECT * from TWO_MINUTE"
    #stocks = execute_read_query(connection, select_stocks)
    #for user in stocks:
        #print(user)

def pushStock(stocks):
    connection = create_connection("localhost", "root", "", "STOCK_MARKET")
    for d in stocks:
            inserting = f"""
            INSERT INTO STOCKS(Ticker)
            VALUES
            ('{d}');
            """
            execute_query(connection, inserting)

#pushDataToDB()
stocks = ["NVDA", "TSLA", "AAPL", "PLTR", "ACB", "TLRY", "RTX", "BA", "NFLX", "SPY", "FSLY", "JKS", "PLUG", "FCEL"]
#pushStock(stocks)
