import random
import math
import time
from PyQt5 import QtWidgets


collision_window_backoff: float = 0.05

# делаешь случайную задержку
# для рассчета задержки используется формула из лекции
def backoff(n: int) -> None:
    k: int = 0
    if n > 10:
        k = 10
    else:
        k = n
    backoff: float = random.random() * math.pow(2, k) / 1000
    time.sleep(backoff)

# занят ли порт?
def is_port_free():
    if random.random() < 0.7:
        return True
    else:
        return False

# обнаружена ли коллизия?
def has_collision() -> bool:
    if random.random() <= 0.3:
        return True
    else:
        return False

# выхдать окно коллизий
def wait_collision_window() -> None:
    time.sleep(collision_window_backoff)

# отправить данные и вывести плюсы-минусы
def send_data(data: str, append_status) -> str:
    # вот эту строку ты юудешь отправлять
    data_to_send: str = ''
    for ch in data:
        while True:

            # ожидание когда порт станет свободным
            while not is_port_free():
                pass

            # счтчик попыток передачи
            counter: int = 0

            # отправка и выжидане окна коллизий
            data_to_send += ch
            wait_collision_window()

            # если произошла коллизия
            if has_collision():
                data_to_send += ch
                # вывод плюса
                append_status('+')
                # блокирует основной поток пока не выполнится вся асинхронка
                QtWidgets.QApplication.processEvents()

                counter += 1
                # попыток отправки слишком много
                if counter < 16:
                    backoff(counter)
                else:
                    break
            else:
                append_status('-')
                QtWidgets.QApplication.processEvents()
                break
        append_status(' ')
        QtWidgets.QApplication.processEvents()

    return data_to_send










