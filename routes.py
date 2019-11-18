from app import app, db

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
            if user is None or not user.check_password(login_form.password.data):
                flash('Invalid username or password')
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
