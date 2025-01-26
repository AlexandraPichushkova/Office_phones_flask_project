# ФАЙЛ С КЛАССОМ, СОДЕРЖАЩИМ ИНФУ О РЕЗУЛЬТАТЕ

from flask import request
from dataclasses import dataclass
from database.select import select_list

months = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

@dataclass  # класс данных, методы __init__ и т.п. создаются автоматически
class ProductInfoResponse:
    result: tuple
    error_massage: str
    status: bool


def model_route(db_config, user_input_data, sql_provider, rep_dict):
    error_massage = ''
    print('error_massage', error_massage)
    user_request = request.endpoint  # название блюпринта + название обработчика
    user_bp = user_request.split('.')[1]
    print('user_bp', user_bp)

    if user_bp == 'report_index':
        error_massage = ''
        # if 'rep_month' not in user_input_data or user_input_data['rep_month'] == "" or 'rep_year' not in user_input_data or user_input_data['rep_year'] == "":  # если категория не определена
        #     print('user_input_data=', user_input_data)
        #     error_massage = 'Временной промежуток не получен'
        #     result = ()
        #     return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print('if', user_input_data['rep_id'] == 'exc_report')
        print('user_input_data[rep_id]', user_input_data['rep_id'])
        _sql = sql_provider.get('report_create.sql',  report=user_input_data['rep_id'], rep_month=user_input_data['rep_month'], rep_year=user_input_data['rep_year'])  # получаем sql запрос

        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)   # получаем кортеж и список имен столбцов
        print('result_report', result)
        if result == -1:   #не надо
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        if len(result) == 0:    # если по данной категории ничего не найдено
            month_rus = months[int(user_input_data['rep_month']) - 1]
            error_massage = f"Отчет за {month_rus} {user_input_data['rep_year']} год создан"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        error_massage = result[0][0]
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)

    if user_bp == 'report_index2':
        error_massage = ''
        # if 'rep_month' not in user_input_data or user_input_data['rep_month'] == "" or 'rep_year' not in user_input_data or user_input_data['rep_year'] == "":  # если категория не определена
        #     print('user_input_data=', user_input_data)
        #     error_massage = 'Временной промежуток не получен'
        #     result = ()
        #     return ProductInfoResponse(result, error_massage=error_massage, status=False)
        # _sql = sql_provider.get('report_view.sql', rep_month=user_input_data['rep_month'], rep_year=user_input_data['rep_year'])  # получаем sql запрос
        sql_query = rep_dict[user_input_data['rep_id']][0]
        print('rep_dict', rep_dict[user_input_data['rep_id']][0])
        _sql = sql_provider.get(sql_query, rep_month=user_input_data['rep_month'], rep_year=user_input_data['rep_year'])
        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)  # получаем кортеж и список имен столбцов
        print('result_report', result)
        print('LENR', len(result))
        if result == -1:
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        if len(result) == 0:  # если по данной категории ничего не найдено
            print('LLENR', len(result))
            month_rus = months[int(user_input_data['rep_month']) - 1]
            print(month_rus)
            error_massage = f"Отчет за {month_rus} {user_input_data['rep_year']} год не найден"
            print(error_massage)
            #error_massage = f"Отчет не найден"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        print('LENR', len(result))
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)
