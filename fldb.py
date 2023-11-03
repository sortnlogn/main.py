import os
import sqlite3
from flask import Flask
import csv

DATABASE = '/tmp/flsite.db'
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

#создаем базу данных
def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

    # Connecting to the geeks database


def add_load(family,name,otch, subj, lab,lect,  practice,group):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Персона_id FROM Персона WHERE Фамилия = ? and Имя = ?  and Отчество = ? ", (family, name, otch))
    id = cur.fetchone()[0]
    cur.execute("SELECT Группа_id FROM Группа WHERE Название_группы = ? ", (group,))
    group_id = cur.fetchone()[0]
    print(group_id)
    if (lab == 'да'):
        lab_tag = 1
    else:
        lab_tag = 0
    if (lect == 'да'):
        lect_tag = 1
    else:
        lect_tag = 0
    if (practice == 'да'):
        practice_tag = 1
    else:
        practice_tag = 0
    print(family, name, otch, subj, lab, lect, practice, group)
# надо сделать разделение по предметам и еще добавить 3 запросы в дашборде указаны - все строится на этом но в другой раз сделаю, например в сб вечером
    #if (lab_tag == 1 and practice_tag)
    #and  Лаб_часов>? and Лекц_часов>? and  Прак_часов>?
    #lab_tag, lect_tag, practice_tag
    lab_pract_tag = practice_tag + lab_tag
    load_id = 1
    # and  Лаб_часов>0 and Лекц_часов=0 and  Прак_часов>0
   # print(lab_tag,lect_tag,practice_tag)
    if (lab_pract_tag == 1 and lect_tag == 0):
        cur.execute(
            "SELECT Нагрузка_id FROM Нагрузка WHERE Состав_id = ? and Название_предмета = ? and  Лаб_часов>=0 and Лекц_часов=0 and  Прак_часов>=0",
            (group_id, subj))
        load_id = cur.fetchone()[0]
    if (lab_pract_tag == 1 and lect_tag == 1):
        cur.execute(
            "SELECT Нагрузка_id FROM Нагрузка WHERE Состав_id = ? and Название_предмета = ?  and  Лаб_часов>0 and Лекц_часов>0 and  Прак_часов>0",
            (group_id, subj))
        load_id = cur.fetchone()[0]
    if (lab_pract_tag == 0 and lect_tag == 1):
        cur.execute(
            "SELECT Нагрузка_id FROM Нагрузка WHERE Состав_id = ? and Название_предмета = ?  and  Лаб_часов=0 and Лекц_часов>0 and  Прак_часов=0",
            (group_id, subj))
        load_id = cur.fetchone()[0]
    print(id,load_id)





    cur.execute("UPDATE Нагрузка SET преподаватель_id = ? WHERE Нагрузка_id = ?", (id, load_id))
    conn.commit()
    conn.close()

#заполняем таблицу
def fill_db(file):
    db = connect_db()
    f = open(file, 'r', encoding='utf-8')
    if f:
        reader = csv.DictReader(f, delimiter=';')
        data = reader
        i=0
        for row in data:
            i = i + 1
            values = (row['Дисциплина'], row['ЗЕ'], row['Семестр'], row['лабораторные'], row['лекции без потока'],
                      row['Практические занятия'], row['итого'])
            query = "INSERT INTO Дисциплина (Название_предмета, Зачетные_еденицы, Семестр, Лаб_часов, Лекц_часов,  Прак_часов ,Итого_часов) VALUES (?, ?, ?, ?, ?, ? , ?)"
            cursor.execute(query, values)

            # if (id !=grou_id(where назавние группы = ?) else id =
            values = (i,row['Группа'])
            query = "INSERT INTO Группа (Группа_id, Название_группы) VALUES (?, ?)"
            cursor.execute(query, values)

            values = (row['Дисциплина'], row['Семестр'], 0, 0,
                      row['Практические занятия'], row['итого'], i,-1, i)
            query = "INSERT INTO Нагрузка (Название_предмета, Семестр, Лаб_часов, Лекц_часов,  Прак_часов ,Итого_часов, Дисциплина_id  , преподаватель_id ,  Состав_id ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, values)

            values = (row['Дисциплина'], row['Семестр'], row['лабораторные'], 0,
                      0, row['итого'], i, -1, i)
            query = "INSERT INTO Нагрузка (Название_предмета, Семестр, Лаб_часов, Лекц_часов,  Прак_часов ,Итого_часов, Дисциплина_id  ,преподаватель_id ,  Состав_id ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, values)

            values = (row['Дисциплина'], row['Семестр'], 0, row['лекции без потока'],
                     0, row['итого'], i, -1, i)
            query = "INSERT INTO Нагрузка (Название_предмета, Семестр, Лаб_часов, Лекц_часов,  Прак_часов ,Итого_часов, Дисциплина_id  ,преподаватель_id ,  Состав_id ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, values)

            values = (row['Дисциплина'], row['Семестр'], row['лабораторные'], row['лекции без потока'],
                      row['Практические занятия'], row['итого'], i,-1, i)
            query = "INSERT INTO Нагрузка (Название_предмета, Семестр, Лаб_часов, Лекц_часов,  Прак_часов ,Итого_часов, Дисциплина_id  ,преподаватель_id , Состав_id ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, values)
    connection.commit()
    db.commit()
    db.close()

#вставить новую функцию
def export_teacher_workload_to_csv(teacher_id):
    connection = connect_db()
    cursor = connection.cursor()
    query = "SELECT * FROM Нагрузка WHERE преподаватель_id = ?"
    cursor.execute(query, (teacher_id,))
    teacher_workload = cursor.fetchall()

    with open('teacher_workload.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Запись заголовков столбцов
        writer.writerows(teacher_workload)

    cursor.close()
    connection.close()
#данные по семестру
def get_semester_data(semester):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Нагрузка_id, Название_предмета, Семестр, Итого_часов FROM Нагрузка WHERE Семестр = ?", (semester,))
    data = cur.fetchall()
    conn.close()
    return data

#данные по курсу -здесь баг сместр это восьмой семестр а не 8
def get_course_data(course):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Нагрузка_id, Название_предмета, (Семестр + 1) / 2 AS Курс, Итого_часов FROM Нагрузка WHERE (Семестр + 1) / 2 = ?", (course,))
    data = cur.fetchall()
    conn.close()
    return data

def get_teacher_load(teacher_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Нагрузка_id, Название_предмета, Семестр, Итого_часов FROM Нагрузка WHERE преподаватель_id = ?", (teacher_id,))
    data = cur.fetchall()
    conn.close()
    return data

#данные по группе
def get_group_data(group):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Название_предмета, Название_группы FROM Нагрузка JOIN Группа ON Нагрузка.Состав_id = Группа.Группа_id WHERE Название_группы = ?", (group,))
    data = cur.fetchall()
    conn.close()
    return data

#список препдавателей - без нагрузки
def get_teachers():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Преподаватель_id, Персона.Фамилия, Персона.Имя, Персона.Отчество FROM Преподаватель JOIN Персона ON Персона.Персона_id = Преподаватель.Персона_id")
    data = cur.fetchall()
    conn.close()
    return data


def view_load():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Персона.Фамилия,Персона.Имя, Персона.Отчество, Нагрузка.Название_предмета  FROM Персона  JOIN Преподаватель ON Персона.Персона_id = Преподаватель.Персона_id  JOIN Нагрузка ON Преподаватель.Преподаватель_id = Нагрузка.преподаватель_id ;")
    data = cur.fetchall()
    conn.close()
    return data

def view_load_id(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Персона.Фамилия,Персона.Имя, Персона.Отчество, Нагрузка.Название_предмета, (Нагрузка.Лаб_часов+Нагрузка.Лекц_часов+Нагрузка.Прак_часов)  as 'Общее кол-во часов' FROM Персона  JOIN Преподаватель ON Персона.Персона_id = Преподаватель.Персона_id  JOIN Нагрузка ON Преподаватель.Преподаватель_id = Нагрузка.преподаватель_id  WHERE Персона.Персона_id = ?;", (id, ))
    data = cur.fetchall()
    conn.close()
    return data

def sal_load_id(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Персона.Фамилия,Персона.Имя, Персона.Отчество, Нагрузка.Название_предмета, round((Нагрузка.Лаб_часов+Нагрузка.Лекц_часов+Нагрузка.Прак_часов)/Нагрузка.Итого_часов ,2) as 'Ставка' FROM Персона  JOIN Преподаватель ON Персона.Персона_id = Преподаватель.Персона_id  JOIN Нагрузка ON Преподаватель.Преподаватель_id = Нагрузка.преподаватель_id  WHERE Персона.Персона_id = ?;", (id, ))
    data = cur.fetchall()
    conn.close()
    return data

#добавление преподавателя
#добавление персоны
def add_teacher(family_name, first_name, patronymic, workload_share, scientific_degree, scientific_title, position, recruitment_conditions):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Персона")
    count = cur.fetchone()[0]
    person_id = count + 1
    teacher_id = count + 1

    cur.execute("INSERT INTO Преподаватель (Преподаватель_id,Доля_ставки, Ученая_степень, Ученое_звание, Должность, Персона_id, Условия_привлечения) VALUES (?,?,?,?,?,?,?)",
                (teacher_id, workload_share, scientific_degree, scientific_title, position, person_id, recruitment_conditions))
    cur.execute(
        "INSERT INTO Персона ( Персона_id ,Фамилия, Имя ,  Отчество) VALUES (?,?,?,?)",
        (person_id ,family_name, first_name, patronymic))
    conn.commit()
    #family_name, first_name, patronymic
    conn.close()
#меняем нагрузку
def assign_teacher_to_load(teacher_id, load_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE Нагрузка SET преподаватель_id = ? WHERE Нагрузка_id = ?", (teacher_id, load_id))
    conn.commit()
    conn.close()

#считаем нагрузку у преподавателя
def calculate_workload_share(teacher_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT Должность, Итого_часов FROM Преподаватель JOIN Нагрузка ON Преподаватель.Преподаватель_id = Нагрузка.преподаватель_id WHERE Преподаватель.Преподаватель_id = ?", (teacher_id,))
    data = cur.fetchall()
    conn.close()

    position = data[0][0]
    total_hours = data[0][1]

    if position == 'Профессор':
        rate = 1.0
    elif position == 'Доцент':
        rate = 0.75
    elif position == 'Старший преподаватель':
        rate = 0.5
    else:
        rate = 0.25

    workload_share = rate * total_hours
    return workload_share


#create_db()
connection = sqlite3.connect('flsite.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()
#file = 'Primer_nagruzki.csv'
#create_db()
#fill_db(file)