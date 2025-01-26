from database.DBcm import DBContextManager


def select_list(db_config: dict, _sql):  # возвращает результат запроса в форме двумерного списка
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            #raise ValueError('Курсор не создан')
            return (-1), []
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()  # двумерный список который содержит рез-ты запроса
            print('d', cursor.description)
            schema = []
            if cursor.description is not None:
                for item in cursor.description:
                    schema.append(item[0])
            print("S", schema)
            print("R",result)
            return result, schema
           # print(result)

def select_dict(db_config, _sql):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    print(result_dict)
    return result_dict
