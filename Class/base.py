import time

from Class.shared import running, paused
from Class.shared import clear_console

class Base:
    def __init__(self, getter, threshold_percent, keys=None):
        self.getter = getter
        self.threshold_percent = threshold_percent
        self.keys = keys

    def execute(self):
        while running:
            if not paused:
                try:
                    value = self.getter()
                    if value > 100:
                        continue  # Ir para a próxima iteração do loop se o valor for maior que 100.
                    if value <= self.threshold_percent:
                        self.action()
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error in {self.__class__.__name__}: {e}. Restarting...")
                    continue
                print(f"{self.getter}: {value} %")
                #clear_console()

    def action(self):
        raise NotImplementedError
    