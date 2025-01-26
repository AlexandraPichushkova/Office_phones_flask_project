# ФАЙЛ С КЛАССОМ, СОДЕРЖАЩИМ ИНФУ О РЕЗУЛЬТАТЕ

from flask import request
from dataclasses import dataclass
from database.select import select_list
from flask import session


@dataclass  # класс данных, методы __init__ и т.п. создаются автоматически
class ProductInfoResponse:
    result: tuple
    error_massage: str
    status: bool


def model_route(db_config, user_input_data, sql_provider):
    error_massage = ''
    user_request = request.endpoint  # название блюпринта + название обработчика
    user_bp = user_request.split('.')[1]
    print('user_bp', user_bp)

    if user_bp == 'tariff_change':
        error_massage = ''
        # if 'rep_month' not in user_input_data or user_input_data['rep_month'] == "" or 'rep_year' not in user_input_data or user_input_data['rep_year'] == "":  # если категория не определена
        print('user_input_data=', user_input_data)
        # _sql = sql_provider.get(sql_query, rep_month=user_input_data['rep_month'], rep_year=user_input_data['rep_year'])  # получаем sql запрос
        _sql = sql_provider.get('tariff_change.sql',  worker=user_input_data['worker'], tariff=user_input_data['tariff_id'])  # получаем sql запрос
        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)   # получаем кортеж и список имен столбцов
        print('result_report', result)
        if result == -1:   #не надо
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        print(result)
        print(schema)
        error_massage = result[0][0]
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)

    if user_bp == 'tariff_check':
        error_massage = ''
        # sql_query = rep_dict[user_input_data['rep_id']][0]
        _sql = sql_provider.get('tariff_view.sql', user_id=session.get('user_id'))
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
            print('LENR', len(result))
            error_massage = f"Вам тариф не выдан"
            #error_massage = f"Отчет не найден"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        print('LENR', len(result))
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)

    if user_bp == 'tariff_view':
        error_massage = ''
        _sql = sql_provider.get('tariff_view.sql', user_id=user_input_data['worker'])
        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)  # получаем кортеж и список имен столбцов
        print('result_report', result)
        print('LENR', len(result))
        _name_sql = sql_provider.get(' get_name.sql', user_id=user_input_data['worker'])
        result_name, schema_name = select_list(db_config, _name_sql)
        print(result_name[0][0], schema_name)
        if result == -1:
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        if len(result) == 0:  # если по данной категории ничего не найдено
            print('LENR', len(result))
            error_massage = f"Тариф сотруднику {result_name[0][0]} не выдан"
            #error_massage = f"Отчет не найден"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        print('LENR', len(result))
        massage = f'Тариф сотрудника {result_name[0][0]}:'
        error_massage = massage
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)
