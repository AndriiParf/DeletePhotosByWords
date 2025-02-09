import os
import json
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_text_in_image(image_path, search_words, tesseract_language):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=tesseract_language)
        for word in search_words:
            if word.lower() in text.lower():
                print(f"Text '{word}' found in image {image_path}. Deleting file.")
                os.remove(image_path)
                return
        print(f"No search words were found in image {image_path}.")
    except Exception as e:
        print(f"Error with file {image_path}: {e}")

def process_images_in_folder(folder_path, search_words, tesseract_language):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(folder_path, filename)
            find_text_in_image(image_path, search_words, tesseract_language)

with open('settings.json', 'r', encoding='utf-8') as settings_file:
    settings = json.load(settings_file)

folder_path = settings.get("folder_path", r"C:\TEST\TEST")
search_words = settings.get("search_words", [])
tesseract_language = settings.get("tesseract_language", "eng")

process_images_in_folder(folder_path, search_words, tesseract_language)
