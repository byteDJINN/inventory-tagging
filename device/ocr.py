import pytesseract

text = pytesseract.image_to_string('img.png')
print(text)