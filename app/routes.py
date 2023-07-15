from flask import render_template, flash, redirect, url_for
import datetime
from app import app
from app.forms import PathForm, RegistrationForm, Addstudent
from app.models import User, Students, Attendance
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.algorithm import short_path

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PathForm()
    if request.method == 'POST':
        startpoint = request.values.get('startpoint')  # Your form's
        endpoint = request.values.get('endpoint')  # input names
        print(startpoint)
        print(endpoint)
        
        path = short_path(startpoint, endpoint)
    else:
        path=""
        

    return render_template('index.html', title='Home', form=form, path=path)


@app.route('/whosnothere')
def whosnothere():
    not_here = []
    date_object = datetime.date.today()
    presents = Attendance.query.filter_by(date=date_object)
    student = Students.query.all()
    for s in student:
        p = Attendance.query.filter_by(date=date_object, s_id=s.s_id).first()
        if p is None:
            not_h = [s.s_id, s.s_name, s.class_code]
            not_here.append(not_h)

    return render_template('not_here.html', not_here=not_here, today_date=date_object)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)


@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():

    form = Addstudent()

    if form.validate_on_submit():
        student = Students(
            s_id=form.s_id.data, class_code=form.class_code.data, s_name=form.s_name.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered student!')
        return redirect(url_for('classlist'))

    return render_template('addstudent.html', form=form)


@app.route("/studenthere/<s_id>")
def studenthere(s_id):
    date_object = datetime.date.today()
    student = Students.query.filter_by(s_id=s_id).first()
    here = Attendance.query.filter_by(s_id=s_id, date=date_object).first()

    if student is None:
        flash('Sir you are not a student')
        return redirect(url_for('index'))
    elif here:
        flash('Sir youve alr arrived at school')
        return redirect(url_for('index'))

    else:
        presentsir = Attendance(class_code=student.class_code,
                                s_name=student.s_name, s_id=student.s_id, date=date_object)
        db.session.add(presentsir)
        db.session.commit()
        flash('Congratulations, you are now at school!')
        return redirect(url_for('classlist'))

    return redirect(url_for('index'))


@app.route('/classlist', methods=['GET', 'POST'])
def classlist():
    student = Students.query.all()
    return render_template('classlist.html', students=student)


@app.route('/delstudent/<s_id>')
def delstudent(s_id):
    Students.query.filter_by(s_id=s_id).delete()

    db.session.commit()

    return redirect(url_for('classlist'))


@app.route('/delstudenta/<id>')
def delstudenta(id):
    Attendance.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
