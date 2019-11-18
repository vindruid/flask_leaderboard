import numpy as np 
import pandas as pd # be replaced soon
import os

from flask import Flask,render_template,url_for,request,g, flash, redirect
from werkzeug import check_password_hash, generate_password_hash, \
     secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, LoginManager, login_user, logout_user, UserMixin

from forms import LoginForm
from config import Config

# PARAMETER

## Upload parameter
UPLOAD_FOLDER = 'submissions'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'names'}

## FLASK configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 16 Megabytes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'my'
app.config.from_object(Config)

## Database configuration
db = SQLAlchemy(app)
db.app = app
migrate = Migrate(app, db)
login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128)) ## Too lazy to make it hash

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password): ## Too lazy to make it hash
        return self.password_hash == password

def allowed_file(filename):
    # checks if extension in filename is allowed
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    login_form = LoginForm()
    ### TODO handle registration
    if request.method == 'POST': 
        # load and insert user data
        print(123123)
    return render_template('register.html', login_form = login_form)

@app.route('/logout')
def logout():
    logout_user()
    print("log out success")
    return redirect(url_for('home_page'))

@app.route('/', methods=['GET', 'POST'])
def home_page():
    login_form = LoginForm()

    ## TODO: query leaderboard from database
    leaderboard = pd.read_csv('dummy_table.csv')
    leaderboard.sort_values('score', ascending = True, inplace = True) 
    leaderboard.reset_index(drop = True, inplace = True)

    if request.method == 'POST': # If upload file / Login
        ### LOGIN 
        if login_form.validate_on_submit():
            print(f'Login requested for user {login_form.username.data}, remember_me={login_form.remember_me.data}')
            user = User.query.filter_by(username=login_form.username.data).first()
            if user is None: # USER is not registered
                print("NO user name")
                return redirect(url_for('home_page'))
            elif user.check_password(login_form.password.data): # Password True
                print('True pass')
                login_user(user, remember=login_form.remember_me.data)
                return redirect(url_for('home_page'))
            else: #WRONG PASSWORD
                print('WRONG PASS')
                return redirect(url_for('home_page'))
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('home_page'))

        ### UPLOAD FILE
        if 'uploadfile' in request.files.keys(): 
            submission_file = request.files['uploadfile']
            #throw error if extension is not allowed
            if not allowed_file(submission_file.filename):
                raise Exception('Invalid file extension')

            if submission_file and allowed_file(submission_file.filename):
                filename = secure_filename(submission_file.filename)
                ## TODO: append userid and date to file to avoid duplicates
                # filename = str(session['user_id']) + '_' + \
                #             str(int(time.time())) + '_' + filename

                fullPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                submission_file.save(fullPath)
                print(f'SAVED SUBMISSION: {fullPath}')

                ## TODO: doing calculation on saved file
            
    return render_template('index.html', 
                        leaderboard = leaderboard,
                        login_form=login_form
    )

if __name__ == '__main__':
    app.run(debug=True)