from flask import Flask, render_template, session, json, redirect, url_for
from auth.route import blueprint_auth
from query.route import blueprint_query
from report.route import blueprint_report
from business.route import blueprint_business

app = Flask(__name__)

with open('../data/db_config.json') as f:    # автоматическое удаление объектов
    app.config['db_config'] = json.load(f)    # добавили db_config в глобальный словарь - можно обратиться ото всюду из проетка
with open('../data/db_access.json') as f:
    app.config['db_access'] = json.load(f)

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/sql')
app.register_blueprint(blueprint_report, url_prefix='/rep')
app.register_blueprint(blueprint_business, url_prefix='/bus')

app.secret_key = 'you will never guess' # параметр клавной апликации, который будет добавляться ко всем кукам

@app.route('/')
def main_menu():
    if 'user_group' in session:
        user_role = session.get('user_group')
        message = f'вы авторизованы как {user_role}'
    else:
        message = 'вам необходимо авторизоваться'
        return redirect(url_for('auth_bp.auth_index'))
    return render_template('main_menu.html', message=message)

@app.route('/exit')
def exit_func():
    session.clear()
    message = 'вам необходимо авторизоваться'   #До свидания, заходите к нам ещё
    return redirect(url_for('auth_bp.auth_index'))

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5001)