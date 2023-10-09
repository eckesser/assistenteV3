import json
import os

def get_keys_for(label, max_keys):
    """Get keys from user for a specific label."""
    keys = []
    while len(keys) < max_keys:
        key = input(f"Digite uma tecla para {label} ({len(keys)+1}/{max_keys}): ")
        if key:
            keys.append(key)
        else:
            break
    return keys

def get_number_of_keys(label, max_keys):
    """Get the number of keys the user wants to assign."""
    while True:
        try:
            num = int(input(f"Quantas teclas você deseja designar para {label} (máximo {max_keys}): "))
            if 0 < num <= max_keys:
                return num
            else:
                print(f"Por favor, insira um número entre 1 e {max_keys}.")
        except ValueError:
            print("Por favor, insira um número válido.")

def save_to_json(data, path):
    """Save data to a JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    # Ensure 'Json' directory exists
    if not os.path.exists("Json"):
        os.mkdir("Json")
    
    data = {}
    
    # Get number of keys from user and then the actual keys
    num_life_keys = get_number_of_keys("life_key", 3)
    data['life_key'] = get_keys_for("life_key", num_life_keys)
    
    num_prayer_keys = get_number_of_keys("prayer_key", 1)
    data['prayer_key'] = get_keys_for("prayer_key", num_prayer_keys)
    
    num_pet_life_keys = get_number_of_keys("pet_life_key", 2)
    data['pet_life_key'] = get_keys_for("pet_life_key", num_pet_life_keys)
    
    # Save data to teclas.json
    save_to_json(data, os.path.join("Json", "teclas.json"))

if __name__ == "__main__":
    main()
