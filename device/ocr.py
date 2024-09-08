import pytesseract

text = pytesseract.image_to_string('img6.jpg')
print(text)