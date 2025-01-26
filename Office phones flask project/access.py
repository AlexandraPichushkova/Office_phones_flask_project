
from flask import session, redirect, url_for, request, current_app, render_template
from functools import wraps

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main_menu'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:                                                                           ###как берется это значение . что за тип данных
            user_role = session.get('user_group')
            user_request = request.endpoint #название блюпринта + название обработчика
            print('request_endpoint=', user_request)
        #  user_bp = user_request.split('.')[0]                                                               ###зачем, где-то исп-ся?
            access = current_app.config['db_access']                                                           ###?
            if user_role in access and user_request in access[user_role]:                                           ###почему наз-ся accesss, откуда?
                return func(*args, **kwargs)
            else:
                return render_template('main_menu_error.html', message="У вас нет доступа на эту функциональность")
        else:
            return redirect(url_for('main_menu'))
    return wrapper
