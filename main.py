import csv
import sqlite3
from flask import Flask, render_template, request, redirect, Response,g
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.loginForm import LoginForm
from data.registerForm import RegisterForm
from data.users import User
import os
import fldb
import io
db_session.global_init("db/blogs.sqlite")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Admin123'
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
login_manager = LoginManager()
login_manager.init_app(app)
cur_id = 0

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

# teacher load _____  calculate load
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/dashboard")
def dash():
    return render_template('dashboard.html')

@app.route("/dashboard_teacher")
def dashboard_teacher():
    return render_template('dashboard_teacher.html')

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # Получаем файл из запроса
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        f = open(file.filename, 'r', encoding='utf-8')
        if f:
            reader = csv.DictReader(f, delimiter=';')
            #fldb.fill_db(file.filename)
            return render_template('data.html', data=reader)
        else:
            return 'Invalid file format'
    return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    global cur_id
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.is_administrator() and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            print(user.is_administrator())
            return redirect("/dashboard")
        elif user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            cur_id = user.get_teacher_id()
            print(cur_id)
            print(user.is_administrator())
            return redirect("/dashboard_teacher")#
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        if request.form.get('query_type') in ['semester', 'course', 'group']:
            query_type = request.form.get('query_type')
            query_text = request.form.get('query_text')

            if query_type == 'semester':
                data = fldb.get_semester_data(query_text)
                names = ['Нагрузка_id', 'Название_предмета', 'Семестр', 'Итого_часов']
                return render_template('results.html', data=data, names = names, query_type='По семестрам')
            elif query_type == 'course':
                data = fldb.get_course_data(query_text)
                names = ['Название_предмета', 'Номер группы']
                return render_template('results.html', data=data, names = names, query_type='По курсам')
            elif query_type == 'group':
                data = fldb.get_group_data(query_text)
                names = ['Нагрузка_id', 'Название_предмета', 'Семестр', 'Итого_часов']
                return render_template('results.html', data=data, names = names, query_type='По группам')
        elif request.form.get('query_type') == 'teachers':
            data = fldb.get_teachers()
            return render_template('all_teachers.html', data=data, query_type='Список преподавателей')
    return render_template('query.html')


@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        if request.form.get('query_type') == 'add_teacher':

            family = request.form.get('family')
            name = request.form.get('name')
            otch = request.form.get('otch')
            workload_share = request.form.get('workload_share')
            scientific_degree = request.form.get('scientific_degree')
            scientific_title = request.form.get('scientific_title')
            position = request.form.get('position')
            recruitment_conditions = request.form.get('recruitment_conditions')

            fldb.add_teacher( family,name,otch, workload_share, scientific_degree, scientific_title, position, recruitment_conditions)

            return "Новый преподаватель успешно добавлен!"
    return render_template('add_teacher.html')



@app.route('/add_load', methods=['GET', 'POST'])
def add_load():
    if request.method == 'POST':
        if request.form.get('query_type') == 'add_load':

            family = request.form.get('family')
            name = request.form.get('name')
            otch = request.form.get('otch')
            subj = request.form.get('subj')
            group = request.form.get('group')
            lab = request.form.get('lab')
            lect = request.form.get('lection')
            practice = request.form.get('practice')
            #print(subj, group)
            fldb.add_load(family,name,otch, subj, lab,lect,  practice, group)
           # print(subj,group)
            return "Нагрузка преподвателя добавлена!"
    return render_template('add_load.html')

@app.route('/view_load', methods=['GET', 'POST'])
def view_load():
    data = fldb.view_load()
    names = ('Фамилия','Имя','Отчество','Название_предмета')
    return render_template('view_load.html', data=data,names = names)


@app.route('/view_load_id', methods=['GET', 'POST'])
def view_load_id():
    data = fldb.view_load_id(cur_id)
    for row in data:
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])
        print(row[4])
    names = ('Фамилия','Имя','Отчество','Название_предмета', 'Общее количество часов')
    return render_template('view_load.html', data=data,names = names)


@app.route('/my_sal', methods=['GET', 'POST'])
def my_load():
    data = fldb.sal_load_id(cur_id)
    names = ('Фамилия','Имя','Отчество','Название_предмета', 'Доля ставки')
    return render_template('my_sal.html', data=data,names = names)

@app.route('/export/<int:teacher_id>', methods=['GET'])
def export_teacher_load(teacher_id):
    data = fldb.get_teacher_load(teacher_id)

    # Создание CSV-файла
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',', quotechar='"')
    writer.writerow(['Нагрузка ID', 'Название предмета', 'Семестр', 'Итого часов'])
    for row in data:
        writer.writerow(row)
        print(row)

    # Создание HTTP-ответа с CSV-файлом
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=teacher_load.csv"
    return response

if __name__ == "__main__":
    isAdmin = False
    db_session.global_init("db/blogs.sqlite")
    app.run()
