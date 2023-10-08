import pyautogui
import json
import os
from PIL import Image
import pytesseract

def find_text_coords(region):
    # Capture the screen region into an image
    screenshot = pyautogui.screenshot(region=region)
    # Use pytesseract to get the text from the image
    text = pytesseract.image_to_string(screenshot, config='--psm 6').strip()
    if all(char in "0123456789%/,." for char in text):
        # Locate the text on the screen
        text_location = pyautogui.locateOnScreen(screenshot, region=region)
        if text_location:
            # Return both the text and its location
            return text, f"{int(text_location.left)}, {int(text_location.top)}, {int(text_location.left + text_location.width)}, {int(text_location.top + text_location.height)}"
    return None, None

def find_image_coords(image_path, save_name):
    location = pyautogui.locateOnScreen(image_path, confidence=0.5)
    if location:
        text, text_coords = find_text_coords(location)
        if text and text_coords:
            # Extract the coordinates from the string
            x1, y1, x2, y2 = map(int, text_coords.split(','))
            # Capture only the text region
            text_screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
            # Save the image
            text_screenshot.save(os.path.join('img_retorno', f'{save_name}.png'))
        
        coords_str = f"{int(location.left)}, {int(location.top)}, {int(location.left + location.width)}, {int(location.top + location.height)}"
        if text_coords:
            coords_str += f" | {text_coords}"
        return coords_str
    else:
        return None

def main():
    # Create img_retorno folder if it doesn't exist
    if not os.path.exists('img_retorno'):
        os.makedirs('img_retorno')

    coords_life = find_image_coords('Imagem/hp.png', 'hp')
    coords_pray = find_image_coords('Imagem/prayer.png', 'prayer')
    coords_pet_life = find_image_coords('Imagem/summon_life.png', 'pet_life')

    data = {
        "coordinates": {
            "coords_life": coords_life,
            "coords_pray": coords_pray,
            "coords_pet_life": coords_pet_life
        }
    }

    if not os.path.exists('json'):
        os.makedirs('json')

    with open('json/coords.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()
