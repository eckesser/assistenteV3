import json
import os

def save_to_json(life_percent, prayer_percent, pet_life_percent):
    # Verifica se a pasta 'Json' existe, caso contrário, cria
    if not os.path.exists('Json'):
        os.makedirs('Json')

    data = {
        'life_percent': life_percent,
        'prayer_percent': prayer_percent,
        'pet_life_percent': pet_life_percent
    }

    with open('Json/percent_key.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    life_percent = int(input("Informe a porcentagem (em valor inteiro) para life_percent: "))
    prayer_percent = int(input("Informe a porcentagem (em valor inteiro) para prayer_percent: "))
    pet_life_percent = int(input("Informe a porcentagem (em valor inteiro) para pet_life_percent: "))

    save_to_json(life_percent, prayer_percent, pet_life_percent)
    print("Dados salvos com sucesso!")
