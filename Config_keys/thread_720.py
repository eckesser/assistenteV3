import threading
import time

import os
import sys
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

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
        from time720 import Time720
        Time720().run()

    def run(self):
        thread = threading.Thread(target=self._press_keys)
        thread.start()
