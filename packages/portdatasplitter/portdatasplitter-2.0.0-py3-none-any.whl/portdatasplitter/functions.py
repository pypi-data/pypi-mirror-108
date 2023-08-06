from portdatasplitter import settings as s
import serial


def get_data_from_port(port):
    """ Прочитать и вернуть данные из переданного порта """
    try:
        data = port.readline()
    except serial.serialutil.SerialException:
        # Если не выйдет - вернуть код ошибки
        data = s.scale_disconnected_code
    return data
