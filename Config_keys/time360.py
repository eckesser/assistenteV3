import random
import threading
import time

from Config_keys.thread_360 import Thread_360

class Time360:
    def __init__(self):
        self.timer_thread = None

    def _timer_task(self, key_name):
        max_time = 360
        end_time = max_time - (0.1 * random.random() * max_time)  # Reduzindo até 10% do tempo total
        time.sleep(end_time)
        Thread_360().run()
        print(f"Usando: {key_name}!")
        print(f"Usando novamente {key_name} em: {end_time} segundos")

    def run(self, key_name):
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()  # Esperando a thread anterior finalizar, se estiver rodando

        self.timer_thread = threading.Thread(target=self._timer_task, args=(key_name,))
        self.timer_thread.start()
