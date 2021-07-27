from task import app
from flask import render_template,redirect,  url_for,flash,request
from task.models import User,Tasks
from task.forms import RegisterForm, LoginForm
from task import db
from flask_login import login_user,logout_user, login_required
from datetime import date
import datetime


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# --------------------------------------------------------------------------------------------------------------    

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user=User(
            username= form.username.data,
            email=form.email.data,
            password=form.password1.data
        )
        db.session.add(user)
        db.session.commit()
        flash("successfully registered",category='success')
        return redirect(url_for('home'))
    else:
        print("ERROR")
        
    if form.errors!={}:
        for err in form.errors.values():
            flash(f"{err}",category='danger')

    return render_template('register.html',form = form)


# -----------------------------------------------------------------------------------------------------

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user  and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            print("SUCCESS")
            flash("successfully logged in",category='success')
            return redirect(url_for('home'))
        else:
            flash("username and password not matching",category='danger')
            
    return render_template('login.html', form=form)

# ---------------------------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    flash("successfully logged out",category='info')
    return redirect(url_for('home'))


# --------------------------------------------------------------------------------------------

def valid_date(to_be_completed_date):
    current_date = str(date.today())
    current_date = current_date.split('-')
    to_be_completed_date = to_be_completed_date.split('-')
    
    # flash(f"{str(datetime.date(int(to_be_completed_date[0]),int(to_be_completed_date[1]),int(to_be_completed_date[2])).isocalendar()[1])}")

    # flash(f"{str(date.today())}")

    if current_date[1] > to_be_completed_date[1]:
        return False
    elif current_date[1] == to_be_completed_date[1]:
        if current_date[2] > to_be_completed_date[2]:
            return False
    return True



# -----------------------------------------------------------------------------------------

def check_if_overdue(completion_date):
    current_date = str(date.today())
    current_date = current_date.split('-')
    completion_date = completion_date.split('-')


    if current_date[1] > completion_date[1]:
        return True
    elif current_date[1] == completion_date[1]:
        if current_date[2] > completion_date[2]:
            return True
        else:
            return False
    else:
        return False
    
# ------------------------------------------------------------------------------------------------

@app.route("/task/<name>",methods=['GET','POST'])
@login_required
def tasks(name):
    id=User.query.filter_by(username=name).first()
    if request.method =='POST':
        if request.form['submit']=="Add":
            new_task=request.form['task']
            date_=str(request.form['date'])
            # date_to_be_completed=datetime.datetime.strptime(date_to_be_completed, '%Y-%m-%d')
            if valid_date(date_):
                date_task=date_
                date_=date_.split('-')
                week_no=str(datetime.date(int(date_[0]),int(date_[1]),int(date_[2])).isocalendar()[1])
                task=Tasks(task_name=new_task,date_to_be_completed=date_task,
                user_id=id.id,week_no=week_no)

                db.session.add(task)
                db.session.commit()
            else:
                flash("Invalid Date", category="danger")
        elif request.form['submit']=="Delete":
            Tasks.query.filter_by(id=int(request.form['task_delete'])).delete()
            db.session.commit()
        
        return redirect(url_for('tasks',name=name))
    else:
        tasks=id.tasks.order_by(Tasks.date_to_be_completed).all()
        date_today=str(date.today())
        date_today=date_today.split('-')
        this_week=str(datetime.date(int(date_today[0]),int(date_today[1]),int(date_today[2])).isocalendar()[1])
        for task in tasks:
            if check_if_overdue(task.date_to_be_completed):
                flash(f"{task.task_name} is overdue", category = 'warning')
        return render_template('task.html',name=name,tasks=tasks,this_week = this_week)