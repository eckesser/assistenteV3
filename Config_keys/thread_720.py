import threading
import time

from Class.KeyPresser import KeyPresser

class Thread_720:
    def __init__(self, keys_config):
        self.keys_config = keys_config

    def _press_keys(self):
        for key, config in self.keys_config.items():
            if config:
                presser = KeyPresser(key, self.keys_config)
                presser.press()
                time.sleep(0.5)

        # Importando Time720 aqui para evitar um loop de importação.
        from Config_keys.time720 import Time720
        Time720().run()

    def run(self):
        thread = threading.Thread(target=self._press_keys)
        thread.start()
