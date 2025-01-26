import os
from string import Template  #класс, данными кото-го яв-ся переданная? строка

class SQLProvider:

    def __init__(self, file_path):  # как работает, что передается и тд
        self.scripts = {}
        for file in os.listdir(file_path):          #os.listdir возвращает список имен файлов в директории file_path
            _sql = open(f"{file_path}/{file}").read()    #Откр. файл с именем file в директории file_path, счит. его содержимое и сохр. в перем. _sql
            self.scripts[file] = Template(_sql)  #символьный шаблон содер-щий стр скл запроса - нач. данные в темплате
                                                    #Сохраняет объект Template в словарь scripts под ключом, равным имени файла.
    def get(self, file, **kwargs):
        sql = self.scripts[file].substitute(**kwargs)     #substitute заменяет переменные в шаблоне на значения, переданные в **kwargs.
        return sql

