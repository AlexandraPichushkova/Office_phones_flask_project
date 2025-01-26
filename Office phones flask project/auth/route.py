import os
from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from database.sql_provider import SQLProvider
from auth.model_route import model_route

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

provider = SQLProvider(
    os.path.join(os.path.dirname(__file__), 'sql'))  # соединяем путь к текущей дериктории и файлу с sql шаблоном



@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_index():
    if request.method == 'GET':
        return render_template('input_auth.html')
    user_input_data = request.form
    print(user_input_data)
    print(user_input_data['login'])
    print(user_input_data['password'])
    user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                   provider)
    print('user_info_result', user_info_result)
    if user_info_result.status:  # если статус True, т.е. все отработало корректно
        user_group = user_info_result.result[0][0]
        user_id = user_info_result.result[0][1]
        session['user_group'] = user_group
        session['user_id'] = user_id
        print("Выполнена аутентификация")
        return redirect(url_for('main_menu'))
    else:
      #  print(user_info_result.error_massage)
        print(user_info_result.result == 0)
        #if user_info_result.result != 0:
        return render_template('auth_error.html', message=user_info_result.error_massage)
        # else:
        #     return render_template('input_auth.html')



