# ФАЙЛ С КЛАССОМ, СОДЕРЖАЩИМ ИНФУ О РЕЗУЛЬТАТЕ

from flask import request
from dataclasses import dataclass
from database.select import select_list
from datetime import datetime


@dataclass  # класс данных, методы __init__ и т.п. создаются автоматически
class ProductInfoResponse:
    result: tuple
    error_massage: str
    status: bool


def model_route(db_config, user_input_data, sql_provider):
    error_massage = ''
    user_request = request.endpoint  # название блюпринта + название обработчика
    user_bp = user_request.split('.')[1]
    print(user_bp)

    months = [
        "январь", "февраль", "март", "апрель", "май", "июнь",
        "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
    ]

    if user_bp == 'query_index':
        if 'month_exceed' not in user_input_data or user_input_data['month_exceed'] == "" or 'year_exceed' not in user_input_data or user_input_data['year_exceed'] == "":  # если временной промежуток не определен
            print('user_input_data=', user_input_data)
            error_massage = 'Временной промежуток не получен'
            result = ()
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        elif user_input_data['month_exceed'].isdigit() is False:
            print('user_input_data=', user_input_data)
            error_massage = 'Месяц должен быть натуральным числом'
            result = ()
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        elif user_input_data['year_exceed'].isdigit() is False:
            print('user_input_data=', user_input_data)
            error_massage = 'Год должен быть натуральным числом'
            result = ()
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        elif int(user_input_data['month_exceed']) < 1 or int(user_input_data['month_exceed']) > 12:
            result = ()
            error_massage = 'Месяц должен быть в диапазоне от 1 от 12'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        current_date = datetime.now()
        current_year = int(current_date.year)
        if int(user_input_data['year_exceed']) < 1900 or int(user_input_data['year_exceed']) > current_year:
            result = ()
            error_massage = f'Год должен быть в диапазоне от 1900 до {current_year}'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        _sql = sql_provider.get('product.sql', year_exceed=user_input_data['year_exceed'], month_exceed=user_input_data['month_exceed'])  # получаем sql запрос
        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)   # получаем кортеж и список имен столбцов
        print('result_query', result)
        if result == -1:
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        if len(result) == 0:    # если по данной категории ничего не найдено
            month_rus = months[int(user_input_data['month_exceed']) - 1]
            error_massage = f"Превышений лимита за {month_rus} {user_input_data['year_exceed']} года не найдены"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)

    if user_bp == 'query_index1':
        if 'bill_days' not in user_input_data or user_input_data['bill_days'] == "":  # если временной промежуток не определен
            print('user_input_data=', user_input_data)
            error_massage = 'Временной промежуток не получен'
            result = ()
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        elif user_input_data['bill_days'].isdigit() is False:
            print('user_input_data=', user_input_data)
            error_massage = 'Количество дней должно быть натуральным числом'
            result = ()
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        elif int(user_input_data['bill_days']) < 1:
            result = ()
            error_massage = 'Количество дней должно быт положительным числом'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        _sql = sql_provider.get('bill.sql', bill_days=user_input_data['bill_days'])  # получаем sql запрос
        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)   # получаем кортеж и список имен столбцов
        print('result_query', result)
        if result == -1:
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        if len(result) == 0:    # если по данной категории ничего не найдено
            error_massage = f"Счета за последние {user_input_data['bill_days']} дней не найдены"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)

    if user_bp == 'query_index2':
        factor = ''
        if user_input_data['worker_role'] != "":  # если временной промежуток не определен
            factor = f"where worker_role='{user_input_data['worker_role']}'"
            print(f'not empty, ({user_input_data['worker_role']})')
        if user_input_data['worker_role'] == "":
            factor = f"order by worker_role"
        _sql = sql_provider.get('workers.sql', factor=factor)  # получаем sql запрос
        print('_sql=', _sql)
        result, schema = select_list(db_config, _sql)   # получаем кортеж и список имен столбцов
        print('result_query', result)
        if result == -1:
            error_massage = 'Ошибка доступа'
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        if result is None:
            error_massage = 'Ошибка sql запроса'
            return ProductInfoResponse((), error_massage=error_massage, status=False)
        if len(result) == 0:    # если по данной категории ничего не найдено
            error_massage = f"По должности {user_input_data['worker_role']} работники не найдены"
            return ProductInfoResponse(result, error_massage=error_massage, status=False)
        print(result)
        print(schema)
        return ProductInfoResponse(result=result, error_massage=error_massage, status=True)