import socket
import threading
from serial import Serial
import serial.tools.list_ports
from time import sleep
from portdatasplitter import settings as s
from traceback import format_exc
from portdatasplitter import functions
from gravity_core_api.main import GCSE


class PortDataSplitter:
    """ Сервер для прослушивания порта port_name (USB, COM),
     и переотправки данных подключенным к нему клиентам (Clients)."""
    def __init__(self, ip: str, port: int, port_name='/dev/ttyUSB0', debug=False, device_name='unknown', test_mode=False,
                 test_value='101010', api_debug=False, *args, **kwargs):
        """ Принимает:
        IP :str - IP адрес, на котором будет размещаться сервер рассылки входных данных,
        port :int - порт данного сервера,
        port_name :str - имя порта, откуда будут приходить входные данные
        debug :bool - режим дебага, выводит в поток вывода дополнительную информацию
        device_name :str - имя устройства, с которого приходят данные (это имя можно использовать для парсинга данных,
            характерных именно для этого устройства, например)
        test_mode :bool - Тестовый режим, PDS не подключается к port_name, а отправляет через сервер рассылки данные,
            из атрибута test_value
        test_value :str - данные, которые рассылает сервер рассылки. Его можно установить через метод set_test_value
        """
        self.start_api(ip, port, api_debug)
        self.device_name = device_name
        self.debug = debug
        self.port_name = port_name
        self.data_list = [s.no_data_code]
        self.server_ip = ip
        self.server_port = port
        self.test_mode = test_mode
        self.test_value = test_value                  # В режиме тестов отправялет клиентам это значение

    def start_api(self, ip, port, api_debug):
        """ Запустить API PDS"""
        sqlshell = None
        self.api_server = GCSE(ip, port, sqlshell, self, debug=api_debug)
        threading.Thread(target=self.api_server.launch_mainloop, args=()).start()

    def get_api_support_methods(self, *args, **kwargs):
        """ Открыть метод для API """
        api_methods = {'set_test_value': {'method': self.set_test_value}}
        return api_methods

    def set_test_value(self, test_value, *args, **kwargs):
        """ Установить тестовое значение
        """
        self.test_value = test_value

    def get_all_connected_devices(self):
        # Показать все подключенные к этому компьютеру устройства
        ports = serial.tools.list_ports.comports()
        self.show_print('\nAll connected devices:')
        for port in ports:
            self.show_print('\t', port)
        return ports

    def get_device_name(self):
        # Вернуть заданный этому устройству имя
        return self.device_name

    def start(self):
        """ Запустить работу PortDataSplitter"""
        # Запустить параллельный поток, который отправляет данные из self.data_list
        threading.Thread(target=self.sending_thread, args=(1,)).start()
        # Запустить основной поток, слушаюший заданный порт и отправляющий эти данные клиентам
        while True:
            try:
                self._mainloop()
            except:
                print(format_exc())
                sleep(5)

    def sending_thread(self, timing=1):
        # Поток отправки показаний весов
        print('START THREAD')
        while True:
            sleep(timing)
            self.send_data(self.data_list[-1])

    def send_data(self, data, *args, **kwargs):
        print("SENDING DATA")
        # Отправить данные по клиентам
        try:
            data = {'new_value': {'value': data}}
            self.show_print('sending:', data, debug=True)
            self.api_server.broadcast_sending(data)
            #conn.send(data)
        except:
            # Если данные отправить клиенту не удалось, удалить клиента из списка подписчиков
            self.show_print('\tFailed to send data to client')
            self.show_print(format_exc())

    def make_str_tuple(self, msg):
        # Перед отправкой данных в стандартный поток вывывода форматировать
        return ' '.join(map(str, msg))

    def show_print(self, *msg, debug=False):
        # Отправка данных в стандартный поток выводы
        msg = self.make_str_tuple(msg)
        if debug and self.debug:
            print(msg)
        elif not debug:
            print(msg)

    def _mainloop(self):
        # Основной цикл работы программы, слушает порт и передает данные клиентам
        self.show_print('\nЗапущен основной цикл отправки весов')
        # Нужно подождать около 5 секунд после запуска всего компа
        sleep(5)
        if not self.test_mode:
            self.port = Serial(self.port_name, bytesize=8, parity='N', stopbits=1, timeout=1, baudrate=9600)
        while True:
            if not self.test_mode:
                data = functions.get_data_from_port(self.port)
            else:
                data = self.test_value
                sleep(1)
            self.show_print('Data from port:', data, debug=True)
            if data:
                # Если есть данные проверить их и добавить в список отправки data_list
                data = self.check_data(data)
                self.prepare_data_to_send(data)
            else:
                print('No data')
                pass

    def check_data(self, data):
        self.show_print('Checking data in {}'.format(self.device_name), debug=True)
        return data

    def prepare_data_to_send(self, data):
        # Подготовить данные перед отправкой
        self.data_list = self.data_list[-15:]
        self.data_list.append(data)

    def reconnect_logic(self):
        # Логика, реализуемая при выключении терминала
        self.show_print('Терминал выключен!')
        self.port.close()
        self._mainloop()