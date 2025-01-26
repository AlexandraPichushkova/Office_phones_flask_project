import json, os
from flask import Flask, render_template, Blueprint, current_app, request
from database.sql_provider import SQLProvider
from query.model_route import model_route
from database.select import select_list, select_dict
from access import login_required, group_required
import calendar
import locale


blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')

provider = SQLProvider(
    os.path.join(os.path.dirname(__file__), 'sql'))  # соединяем путь к текущей дериктории и файлу с sql шаблоном

months = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

@blueprint_query.route('/query_index', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def query_index():
    if request.method == 'GET':
        return render_template('input_category.html')
    else:
        user_input_data = request.form  # записываем словаль с данными из формы
        print(user_input_data['year_exceed'] == "", user_input_data['month_exceed'] == "")
        print(user_input_data['year_exceed'], user_input_data['month_exceed'])
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider)  # получаем экземпляр класса с result, error_mas, status
        if user_info_result.status:  # если статус True, т.е. все отработало корректно
            exceeds = user_info_result.result  # записываем кортеж
            print("exceeds", exceeds)
            month_rus = months[int(user_input_data['month_exceed']) - 1]
            title = f'Превышение лимита за {month_rus} {user_input_data['year_exceed']} год:'
            return render_template('dynamic.html', title=title, exceeds=exceeds)  # рендер страницы
        else:
            return render_template('error.html', message=user_info_result.error_massage)


@blueprint_query.route('/query_index1', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def query_index1():
    if request.method == 'GET':
        return render_template('input_bill_days.html')
    else:
        user_input_data = request.form  # записываем словаль с данными из формы
        print(user_input_data['bill_days'] == "")
        print(user_input_data['bill_days'])
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider)  # получаем экземпляр класса с result, error_mas, status
        print('user_info_result =', user_info_result)
        if user_info_result.status:  # если статус True, т.е. все отработало корректно
            bills = user_info_result.result  # записываем кортеж
            print(bills)
            title = f'Счета, выставленные за последние {user_input_data['bill_days']} дней:'
            return render_template('dynamic_bill_days.html', title=title, bills=bills)  # рендер страницы
        else:
            return render_template('error_bill.html', message=user_info_result.error_massage)


@blueprint_query.route('/query_index2', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def query_index2():
    if request.method == 'GET':
        return render_template('input_role.html')
    else:
        user_input_data = request.form  # записываем словаль с данными из формы
        print(user_input_data['worker_role'] == "")
        print(user_input_data['worker_role'])
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider)  # получаем экземпляр класса с result, error_mas, status
        print('user_info_result =', user_info_result)
        if user_info_result.status:  # если статус True, т.е. все отработало корректно
            worker_roles = user_info_result.result  # записываем кортеж
            print(worker_roles)
            title = f'Список сотрудников должности {user_input_data['worker_role']}'
            return render_template('dynamic_role.html', title=title, worker_roles=worker_roles)  # рендер страницы
        else:
            return render_template('error_worker.html', message=user_info_result.error_massage)


@blueprint_query.route('/query_menu', methods=['GET'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def query_menu():
    return render_template('query_menu.html')


















