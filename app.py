from flask import Flask, render_template, redirect, request, url_for
from flask_login import (LoginManager, UserMixin, login_user, logout_user, login_required, current_user)
import json, os

app = Flask(__name__)

app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id):
        folder_path = "sources/users"
        users = os.listdir(folder_path)
        for user in users:
            userId = user.replace("user_", "")
            userId = userId.replace(".json", "")
            if userId == user_id:
                self.id = user_id
                user_path = folder_path + "/" + user
                with open(user_path, 'r') as json_file:
                    user_data = json.load(json_file)
                self.username = user_data["username"]
                if user_data["username"] == "KEFedorov":
                    self.is_admin = True
                else:
                    self.is_admin = False

@login_manager.user_loader
def load_user(user_id):
    folder_path = "sources/users"
    users = os.listdir(folder_path)
    for user in users:
        userId = user.replace("user_", "")
        userId = userId.replace(".json", "")
        if userId == user_id:
            return User(user_id)
    # Если user_id некорректный, то нужно вернуть None
    return None


@app.route('/')
@app.route('/home')
def home():
    logged_in = current_user.is_authenticated  # Автоматическая проверка статуса
    return render_template('home.html', loggedIn=logged_in)



# @app.route('/profile')
# @login_required
# def profile():
#     return f'''
#     <b>Личный кабинет пользователя (защищенная страница)</b><br>
#     Ваш логин: { current_user.username }<br>
#     <a href="/logout">Выйти</a>'''


@app.route('/account')
def account():
    logged_in = current_user.is_authenticated
    if not logged_in:
        return render_template('not_logged.html')
    folder_path = "sources/users/user_%s" % current_user.id + ".json"
    
    
    return render_template('account.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/courses')
def courses():
    return render_template('courses.html')

# @app.route('/admin')
# @login_required
# def admin_panel():
#     if current_user.is_admin:
#         return '''
#         <b>Панель администратора</b><br>
#         Защищенная страница, доступная только администратору
#         '''
#     else:
#         # Ошибка доступа
#         abort(403)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        data = dict(request.form)
        data['id'] = str(len(os.listdir('sources/users')))
        data.pop('confirmPassword', None)
        folder_path = "sources/users/" + 'user_' + data['id'] + '.json'
        with open(folder_path, 'w') as json_file:
            json.dump(data, json_file)
        return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        #data = dict(request.form)
        username = request.form.get("username")
        password = request.form.get("password")
        folder_path = "sources/users"
        users = os.listdir(folder_path)
        for user in users:
            user_path = folder_path + "/" + user
            with open(user_path, 'r') as json_file:
                    user_data = json.load(json_file)
                    print(user_data)
            if user_data["username"] == username and user_data["password"] == password:
                print(user_data["id"])
                cur_user = User(user_data["id"])
                print(cur_user)
                login_user(cur_user)
                return redirect(url_for('home'))

        return 'Неверные данные! <a href="/login">Попробовать снова</a>'

#=================================================================================================

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")