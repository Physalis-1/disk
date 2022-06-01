import copy
import sqlite3
import threading
import socket
from hashlib import sha256

from win32api import GetSystemMetrics
# логин пароль админа
# таблица виды работ (работа-время-стоимость)
# таблица цены за диаметр (диаметр-стоимость)
# таблица запись (дата-время-ФИО-телефон-стоимость)

soc = socket.socket()
soc.bind (('localhost',2004))
lock = threading.RLock()

def create_table_login():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login(log TEXT PRIMARY KEY, pas TEXT NULL)""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS work(job TEXT PRIMARY KEY,time TEXT, price INTEGER NULL)""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS diametr(razmer TEXT PRIMARY KEY,price INTEGER)""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS zapis(date TEXT,fio TEXT, phone TEXT, time TEXT, price TEXT, diam TEXT, serv TEXT)""")
    conn.commit()
    code = sha256('ADMIN'.encode('utf-8')).hexdigest()
    pwd = [('ADMIN', str(code))]
    cursor.executemany("INSERT INTO login VALUES (?,?)", pwd)
    pwd = [('D10-13', 1000)]
    cursor.executemany("INSERT INTO diametr VALUES (?,?)", pwd)
    conn.commit()
    pwd = [('D14-16', 1400)]
    cursor.executemany("INSERT INTO diametr VALUES (?,?)", pwd)
    conn.commit()
    pwd = [('D17-21', 1600)]
    cursor.executemany("INSERT INTO diametr VALUES (?,?)", pwd)
    conn.commit()
    pwd = [('D22-26', 1800)]
    cursor.executemany("INSERT INTO diametr VALUES (?,?)", pwd)
    conn.commit()

    pwd = [('Балансировка со снятием и чисткой', '20',1000)]
    cursor.executemany("INSERT INTO work VALUES (?,?,?)", pwd)
    conn.commit()
    pwd = [('Замена шин со сбором колес', '20',1500)]
    cursor.executemany("INSERT INTO work VALUES (?,?,?)", pwd)
    conn.commit()
    pwd = [('Сбор с балансировкой', '20',1700)]
    cursor.executemany("INSERT INTO work VALUES (?,?,?)", pwd)
    conn.commit()
    cursor.close()

def select_login(login,pc):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login WHERE log='" + login + "' AND pas='" + pc + "'")
    records = cursor.fetchall()
    cursor.close()
    return records

def check_login():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT count(name)  FROM sqlite_master WHERE type = 'table'  AND name = 'login'""")
    if cursor.fetchone()[0] == 1:
        conn.commit()
        cursor.close()
        return 0
    else:
        conn.commit()
        cursor.close()
        return 1

def insert_diam(a1,a2):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    pwd = [(a1,int(a2))]
    cursor.executemany("INSERT INTO diametr VALUES (?,?)", pwd)
    conn.commit()
    cursor.close()


def delet_diam(a1,a2):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM diametr WHERE razmer='"+a1+"' AND price="+a2)
    conn.commit()
    cursor.close()

def insert_serv(m0,m1,m2,m3,m4,m5,m6):
    print(m0,m1,m2,m3,m4,m5,m6)
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    pwd = [(m0,m1,m2,m3,m4,m5,m6)]
    cursor.executemany("INSERT INTO zapis VALUES (?,?,?,?,?,?,?)", pwd)
    conn.commit()
    cursor.close()

def delet_serv(a1,a2):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM zapis WHERE time='"+a1+"' AND date='"+a2+"'")
    conn.commit()
    cursor.close()


def insert_work(a1,a2,a3):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    pwd = [(a1,a2,int(a3))]
    cursor.executemany("INSERT INTO work VALUES (?,?,?)", pwd)
    conn.commit()
    cursor.close()

def delet_work(a1,a2,a3):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM work WHERE job='"+a1+"'")
    conn.commit()
    cursor.close()




def select_price():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diametr")
    records = cursor.fetchall()
    print(records)
    cursor.close()
    return records

def select_serv():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zapis")
    records = cursor.fetchall()
    print(records)
    cursor.close()
    return records

def select_work():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work")
    records = cursor.fetchall()
    cursor.close()
    return records

from datetime import timedelta, datetime
def select_date():
    date = []
    now = datetime.now()
    time = []
    time_date = []
    for k in range(1, 5):
        day = timedelta(k)
        in_two_days = now + day
        d=str(in_two_days.day) + ":" + str(in_two_days.month) + ":" + str(in_two_days.year)
        range_ = (timedelta(hours=19) - timedelta(hours=8)) / timedelta(minutes=20)
        tim = []
        for i in range(0, int(range_)):
            conn = sqlite3.connect("base.db")
            cursor = conn.cursor()
            str_t=str(timedelta(hours=8)+timedelta(minutes=20)*i)
            cursor.execute("SELECT * FROM zapis WHERE date='"+d+"' AND time='"+str_t+"'")
            records = cursor.fetchall()
            cursor.close()
            if len(records)==0:
                tim.append(copy.deepcopy(str_t))
        if len(tim)>0:
            date.append(copy.deepcopy(d))
            time_date.append(copy.deepcopy(tim))
    return date,time_date


#     cursor.execute("""CREATE TABLE IF NOT EXISTS zapis(day TEXT, month TEXT, year TEXT, phone TEXT, time TEXT)""")
def func(conn,addres):
    global soc
    lock.acquire()
    if check_login() == 1:
        create_table_login()
    lock.release()
    datchik = 0
    datch = 0
    mass = []
    strs=""
    while True:
        msg = conn.recv(1024).decode("UTF-8")
        print(msg)
        for i in range (0, len(msg)):
            if msg[i]!="|":
                strs=strs+msg[i]
            elif (datchik==0 and (i==len(msg)-1 and ("flag" in strs)) or ("flag" in strs)):
                if ("flag11" in strs):
                    #
                    datchik = 11
                elif ("flag10" in strs):
                    # добавить запись на сервис
                    datchik = 10
                    strs = ""
                elif ("flag3" in strs):
                    # добавить запись об услуге
                    datchik = 3
                    strs = ""
                elif ("flag4" in strs):
                    # посмотреть запись на сервис
                    datchik = 4
                elif ("flag5" in strs):
                    # удалить запись на сервис
                    datchik = 5
                elif ("flag6" in strs):
                    # посмотреть услуги работы
                    datchik = 6
                elif ("flag7" in strs):
                    # посмотреть диаметры
                    datchik = 7
                elif ("flag8" in strs):
                    # удалить диаметры
                    datchik = 8
                    strs = ""
                elif ("flag9" in strs):
                    # добавить диаметры
                    datchik = 9
                    strs = ""
                elif ("flag2" in strs):
                    # удалить запись об услуге
                    datchik = 2
                    strs = ""
                elif ("flag1" in strs):
                    # вход
                    datchik = 1
                    strs = ""
            else:
                # strs = strs + msg[i]
                mass.append(copy.deepcopy(strs))
                print(mass)
                print(datchik)
                strs = ""
            print(strs)
        if (datchik==8 or datchik==9 or datchik==5) and len(mass)==2:
            break
        if datchik==10 and len(mass)==7:
            break
        if (datchik==2 or datchik==3) and len(mass)==3:
            break
        if (datchik==1 or datchik==4 or datchik==6 or datchik==7 or datchik==11 ):
            break

    lock.acquire()
    exit_mass = []
    if datchik == 1:
        rec = select_login(mass[0], mass[1])
        print(rec)
        if len(rec) == 0:
            exit_mass.append("error")
        else:
            exit_mass.append("ok")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    if datchik == 6 or datchik ==7 or datchik==4:
        rec=3
        if datchik==6:
            rec = select_work()
        elif datchik==7:
            rec = select_price()
        elif datchik==4:
            rec = select_serv()
        if len(rec) == 0:
            exit_mass.append("error")
        else:
            print(rec)
            exit_mass=rec
        for i in range(0, len(exit_mass)):
            for j in range(0, len(exit_mass[i])):
                conn.send(str(exit_mass[i][j]).encode("UTF-8"))
                conn.send(str("|").encode("UTF-8"))
        conn.send(str("finish").encode("UTF-8"))
    if datchik == 8:
        try:
            delet_diam(mass[0],mass[1])
            exit_mass.append("ok")
        except sqlite3.Error:
            exit_mass.append("error")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    if datchik == 9:
        try:
            insert_diam(mass[0],mass[1])
            exit_mass.append("ok")
        except sqlite3.Error:
            exit_mass.append("error")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    if datchik == 10:
        try:
            insert_serv(mass[0],mass[1],mass[2],mass[3],mass[4],mass[5],mass[6])
            exit_mass.append("ok")
        except sqlite3.Error:
            exit_mass.append("error")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    if datchik == 5:
        try:
            print(mass)
            delet_serv(mass[0],mass[1])
            exit_mass.append("ok")
        except sqlite3.Error:
            exit_mass.append("error")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    if datchik == 3:
        try:
            insert_work(mass[0],mass[1],mass[2])
            exit_mass.append("ok")
        except sqlite3.Error:
            exit_mass.append("error")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    if datchik == 2:
        try:
            delet_work(mass[0],mass[1],mass[1])
            exit_mass.append("ok")
        except sqlite3.Error:
            exit_mass.append("error")
        for i in range(0, len(exit_mass)):
            message_to_send = exit_mass[i].encode("UTF-8")
            conn.send(message_to_send)
    # if datchik == 5 or datchik==10:
    if datchik == 11:
        a1,a2=select_date()
        if len(a1) == 0:
            exit_mass.append("error")
        else:
            exit_mass=a1
        # print('ee',a1)
        # print('uu',a2)
        print('ppp',len(a2[0]))
        for i in range(0, len(exit_mass)):
            for j in range(0, len(a2[i])):
                conn.send(str(exit_mass[i]).encode("UTF-8"))
                conn.send(str("|").encode("UTF-8"))
                conn.send(str(a2[i][j]).encode("UTF-8"))
                conn.send(str("|").encode("UTF-8"))
        conn.send(str(len(a2[0])).encode("UTF-8"))
        conn.send(str("|").encode("UTF-8"))
        conn.send(str(len(a2[1])).encode("UTF-8"))
        conn.send(str("|").encode("UTF-8"))
        conn.send(str(len(a2[2])).encode("UTF-8"))
        conn.send(str("|").encode("UTF-8"))
        conn.send(str(len(a2[3])).encode("UTF-8"))
        conn.send(str("|").encode("UTF-8"))
        conn.send(str("finish").encode("UTF-8"))
    lock.release()
    exit()


print('Start Server')
while True:
    soc.listen(1024)
    conn, addr = soc.accept()
    threading.Thread(target=func, args=(conn,addr)).start()