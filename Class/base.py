import time
from Class.shared import running, paused, pause_condition

class Base:
    def __init__(self, getter, threshold_percent, action_callback):
        self.getter = getter
        self.threshold_percent = float(threshold_percent)
        self.action_callback = action_callback
        self.invalid_value_count = 0

    def execute(self):
        global paused, pause_condition
        while running:
            with pause_condition:
                while paused:
                    pause_condition.wait()
            
            try:
                value = self.getter()
                if isinstance(value, str):
                    try:
                        value = float(value)
                    except ValueError:
                        raise ValueError(f"Getter returned a string that could not be converted to float: {value}")
                elif not isinstance(value, (int, float)):
                    raise ValueError(f"Expected numeric value from getter but received: {type(value)}")
                
                if value > 100:
                    continue
                
                if value < self.threshold_percent:
                    self.action()
                
                time.sleep(0.5)
                self.invalid_value_count = 0
            except Exception as e:
                self.invalid_value_count += 1 
                if self.invalid_value_count >= 10: 
                    value = 100 
                    self.invalid_value_count = 0 
                from Config.coords import ImageFinder 
                finder = ImageFinder()
                finder.main()
                continue

    def action(self):
        self.action_callback()
