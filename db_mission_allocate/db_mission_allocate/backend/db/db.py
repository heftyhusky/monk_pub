import mysql.connector
import sys
import json
from InputStrategy import InputStrategyFromLocal
import ast

from db_mission_allocate.config import (
    MYSQL_DATA_USER,
    MYSQL_DATA_PASSWORD,
    MYSQL_DATA_HOST,
    MYSQL_DATA_PORT,
    MYSQL_DATA_DATABASE,
)

def db_init(passwd:str):
    if passwd == "uuio":
        mydb = mysql.connector.connect(
            host = MYSQL_DATA_HOST,
            user = MYSQL_DATA_USER,
            password = MYSQL_DATA_PASSWORD
        )
        cursor = mydb.cursor()

        cursor.execute("DROP DATABASE IF EXISTS healthData")
        cursor.execute("CREATE DATABASE healthData")
        cursor.close()

        mydb = mysql.connector.connect(
            host = MYSQL_DATA_HOST,
            user = MYSQL_DATA_USER,
            password = MYSQL_DATA_PASSWORD,
            database="healthData"
        )
        cursor = mydb.cursor()



        cursor.execute("DROP TABLE IF EXISTS `index`")
        cursor.execute("""CREATE TABLE `index` (
            userId VARCHAR(25) PRIMARY KEY, 
            Vo2 VARCHAR(10),
            fitnessAge VARCHAR(10),
            FTP VARCHAR(10),
            gTrimp VARCHAR(10),
            heartRateDataCount INT
        )""")

        cursor.execute("DROP TABLE IF EXISTS heartRate")
        cursor.execute("""CREATE TABLE heartRate (
            heartRateDataCount INT PRIMARY KEY AUTO_INCREMENT,
    		userId VARCHAR(25),
    		FOREIGN KEY (userId) REFERENCES `index`(userId),
            raw JSON 
        )""")

        cursor.execute("""ALTER TABLE `index` ADD FOREIGN KEY (`heartRateDataCount`) REFERENCES `heartRate`(`heartRateDataCount`)""")
        cursor.close()

        return 'init database'
    else:
        return 'permission denied'

def db_upload(user_id, data):
    mydb = mysql.connector.connect(
            host = MYSQL_DATA_HOST,
            user = MYSQL_DATA_USER,
            password = MYSQL_DATA_PASSWORD,
            database="healthData"
        )
    cursor = mydb.cursor()
    sql = "SELECT heartRateDataCount FROM `index` WHERE userId=%s LIMIT 1"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    if result == []:
        sql = "INSERT INTO `index` (userId) VALUES(%s)"
        cursor.execute(sql, (user_id,))

        sql = "INSERT INTO `heartRate` (userId, raw) VALUES(%s, %s)"
        cursor.execute(sql, (user_id,data))

        sql = """UPDATE `index` SET heartRateDataCount=
                (SELECT heartRateDataCount FROM heartRate WHERE userId=%s ORDER BY heartRateDataCount DESC LIMIT 1)
                WHERE userId=%s"""
        cursor.execute(sql, (user_id,user_id))
    else:
        sql = "INSERT INTO `heartRate` (userId, raw) VALUES(%s, %s)"
        cursor.execute(sql, (user_id,data))

        sql = """UPDATE `index` SET heartRateDataCount=
                (SELECT heartRateDataCount FROM heartRate WHERE userId=%s ORDER BY heartRateDataCount DESC LIMIT 1)
                WHERE userId=%s"""
        cursor.execute(sql, (user_id,user_id))


    # sql = """INSERT INTO healthData.heartRate (heartRateDataCount, userId, raw) VALUES (%s, %s, %s)
    # """
    # val = (str(user_id), data)
    # cursor.execute(sql, val)
    mydb.commit()
    return data

def get_widgets(user_id):
    mydb = mysql.connector.connect(
        host = MYSQL_DATA_HOST,
        user = MYSQL_DATA_USER,
        password = MYSQL_DATA_PASSWORD,
        database="healthData"
    )
    cursor = mydb.cursor()

    # sql = "SELECT * FROM heartrate WHERE user_id=%(user_id)s"
    # cursor.execute(sql, {'user_id':user_id})
    sql = "SELECT raw FROM heartRate WHERE heartRateDataCount=6"
    cursor.execute(sql)

    row_headers=[x[0] for x in cursor.description] #this will extract row headers

    results = cursor.fetchall()
    x = ast.literal_eval(results[0][0])
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()

    return json.dumps(json_data)

if __name__ == "__main__":
    if len(sys.argv[1:]) == 2:
        command, arg = sys.argv[1:]
        if command == 'db_upload':
            inputobj = InputStrategyFromLocal("data.pkl")
            data = inputobj.get()
            db_upload(arg, json.dumps(data.user))
        if command == 'get_widgets':
            print(get_widgets(arg))
        if command == 'db_init':
            db_init(arg)