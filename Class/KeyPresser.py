import pyautogui

class KeyPresser:
    def __init__(self, key, config):
        self.key = key
        self.tecla_config = config.get(key, [])

    def press(self):
        if not self.tecla_config or self.tecla_config[0] is None:
            return
        try:
            for key in self.tecla_config:
                pyautogui.keyDown(key)
            for key in self.tecla_config:
                pyautogui.keyUp(key)
            print(f"Teclas {self.tecla_config} pressionadas com sucesso.")
        except Exception as e:
            print(f"Erro ao pressionar as teclas {self.tecla_config}: {e}")
    