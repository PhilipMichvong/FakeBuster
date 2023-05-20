import csv
import os
import pytesseract
import pandas as pd
from googletrans import Translator

from langdetect import detect
from PIL import Image


def open_folder(path):
    result = []
    try:
        files = os.listdir(path)
        for file in files:
            result.append(path + '/' + file)
    except FileNotFoundError:
        print(f"Katalog o nazwie {path} nie istnieje.")
    return result


def ocr(image_path):
    image = Image.open(image_path)
    text_from_ocr = pytesseract.image_to_string(image, lang="pol")
    return text_from_ocr


def prepare(data):
    df = pd.DataFrame({
        'Path': [],
        'Content': [],
        'Fake': []
    })
    for i in range(3):
        conn = str(ocr(data[i]))
        lang = detect(conn)
        tran_conn = translate(conn, lang=lang)
        df.loc[i, 'Path'] = data[i]
        df.loc[i, 'Content'] = tran_conn
        df.loc[i, 'Fake'] = 1
        print(data[i])

    return df


def translate(text, lang):
    translator = Translator()
    return translator.translate(text, src=lang, dest='en').text
