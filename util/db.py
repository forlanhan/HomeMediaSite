# coding:utf-8
import psycopg2

def genSQLConnection():
    return psycopg2.connect(
        database="pvideo",
        user="postgres",
        password="979323",
        host="localhost",
        port="5432")


def queryInfo(conn, querySQL):
    curs = conn.cursor()
    curs.execute(querySQL)
    return curs.fetchall()


def queryInfoNewConn(querySQL):
    conn = genSQLConnection()
    curs = conn.cursor()
    curs.execute(querySQL)
    queryResult = curs.fetchall()
    conn.close()
    return queryResult
