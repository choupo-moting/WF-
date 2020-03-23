import json
import redis
import pymysql


def main(redis_database, mysql_tables):
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='wanfangproject', port=3306,
                               charset='utf8')
    cur = mysqlcli.cursor()
    while True:
        print('==-=-=')
        source, data = rediscli.blpop("kanqi:items")
        item = json.loads(data.decode('utf-8'))
        try:
            sql=""" INSERT INTO kanqi({}) value ({})""" .format(','.join(item.keys()), ','.join(['%s'] * len(item)))
            cur.execute(sql,list(item.values()))
            mysqlcli.commit()
            print("inserted successed")
        except Exception as err:
            print("Mysql Error", err)
            mysqlcli.rollback()


if __name__ == '__main__':
    start_key = [
        {'degree:items': 'degree'},
        {'laws:items': 'laws'},
        {'scientific_report:items': 'scientificreport'},
        {'patent:items': 'zhuanli'},
        {'kanqi:items': 'kanqi'},
        {'meeting:items': 'meeting'}
    ]
    for key in start_key:
        for start in key.items():
            main(start[0], start[1])
