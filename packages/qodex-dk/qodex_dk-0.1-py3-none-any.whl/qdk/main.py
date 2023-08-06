from qsct.main import QSCT
from qdk import functions
from qdk import methods
import socket


class QDK(QSCT):
    """Qodex Development Kit - клиентская часть для подключения и взаимодействия с QPI"""
    def __init__(self, ip, port, login, password, debug='False', methods_dict={}):
        super().__init__(debug=debug)
        self.ip = ip
        self.methods_dict = methods_dict
        self.methods_dict.update(methods_dict)
        self.port = port
        self.login = login
        self.password = password

    def subscribe(self, *args, **kwargs):
        """ Подписаться на все данные от WITServer """
        return self.send_command(method_name='subscribe', *args, **kwargs)

    def send_command(self, method_name='hello_world', get_response=None, *args, **kwargs):
        functions.execute_method(self, self.methods_dict, method_name, get_response, **kwargs)
        if get_response:
            return self.get_data()

    def send_data(self, data, *args, **kwargs):
        """ Предопределить родительский метод send_data передав ему свой сокет"""
        super().send_data(self.sock, data)

    def get_data(self, *args, **kwargs):
        """Получить данные из сокета, объемом data_size. Если размер передаваемого объекта больше dataSize, -
        функция собирает объект по частям, пока не соберет его весь и возвращает результат"""
        self.show_print('\nОжидаем данные', debug=True)
        data = self.get_data(self.sock)
        return data

    def make_connection(self):
        """Создать соединение с QPI"""
        self.sock = socket.socket()
        self.show_print('\nMaking connection with WServer on {}:{}...'.format(self.ip, self.port), debug=True)
        self.sock.connect((self.ip, self.port))
        self.show_print('\tSuccess! Connection has been established.', debug=True)
        return self.sock

    def make_auth(self, method_name='auth_me', *args, **kwargs):
        """Отправить данные для авторизации """
        kwargs['login'] = self.login
        kwargs['password'] = self.password
        return self.send_command(method_name=method_name, *args, **kwargs)

    def get_sdk_methods(self, *args, **kwargs):
        """ Получить все поддерживаемые методы SDK """
        return self.methods_dict

    def get_api_methods(self, *args, **kwargs):
        """ Получить все методы API """
        return functions.extract_supported_methods(self)
