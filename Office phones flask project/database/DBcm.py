from pymysql import connect
from pymysql.err import OperationalError  #объект куда mysql поместит сообщ об ошибке если возникнет

class DBContextManager:   #контекстный менджер для управления соединения с бд

    def __init__(self, db_config: dict):
        self.conn = None        #трибут для хранения подключения к базе данных
        self.cursor = None      #атрибут для хранения курсора базы данных
        self.config = db_config     #Сохраняет переданную конфигурацию базы данных в атрибут config

    def __enter__(self):        # спец. метод, кот-ый вызывается при входе в блок with; возвр. объект, кот-й будет исп-ся внутри блока with
        try:        #для перехвата исключений
            self.conn = connect(**self.config)  #** - разбор именованных параметров на отдельные части
            self.cursor = self.conn.cursor()    #
            return self.cursor
        except OperationalError as err:
          ##  print(err.args)    # код ошибки + пояснение;  сам-но - обработка ошибок для каждой свой вывод?
             if err.args[0] == 1045:
                 print("Ошибка: Неверное имя пользователя или пароль.")
             elif err.args[0] == 2003:
                 print("Ошибка: Невозможно подключиться к серверу базы данных. Возможная причина ошибки: неверный хост или порт, сервер базы данных не запущен")
             elif err.args[0] == 1049:
                 print("Ошибка: Неизвестная база данных.")
          #   elif err.args[0] == 2002:
          #       print("Ошибка: Невозможно подключиться к локальному серверу базы данных через сокет.")
             elif err.args[0] == 1044:
                 print("Ошибка: Доступ к базе данных запрещен.")
             else:
                 print(f"Ошибка подключения к базе данных: {err}")
             return None

    def __exit__(self, exc_type, exc_val, exc_tb):  #метод, кот-й выз-ется при выходе из блока with. отв. за закр. ресурсов кот. были открыты в __enter__
        if exc_type:
            print(exc_type)
            print(exc_val)
        if self.cursor:
            if exc_type:   # если ошибки
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return True               # тк всё предусмотрели


