import random
import threading
import time
from thread_720 import Thread_720

class Time720:
    def __init__(self):
        self.timer_thread = None

    def _timer_task(self, key_name):
        max_time = 720
        end_time = max_time - (0.1 * random.random() * max_time)  # Reduzindo até 10% do tempo total
        time.sleep(end_time)
        Thread_720().run()
        print(f"Tempo finalizado para a chave {key_name}!")

    def run(self, key_name):
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()  # Esperando a thread anterior finalizar, se estiver rodando

        self.timer_thread = threading.Thread(target=self._timer_task, args=(key_name,))
        self.timer_thread.start()
