import json
import sys
import logging
import rds_config
import pymysql
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

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    resultSet = []
    with conn.cursor() as cur:
        conn.commit()
        statement = f'SELECT * FROM {event["table"]}'
        if "id" in event.keys():
            statement = statement + " WHERE Id="+str(event["id"])
        cur.execute(statement)
        for row in cur:
            logger.info(row)
            resultSet.append(row)
    conn.commit()

    return {
        'statusCode': 200,
        "header": {},
        "body": json.dumps({"message": "Successful", "data":resultSet})
    }

# event = {"table": "TWO_MINUTE", "etc": {}}
# s = lambda_handler(event, None)
# print(s)
