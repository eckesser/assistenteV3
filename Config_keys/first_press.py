import time
import threading

from Class.KeyPresser import KeyPresser
from Config_keys.time360 import Time360
from Config_keys.time720 import Time720

class FirstPress:
    def __init__(self, json_data):
        self.data = json_data
        self.time360_keys = ["ovl_key", "anti_fire_key", "Anti-fire", "anti_poison_key", "Anti-Poison", "aggression_key", "Aggression potion"]
        self.time720_keys = ["weapon_poison_key", "necro_mage_key"]

    def _press_key(self, key, value):
        """Press the key using KeyPresser and wait for 0.5 seconds."""
        if value:
            key_presser = KeyPresser(key, {key: value})
            key_presser.press()
            time.sleep(0.5)

    def run(self):
        """Process the JSON data and activate the keys."""
        # Press the keys
        for key, value in self.data.items():
            self._press_key(key, value)

        # Close all threads
        for thread in threading.enumerate():
            if thread is not threading.current_thread():
                thread.join()

        # Call Time360 and Time720 based on the keys
        for key, value in self.data.items():
            if key in self.time360_keys and value:
                Time360().run(key)
            elif key in self.time720_keys and value:
                Time720().run(key)

# Example usage:
# (Assuming you have already read the JSON using JsonReader and it's stored in a variable named json_data)
# first_press = FirstPress(json_data)
# first_press.run()
