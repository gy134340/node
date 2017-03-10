import pymysql

# mysql connect
global conn
def connect():
    global conn
    conn = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='123456789', db='ibook')

# mysql close
def close():
    global conn
    conn.close()


def insert():
    global cursor
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bean')
    for r in cursor.fetchall():
        print(r)


def delete():
    print()

def select():
    print()

def update():
    print()