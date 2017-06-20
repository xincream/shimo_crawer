# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import pymysql
from DBUtils.PooledDB import PooledDB

config = {
    'db': 's3c',
    'table': 'docs',
    'col': ['id', 'title', 'url', 'content', 'type', 'tags'],
    'ip': '10.8.2.84',
    'name': 'root',
    'passwd': 'sorry'
}

pool = PooledDB(pymysql, 5, host=config['ip'], user=config['name'],
                passwd=config['passwd'], db=config['db'], port=3306, charset='utf8')


def insert_data(data):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        key = '(' + ','.join(config['col'][1:5]) + ')'
        sql = 'insert into ' + config['table'] + key + 'values(%s, %s, %s, "sync")'
        cursor.executemany(sql, data)
        cursor.close()
        conn.commit()
    except Exception as e:
        print('mysql error : %d %s' % (e.args[0], e.args[1]))


def update_data(data):
    try:
        # 重新构造一下数据
        data_update = []
        for item in data:
            item = list(item)
            item[1], item[2] = item[2], item[1]
            data_update.append(item)
        conn = pool.connection()
        cursor = conn.cursor()
        sql = 'update ' + config['table'] + ' set ' + config['col'][1] + \
              ' = %s, ' + config['col'][3] + ' = %s, ' \
              + config['col'][4] + ' = "sync"'\
              + ' where ' + config['col'][2] + ' = %s'
        cursor.executemany(sql, data_update)
        cursor.close()
        conn.commit()
    except Exception as e:
        print('mysql error : %d %s' % (e.args[0], e.args[1]))


def get_now_sync():
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        sql = 'SELECT DISTINCT ' + config['col'][2] + ' FROM ' + config['table'] + \
              ' WHERE ' + config['col'][4] + r' = "sync"'
        result = query(cursor, sql)
        return result
    except Exception as e:
        print('mysql error : %d %s' % (e.args[0], e.args[1]))


def query(cursor, sql):
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        desc = cursor.description
        rows = []
        for cloumn in result:
            row = {}
            for i in range(0, len(cloumn)):
                row[desc[i][0]] = cloumn[i]
            rows.append(row)
        return rows
    except pymysql.Error as e:
        print('mysql error: %s SQL: %s' % (e, sql))


def insert(conn, cursor, data, table=config['table']):
    try:
        key = '(' + ','.join(config['col'][1:5]) + ')'
        print(key)
        part = []
        for item in data:
            temp = list(item)
            temp.append('sync')
            part.append("values('" + "','".join(temp) + "')")
        values = ', '.join(part)
        # print(values)
        sql = 'insert into ' + table + ' ' + key + ' ' + values
        print(sql)
        cursor.execute("set names 'utf8'")
        cursor.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        conn.rollback()
        print('mysql error: %s %s' % (e.args[0], e.args[1]))


if __name__ == '__main__':
    print(get_now_sync())






