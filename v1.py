import os
from flask import Flask, request, render_template, redirect, url_for, abort, make_response, session, flash
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)

# rutiranje

@app.route('/')
def hello_world(): return 'Hello World!'

@app.route('/ford')
def ford():
    return '<h1> FORD </h1>'

@app.route('/profilee/<username>')
def profile(username):
    return '<h1> Hi '+username+'<h1>'

@app.route('/post/<int:post_id>')
def show_id(post_id):
    return '<h1> ID: {}</h1>'.format(post_id)


# metode slanja

@app.route('/what',methods=['GET','POST'])
def what():
    if request.method == 'GET':
        return 'GET'
    else:
        return 'POST'


# template

@app.route('/hello/<int:score>')
def hello_name(score):
    return render_template('hello.html', marks = score)

@app.route('/profile/<name>')
def index(name):
    return render_template("profile.html", parametar_ime=name)

@app.route('/result')
def result():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template('result.html', result = dict)



# redirekcija

@app.route('/admin')
def hello_admin(): return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest): return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
    if name =='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest = name))



# uzimanje podataka forme

# @app.route('/success/<name>')
# def success(name): return 'welcome %s' % name
@app.route('/success')
def success(): return 'logged in successfully'

@app.route('/formaLog')
def formaLog():
    return render_template('FormaLog.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    # if request.method == 'POST':
    #     user = request.form['nm']
    # return redirect(url_for('success', name=user))
    # else:
    # user = request.args.get('nm')
    # return redirect(url_for('success', name=user))
    if request.method == 'POST':
        if request.form['nm'] == 'admin':
           return redirect(url_for('success'))   # redirekcija
        else:
            abort(401)                           # abort
    else:
        return redirect(url_for('formaLog'))


# cookie

@app.route('/entercookie')
def entercookie():
    return render_template('enter_cookie.html')

@app.route('/error/<mess>')
def error(mess):
    return '<h1> GRESKA: '+mess+ '</h1>'

@app.route('/setcookie', methods=['POST','GET'])
def setcookie():
    if request.method=='POST':
        user = request.form['nm']
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie('userID', user)
        return resp
    else:
        return redirect(url_for('error', mess='SAMO POST')) # mala igra

@app.route('/getcookie')
def getcokie():
    uid = request.cookies.get('userID')
    return '<h1> Hi '+uid+ '</h1>'


# session

lstr=list('interesantno')
random.shuffle(lstr)
app.secret_key = str(lstr)

@app.route('/sessionn')
def sessionn():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
            "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/loginSess'></b>" + \
        "click here to log in</b></a>"

@app.route('/loginSess',methods = ['POST', 'GET'])
def loginSess():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('sessionn'))
    return '''
    <form action = "" method = "post">
    <p><input type = text name = username></p>
    <p><input type = submit value = Login></p>
    </form>
    '''

@app.route('/logout')
def logout():
    # uklanja ulaz username
    # iz session recnika
    session.pop('username', None)
    return redirect(url_for('sessionn'))


# message flashing

app.secret_key = 'random string'

@app.route('/indexx')
def indexx():
    return render_template('index.html')

@app.route('/loginn', methods=['GET', 'POST'])
def loginn():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
            request.form['password'] != 'pass':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('indexx'))
    return render_template('login.html', error=error)


# file uploading

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
lstr=list('interesantno')
random.shuffle(lstr)
app.secret_key = str(lstr)
app.config['UPLOAD_FOLDER']= './uploadfiles/'
app.config['MAX_CONTENT_LENGTH']= 10*1024*1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
    return render_template('uploadfile.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        # postoji li deo file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(redirect(url_for('upload_file')))
        f = request.files['file']
        # korisnik nije odabrao fajl,
        # browser salje prazan deo bez naziva fajla
        if f.filename == '':
            flash('No selected file')
            return redirect(url_for('upload_file'))
        if allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                secure_filename(f.filename)))
            return 'file uploaded successfully'
        else:
            flash('File extension not allowed.')
            return redirect(url_for('upload_file'))




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port= 5004)