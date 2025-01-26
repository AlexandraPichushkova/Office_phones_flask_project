import json, os
from flask import Flask, render_template, Blueprint, current_app, request

from database import sql_provider
from database.sql_provider import SQLProvider
from business.model_route import model_route
from database.select import select_list, select_dict
from access import login_required, group_required
from flask import request
from database.select import select_list
from flask import session



blueprint_business = Blueprint('business_bp', __name__, template_folder='templates')

provider = SQLProvider(
    os.path.join(os.path.dirname(__file__), 'sql'))  # соединяем путь к текущей дериктории и файлу с sql шаблоном


@blueprint_business.route('/business', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def tariff_change():
    if request.method == 'GET':
        return render_template('input_worker.html')
    else:
        user_input_data = request.form  # записываем словарь с данными из формы
        print('input_data', user_input_data)
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider)  # получаем экземпляр класса с result, error_mas, status
        print('user_info_result', user_info_result)
        print('user_info_result.error_massage', user_info_result.error_massage)
        if user_info_result.status:
            return render_template('tariff_message.html', message=user_info_result.error_massage)
        else:
            print('error')
            return render_template('bus_error2.html', message=user_info_result.error_massage)

@blueprint_business.route('/check', methods=['GET'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def tariff_check():
    user_input_data = ()# записываем словарь с данными из формы
    print('input_data', user_input_data)
    user_id = session.get('user_id')
    print("user_id", user_id)
    user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                   provider)  # получаем экземпляр класса с result, error_mas, status
    print("user_info_result", user_info_result)
    if user_info_result.status:  # если статус True, т.е. все отработало корректно
        products = user_info_result.result  # записываем кортеж
        prod_title = f'Ваш тариф:'
        print('True')
        # print(schema)
        return render_template('output_tariff.html', columns=user_info_result.result, prod_title=prod_title)  # рендер страницы
    else:
        print('error')
        return render_template('bus_error2.html', message=user_info_result.error_massage)

@blueprint_business.route('/users', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def tariff_view():
    if request.method == 'GET':
        print("get")
        return render_template('input_view_worker.html')
    else:
        user_input_data = request.form  # записываем словарь с данными из формы
        print('input_data', user_input_data)
        user_id = session.get('user_id')
        print("user_id", user_id)
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider)  # получаем экземпляр класса с result, error_mas, status
        print("user_info_result", user_info_result)
        if user_info_result.status:  # если статус True, т.е. все отработало корректно
            products = user_info_result.result  # записываем кортеж
            print('True')
            # print(schema)
            return render_template('output_worker_tariff.html', columns=user_info_result.result, title=user_info_result.error_massage)  # рендер страницы
        else:
            print('error')
            return render_template('bus_error3.html', message=user_info_result.error_massage)


@blueprint_business.route('/menu', methods=['GET'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def business_menu():
    return render_template('business_menu.html')



if __name__ == '__main__':
    current_app.run(host = '127.0.0.1', port = 5001)

















# @blueprint_query.route('/')
# @group_required    #у меня было @login_required
# def query_index():
#     prod_category = 1
#     _sql = f"""select prod_name, prod_measure, prod_price from product
#             where prod_category = {prod_category}"""
#     products = select_dict(current_app.config['db_config'], _sql)
#     if products:
#         prod_title = 'Результат из БД'
#         return render_template('dynamic.html', prod_title=prod_title, products = products)
#     else:
#         return 'Результат не получен'
