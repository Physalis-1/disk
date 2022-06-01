import copy
from datetime import time
import socket
from hashlib import sha256
# import streamlit_authenticator as at
import streamlit as st
import requests
import pandas as pd
import numpy as np
def app():
    def check_password():

        def password_entered():
            server = 'localhost', 2004
            sor = socket.socket()
            sor.connect(('localhost', 2004))
            code = sha256(ps.encode('utf-8')).hexdigest()
            sor.sendto((lg + '|').encode('utf-8'), server)
            sor.sendto((str(code) + '|').encode('utf-8'), server)
            sor.sendto(('flag1' + '|').encode('utf-8'), server)
            mass = []
            while True:
                data = sor.recv(1024).decode('utf-8')
                mass.append(data)
                if len(mass) == 1:
                    break
            sor.close()
            if mass[0] == 'error':
                st.session_state["password_correct"] = False
            elif mass[0] == 'ok':
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store username + password
                del st.session_state["username"]

        if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
            lg = st.text_input("Username", key="username")
            ps = st.text_input(
                "Password", type="password", key="password")
            if st.button("Старт!"):
                password_entered()
            return False
        else:
            return True

    def ins_del_diam(flag,data):
        server = 'localhost', 2004
        sor = socket.socket()
        sor.connect(('localhost', 2004))
        sor.sendto((flag + '|').encode('utf-8'), server)
        for i in range(0, len(data)):
            sor.sendto((data[i] + '|').encode('utf-8'), server)
        mass = []
        while True:
            data = sor.recv(1024).decode('utf-8')
            print(data)
            if data == 'ok' or data == 'error':
                break
            mass.append(data)
        sor.close()
        print('mass', mass)
        return mass

    def table1(flag, l):
        server = 'localhost', 2004
        sor = socket.socket()
        sor.connect(('localhost', 2004))
        sor.sendto((flag + '|').encode('utf-8'), server)
        mass = []
        vrem = []
        result = ''
        while True:
            result = ''
            data = sor.recv(1024).decode('utf-8')
            print('data', data)
            for i in range(0, len(data)):
                if data[i] != '|':
                    result = result + data[i]
                elif result != '':
                    if result == 'finish' or result == 'error':
                        break
                    else:
                        vrem.append(copy.deepcopy(result))
                        result = ''
                        if len(vrem) == l:
                            mass.append(copy.deepcopy(vrem))
                            vrem = []
            if len(result) > 0:
                if result == 'finish' or result == 'error':
                    break
                vrem.append(copy.deepcopy(result))
                if len(vrem) == l:
                    mass.append(copy.deepcopy(vrem))
                    vrem = []
        sor.close()
        print('mass', mass)
        return mass

    from datetime import timedelta, datetime
    if check_password():
        sum_count=0
        option = st.selectbox('Выбирите дейтвие',('Заказы', 'Услуга', 'Диаметр колес'))
        if option == 'Заказы':
            data = table1('flag4', 7)
            if len(data) == 0:
                st.write("Пусто")
            else:
                df = pd.DataFrame(data)
                df.columns = ['Дата', 'ФИО', 'Телефон','Время','Стоимость','диметр','работы']
                st.dataframe(df)
            data2 = table1('flag6', 3)
            data3 = table1('flag7', 2)
            work=[]
            work_price = []
            diamentr = []
            diametr_price = []
            for i in range (0,len(data2)):
                work.append(data2[i][0])
            for i in range (0,len(data2)):
                work_price.append(data2[i][2])
            for i in range (0,len(data3)):
                diamentr.append(data3[i][0])
            for i in range (0,len(data3)):
                diametr_price.append(data3[i][1])
            option_work = st.selectbox(
                'Выбирите дату',
                (work))
            option_diametr = st.selectbox(
                'Выбирите дату',
                (diamentr))
            sum_count = int(work_price[work.index(option_work)])+int(diametr_price[diamentr.index(option_diametr)])
            st.write('стоимость:', sum_count)
            data1 = table1('flag11', 2)
            d2=data1.pop()
            d1=data1.pop()
            date=[]
            time_1 = [[],[],[],[]]
            d1[0] = int(d1[0])
            d1[1] = int(d1[1])
            d2[0] = int(d2[0])
            d2[1] = int(d2[1])
            if d1[0] > 0:
                for i in range(0, d1[0]):
                    time_1[0].append(data1[i][1])
                date.append(data1[i][0])
            if d1[1] > 0:
                for i in range(d1[0], d1[1] + d1[0]):
                    time_1[1].append(data1[i][1])
                date.append(data1[i][0])
            if d2[0] > 0:
                for i in range(d1[1] + d1[0], d1[1] + d1[0] + d2[0]):
                    time_1[2].append(data1[i][1])
                date.append(data1[i][0])
            if d2[1] > 0:
                for i in range(d1[1] + d1[0] + d2[0], d1[1] + d1[0] + d2[0] + d2[1]):
                    time_1[3].append(data1[i][1])
                date.append(data1[i][0])
            option6 = st.selectbox(
                'Выбирите дату',
                (date))
            q=date.index(option6)
            option1=time_1[q][0]
            if q!=None:
                option1 = st.selectbox(
                    'Выбирите время',
                    (time_1[q]))

            title1 = st.text_input('ФИО')
            title2 = st.text_input('Телефон')
            st.write('для удаления заполните толкьо время и дату!')
            if st.button("Вставка!"):
                st.write('Вставака ожидайте')
                ins_del_diam('flag10', [option6, title1, str(title2),option1,str(sum_count), option_diametr,option_work ])
                st.write('Проверьте результут в таблице')
            if st.button("Удаление!"):
                st.write('Удаление ожидайте')
                ins_del_diam('flag5', [option1,option6])
                st.write('Проверьте результут в таблице')
        elif option == 'Услуга':
            data = table1('flag6',3)
            if len(data) == 0:
                st.write("Пусто")
            else:
                # 'Работа','Время','Цена'
                df = pd.DataFrame(data)
                df.columns = ['Работа', 'Время', 'Цена']
                st.dataframe(df)
                title1 = st.text_input('Работа')
                title2 = st.text_input('Время')
                title3 = st.text_input('Цена')
                if st.button("Вставка!"):
                    st.write('Вставака ожидайте')
                    ins_del_diam('flag3', [title1, title2,title3])
                    st.write('Проверьте результут в таблице')
                if st.button("Удаление!"):
                    st.write('Удаление ожидайте')
                    ins_del_diam('flag2', [title1, title2,title3])
                    st.write('Проверьте результут в таблице')
        elif option == 'Диаметр колес':
            data = table1('flag7',2)
            if len(data) == 0:
                st.write("Пусто")
            else:
                df = pd.DataFrame(data)
                df.columns = ['Диаметр', 'Цена']
                st.dataframe(df)
                st.write('вставка/удаление',data)
                title1 = st.text_input('Диаметр')
                title2 = st.text_input('Цена')
                if st.button("Вставка!"):
                    st.write('Вставака ожидайте')
                    ins_del_diam('flag9',[title1,title2])
                    st.write('Проверьте результут в таблице')
                if st.button("Удаление!"):
                    st.write('Удаление ожидайте')
                    ins_del_diam('flag8', [title1, title2])
                    st.write('Проверьте результут в таблице')

