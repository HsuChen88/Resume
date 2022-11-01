from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index(title='About HsuChen'):
    return render_template('about.html', title=title)

@app.route('user/<usernname>')
def show_user(username):
    return render_template('user.html', username=username)

@app.route('/resume')
def show_resume(title='Resume'):
    return render_template('resume.html', title=title)

def register_action():
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    password1 = request.form.get('password1', '')
    password2 = request.form.get('password2', '')

    if not username:
        return '請輸入username<br><a href="/register">返回註冊畫面</a>'
    elif not email:
        return '請輸入email<br><a href="/register">返回註冊畫面</a>'
    elif not password1:
        return '請輸入password<br><a href="/register">返回註冊畫面</a>'
    elif not password2:
        return '請輸入password<br><a href="/register">返回註冊畫面</a>'
    elif len(password1)<4:
        return '密碼必須大於4碼<br><a href="/register">返回註冊畫面</a>'
    elif not password1==password2:
        return '兩次密碼必須相符<br><a href="/register">返回註冊畫面</a>'

    db = sqlite3.connect('mywebsite.db')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM user WHERE `email`="{email}"')
    queryresult = cur.fetchall()
    if queryresult:
        return 'email重複，請使用另一個email<br><a href="/register">返回註冊畫面</a>'
    cur.execute(f'SELECT * FROM user WHERE `username`="{username}"')
    queryresult = cur.fetchall()
    if queryresult:
        return 'username重複，請使用另一個username<br><a href="/register">返回註冊畫面</a>'

    cur.execute(f"INSERT INTO user (`username`, `email`, `password`) VALUES ('{username}','{email}','{password1}')")
    db.commit()
    db.close()
    return '註冊成功<br><a href="/login">前往登入畫面</a>'

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        return register_action()
    else:
        username = request.args.get('username', '')
        email = request.args.get('email', '')
        return render_template('register.html', username=username, email=email)


def login_process():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    db = sqlite3.connect('mywebsite.db')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM user WHERE `email`="{email}"')
    queryresult = cur.fetchall()
    if str(queryresult[0][3]) == password:
        return redirect(url_for('show_user_profile', username=queryresult[0][1]))
    return '密碼錯誤<br><a href="/login">返回登入畫面</a>'
    
@app.route('/login', methods=['GET', 'POST'])
def login(title='Login'):
    if request.method == 'POST':
        return login_process()
    return render_template('login.html', title=title)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
