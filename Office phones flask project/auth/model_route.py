from dataclasses import dataclass
from database.select import select_list

@dataclass  # класс данных, методы __init__ и т.п. создаются автоматически
class ProductInfoResponse:
    result: tuple
    error_massage: str
    status: bool

def model_route(db_config, user_input_data, sql_provider):
    error_massage = ''
    if 'login' not in user_input_data or 'password' not in user_input_data or user_input_data['password'] == "" or user_input_data['login'] == "":  # если категория не определена
        print('user_input_data=', user_input_data)
        error_massage = 'Логин или пароль не получен'
        result = (0)
        return ProductInfoResponse(result, error_massage=error_massage, status=False)
    _sql = sql_provider.get('user.sql', user_login=user_input_data['login'], user_pass=user_input_data['password'])  # получаем sql запрос
    print('_sql=', _sql)
    result, schema = select_list(db_config, _sql)   # получаем кортеж и список имен столбцов
    print('result_auth', result)
    if result == -1:
        error_massage = 'Ошибка доступа'
        return ProductInfoResponse(result, error_massage=error_massage, status=False)
    if result is None:
        error_massage = 'Ошибка sql запроса'
        return ProductInfoResponse((), error_massage=error_massage, status=False)
    if len(result) == 0:    # если по данной категории ничего не найдено
        error_massage = f"Данные о пользователе {user_input_data['login']} не найдены. Доступ запрещен"
        return ProductInfoResponse(result, error_massage=error_massage, status=False)
    print("res", result)
    print("sch", schema)
    return ProductInfoResponse(result=result, error_massage=error_massage, status=True)









# @dataclass
# class AuthInfoResponse:
#     result: tuple
#     error_massage: str
#     status: bool
#
#
# def model_route(db_config, user_input_data, sql_provider):
#     error_massage = ''
#     if 'login' not in user_input_data or user_input_data['login'] == "" or 'password' not in user_input_data or user_input_data['password'] == "":
#         print('user_input_data=', user_input_data)
#         error_massage = 'Логин и пароль не могут быть пустыми'
#         result = ()
#         return AuthInfoResponse(result, error_massage=error_massage, status=False)
#
#     _sql = sql_provider.get('user.sql', login=user_input_data['login'], password=user_input_data['password'])
#     print('_sql=', _sql)
#     result, schema = select_list(db_config, _sql)
#     if result == -1:    # если по данной категории ничего не найдено
#         error_massage = f"Ошибка доступа"
#         return AuthInfoResponse(result, error_massage=error_massage, status=False)
#     # if result is None:
#     #     error_massage = 'Ошибка sql запроса'
#     #     return AuthInfoResponse((), error_massage=error_massage, status=False)
#     if len(result) == 0:    # если по данной категории ничего не найдено
#         error_massage = f"данные о пользователе {user_input_data['login']} не найдены"
#         return AuthInfoResponse(result, error_massage=error_massage, status=False)
#     print(result)
#     print(schema)
#     return AuthInfoResponse(result=result, error_massage=error_massage, status=True)
