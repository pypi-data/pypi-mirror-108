from witapi.main import WITClient
from witapi.tests import test_cfg
import time
import threading


def connect_thread():
    wclient = WITClient('192.168.100.118', 3001, 'Элеваторная', 'zeus17')
    wclient.make_connection()
    response = wclient.make_auth()
    wclient.send_file(r'C:\Users\faizi\OneDrive\Рабочий стол\путевка моя.xlsx')

if __name__ == '__main__':
    clients = [1,2]
    for client in clients:
        print('Starting', client)
        threading.Thread(target=connect_thread, args=()).start()
        print('sleeping')
        time.sleep(5)

