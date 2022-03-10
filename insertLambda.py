import json
import sys
import logging
import rds_config
import pymysql
import datetime
from StockDB import *
# rds settings

rds_host = rds_config.db_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()


def readTable():
    select_stocks = """
    SELECT * FROM TWO_MINUTE;"""
    stocks = []
    with conn.cursor() as cur:
        cur.execute(select_stocks)
        for row in cur:
            stocks.append(row)
    return stocks


logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    i = 0
    with conn.cursor() as cur:
        conn.commit()
        statement = f'INSERT INTO {event["table"]} VALUES '
        for el in event["data"]:
            temp = statement + str(el)
            cur.execute(temp)
            i += 1
            if i % 1000 == 0:
                print(f"{i} amount has been pushed.")
                conn.commit()
    conn.commit()
    conn.close()

    return {
        'statusCode': 200,
        "header": {},
        "body": json.dumps({"message": "Successful", "data":len(event["data"])})
    }

# print(lambda_handler(event, None))

# TABLE = "TWO_MINUTE"
# connection = create_connection("localhost", "root", "", "STOCK_MARKET")
# select_stocks = """
# SELECT * FROM TWO_MINUTE;"""
# stocks = execute_read_query(connection, select_stocks)
# stocks = getDateFormat(stocks)
# event = {"table": TABLE, "data":stocks, "etc": {}}
# print(lambda_handler(event, None))