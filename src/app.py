
__author__= 'nawaz'

import os
import datetime
from src.models.user import User
import src.models.errors as UserErrors
from src.models.process import Process
from src.models.automation import Automation
from src.common.database import Database
from flask import Flask, render_template, request, session, make_response, redirect, url_for


app = Flask(__name__)  # __main__
app.secret_key = os.urandom(64)



@app.route('/')  # www.mysite.com/
def home_template():
    return render_template('home.html')



@app.route('/login', methods=['POST'])  # www.mysite.com/api/login
def login_template():
    return render_template('login.html')



@app.route('/register', methods=['POST'])  # www.mysite.com/api/register
def register_template():
    return render_template('register.html')



@app.before_first_request
def initialize_database():
    Database.initialize()



@app.route('/auth/login', methods=['GET', 'POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    try:
        if User.login_valid(email, password):
            User.login(email)
        else:                           # these lines may never execute due to exceptions TODO
            User.logout()               # these lines may never execute due to exceptions TODO
    except UserErrors.UserError as e:
        return e.message

    return render_template("landing_page.html", email=session['email'])



@app.route('/auth/logout', methods=['GET', 'POST'])
def logout_user():
    User.logout()

    return render_template("login.html")



@app.route('/auth/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register(email, password)
            session['email'] = email
            #return email
            return render_template("landing_page.html", email=session['email'])
        except UserErrors.UserError as e:
            return e.message



@app.route('/processes/<string:user_id>')
@app.route('/processes', methods=['POST', 'GET'])
def process_listing(user_id=None):
    if user_id is not None:
        user =  User.get_by_user_id(user_id)
    else:
        user =  User.get_by_email(session['email'])

    processes = Process.get_all()

    return render_template("processes.html", processes=processes, email=user.email)



@app.route('/processes/new', methods=['POST', 'GET'])
def create_new_process():
    if request.method == 'GET':
        return render_template('new_process.html', email=session['email'])
    else:
        lob =  request.form['lob']
        group = request.form['group']
        process_name = request.form['process_name']
        process_desc = request.form['process_desc']
        created_by   = session['email']
        created_date = datetime.datetime.utcnow()
        updated_by   = None
        updated_date = None


        new_process = Process(lob, group, process_name, process_desc, )
        new_process.insert()
        return make_response(process_listing())



@app.route('/processes/edit/<string:process_id>', methods=['POST', 'GET'])
def edit_process(process_id):
    process = Process.get_by_id(process_id)

    if request.method == 'POST':
        process.process_desc = request.form['process_desc']
        print("request.form['process_desc']: "+request.form['process_desc'])
        print("process.process_desc: "+process.process_desc)
        process.update()
        return make_response(process_listing())

    return render_template('edit_process.html', process=process, email=session['email'])



@app.route('/processes/delete/<string:process_id>', methods=['POST', 'GET'])
def delete_process(process_id):
    process = Process.get_by_id(process_id)
    process.remove_from_db()
    return make_response(process_listing())



@app.route('/automations/<string:process_id>', methods=['GET'])
def process_automations(process_id):
    process = Process.get_by_id(process_id)
    automations = process.get_automations()
    return render_template('automations.html', email=session['email'], automations=automations, process_name=process.process_name, process_id=process._id)



@app.route('/automations/new/<string:process_id>', methods=['POST', 'GET'])
def create_new_automation(process_id):

    process = Process.get_by_id(process_id)

    if request.method == 'GET':
        return render_template('new_automation.html', process=process, email=session['email'])
    else:
        #automation_tag, automation_name, automation_desc, platform, golive_dt, status, retirement_dt, last_certified_dt
        automation_tag =  request.form['automation_tag']
        automation_name = request.form['automation_name']
        automation_desc = request.form['automation_desc']
        platform = request.form['platform']
        golive_dt = request.form['golive_dt']
        status = request.form['status']
        retirement_dt = request.form['retirement_dt']
        last_certified_dt = request.form['last_certified_dt']

        new_automation = Automation(process_id, automation_tag, automation_name, automation_desc, platform, golive_dt, status, retirement_dt, last_certified_dt)
        new_automation.insert()
        return make_response(process_automations(process_id))



@app.route('/automations/edit/<string:automation_id>', methods=['POST', 'GET'])
def edit_automation(automation_id):
    automation = Automation.get_by_id(automation_id)

    if request.method == 'POST':
        automation.automation_name = request.form['automation_name']
        automation.automation_desc = request.form['automation_desc']
        automation.platform = request.form['platform']
        automation.golive_dt = request.form['golive_dt']
        automation.status = request.form['status']
        automation.retirement_dt = request.form['retirement_dt']
        automation.update()
        #return redirect(url_for('process_automations()', process_id=automation.process_id))
        return make_response(process_automations(automation.process_id))

    return render_template('edit_automation.html', automation=automation, email=session['email'])



@app.route('/automations/delete/<string:automation_id>', methods=['POST', 'GET'])
def delete_automation(automation_id):
    automation = Automation.get_by_id(automation_id)
    automation.remove_from_db()
    return make_response(process_automations(automation.process_id))



if __name__ == '__main__' :
    app.run(port= 4995, debug=True)

