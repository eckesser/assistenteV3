import time
from Class.shared import running, paused, restart
from Class.shared import clear_console

class Base:
    def __init__(self, getter, threshold_percent, action_callback):
        self.getter = getter
        self.threshold_percent = float(threshold_percent)  # Convert threshold_percent to float
        self.action_callback = action_callback

    def execute(self):
        while running:
            if not paused:
                try:
                    value = self.getter()
                    # Convert the value to float safely
                    if isinstance(value, str):
                        try:
                            value = float(value)
                        except ValueError:
                            raise ValueError(f"Getter returned a string that could not be converted to float: {value}")
                    elif not isinstance(value, (int, float)):
                        raise ValueError(f"Expected numeric value from getter but received: {type(value)}")

                    if value > 100:
                        continue  # Ir para a próxima iteração do loop se o valor for maior que 100.
                    if value < self.threshold_percent:
                        self.action()
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error in {self.__class__.__name__}: {e}. Restarting...")
                    continue
                #print(f"{self.getter.__name__}: {value} %")
                #clear_console()

    def action(self):
        self.action_callback()
