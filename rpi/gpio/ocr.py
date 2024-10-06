from PIL import Image
import pytesseract

def submit_text(socket):
    path = "/home/csseiot/Desktop/xxx.jpg"
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    socket.emit("ocr",text)