import logging
import json
import sys
import pymysql
from StockDB import *
import rds_config

class AwsResource:
    #
    def __init__(self, event, context=None):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  
        try:
            self.conn = pymysql.connect(host=event["rds_host"], user=event["name"], passwd=event["password"], db=event["db_name"], connect_timeout=5)
            logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            sys.exit()
        #self.lambda_handler(event, None)
        #self.readTable(event)
        #self.getId("AAPL")
    #
    def close(self):
        self.conn.close()
    #
    def readTable(self, event):
        statement = f"""SELECT * FROM {event["table"]}"""
        stocks = []
        with self.conn.cursor() as cur:
            cur.execute(statement)
            for row in cur:
                stocks.append(row)
        print(len(stocks))
        return stocks
    #
    def getId(self, name):
        load = self.readTable({"table": "STOCKS"})
        for l in load:
            if (l[1] == name): return l[0]
        return -1
    #
    def lambda_handler(self, event, context):
        i = 0
        with self.conn.cursor() as cur:
            self.conn.commit()
            statement = f'INSERT INTO {event["table"]} VALUES '
            for el in event["data"]:
                for l in el:
                    temp = statement + str(l)
                    i += 1
                    cur.execute(temp)
                    if i % 1000 == 0:
                        self.conn.commit()
                        print(f"{i} amount has been pushed.")
        self.conn.commit()
        #self.conn.close()

        return {
            'statusCode': 200,
            "header": {},
            "body": json.dumps({"message": f"Successfully pushed {len(event['data'])} lines of data into {event['table']}."})
        }

if __name__ == '__main__':
    event = {
        "rds_host" : "market.cucrygetviqs.us-east-1.rds.amazonaws.com",
        "name": rds_config.db_username,
        "password": rds_config.db_password,
        "db_name": rds_config.db_name,
        "table": "MINUTE",
        "data": []
    }
    AWS = AwsResource(event, None)