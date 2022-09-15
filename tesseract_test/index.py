from base64 import decode
import pytesseract
from PIL import Image

import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
folder_path =os.path.join(os.path.dirname(os.path.realpath(__file__)),'dist') 
file_path = os.path.join(folder_path,'0_265.png')
img = Image.open(file_path)
text = pytesseract.image_to_string(img,lang='eng+chi_sim')
with open(os.path.join(folder_path,'test.txt'),'w',encoding='utf8') as f:
    f.write(text)