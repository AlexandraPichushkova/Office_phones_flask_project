import json, os
from flask import Flask, render_template, Blueprint, current_app, request
from database.sql_provider import SQLProvider
from report.model_route import model_route
from database.select import select_list, select_dict
from access import login_required, group_required

blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')

provider = SQLProvider(
    os.path.join(os.path.dirname(__file__), 'sql'))  # соединяем путь к текущей дериктории и файлу с sql шаблоном

rep_dict = {'exc_report_': ('report_view.sql', ('ID отчета', 'Фамилия', 'Телефон', 'Сумма превышения')), 'unpaid_exc_report': ('report2_view.sql', ('ID отчета', 'ID платежки', 'Фамилия', 'Телефон', 'Сумма оплаты'))}

months = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

@blueprint_report.route('/create', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def report_index():
    if request.method == 'GET':
        return render_template('input_report.html')
    else:
        user_input_data = request.form  # записываем словарь с данными из формы
        print('input_data', user_input_data)
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider, rep_dict)  # получаем экземпляр класса с result, error_mas, status
        print(user_info_result.error_massage)
        return render_template('message.html', message=user_info_result.error_massage)

@blueprint_report.route('/select', methods=['GET', 'POST'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def report_index2():
    if request.method == 'GET':
        return render_template('input_report.html')
    else:
        user_input_data = request.form  # записываем словарь с данными из формы
        print('input_data', user_input_data)
        user_info_result = model_route(current_app.config['db_config'], user_input_data,
                                       provider, rep_dict)  # получаем экземпляр класса с result, error_mas, status
        print('status ', user_info_result.status)
        if user_info_result.status:  # если статус True, т.е. все отработало корректно
            products = user_info_result.result  # записываем кортеж
            month_rus = months[int(user_input_data['rep_month']) - 1]
            prod_title = f'Отчет за {month_rus} {user_input_data['rep_year']} год'
            print('True')
            # print(schema)
            print(rep_dict[user_input_data['rep_id']][1])
            return render_template('output_report.html', prod_title=prod_title, products=products, columns=rep_dict[user_input_data['rep_id']][1])  # рендер страницы
        else:
            print('error')
            return render_template('rep_error2.html', message=user_info_result.error_massage)

@blueprint_report.route('/menu', methods=['GET'])  # GET — это метод HTTP, который используется для запроса данных с сервера
@group_required
def report_menu():
    return render_template('report_menu.html')



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
