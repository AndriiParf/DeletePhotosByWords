import os
import json
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_text_in_image(image_path, search_words, tesseract_language, output_file):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=tesseract_language)
        found_words = [word for word in search_words if word.lower() in text.lower()]
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"Photo: {image_path}\n")
            if found_words:
                f.write(f"Found words: {', '.join(found_words)}\n")
            else:
                f.write("Text not found.\n")
            f.write(f"Text: {text}\n\n")

        if found_words:
            print(f"Found words {', '.join(found_words)} in image {image_path}. Writing to file.")
        else:
            print(f"No search words found in image {image_path}. Written to file.")

    except Exception as e:
        print(f"Error with file {image_path}: {e}")

def process_images_in_folder(folder_path, search_words, tesseract_language, output_file):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(folder_path, filename)
            find_text_in_image(image_path, search_words, tesseract_language, output_file)

with open('settings.json', 'r', encoding='utf-8') as settings_file:
    settings = json.load(settings_file)

folder_path = settings.get("folder_path", "C:\\TEST\\TEST")
search_words = settings.get("search_words", [])
tesseract_language = settings.get("tesseract_language", "eng")
output_file = settings.get("output_file", "results.txt")

open(output_file, 'w').close()

process_images_in_folder(folder_path, search_words, tesseract_language, output_file)
