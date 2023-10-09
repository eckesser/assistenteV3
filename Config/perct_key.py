import json
import os

class JsonSaver:

    def __init__(self):
        pass

    def save_to_json(self, life_percent, prayer_percent, pet_life_percent):
        if not os.path.exists('Json'):
            os.makedirs('Json')

        data = {
            'life_percent': life_percent,
            'prayer_percent': prayer_percent,
            'pet_life_percent': pet_life_percent
        }

        with open('Json/percent_key.json', 'w') as f:
            json.dump(data, f, indent=4)

    def input_and_save(self):
        life_percent = int(input("Informe a porcentagem (em valor inteiro) para life_percent: "))
        prayer_percent = int(input("Informe a porcentagem (em valor inteiro) para prayer_percent: "))
        pet_life_percent = int(input("Informe a porcentagem (em valor inteiro) para pet_life_percent: "))

        self.save_to_json(life_percent, prayer_percent, pet_life_percent)
        print("Dados salvos com sucesso!")

saver = JsonSaver()
saver.input_and_save()
