# recognizes characters in an image stores them in a string variable and writes it to a file
import pytesseract 
from PIL import Image, ImageEnhance, ImageFilter
import cv2

pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract"  #refer to the tesseract_OCR Dir
im = Image.open('UH8.png', mode = 'r')  #open the screenshot image that you get from the camera feed 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)  #raise the image contrast
im = enhancer.enhance(2)
im = im.convert('1')  #convert image to B&W
im.save('temp2.jpg')  #saves the enhanced image
text1 = pytesseract.image_to_string(im, lang = 'eng')
text2 = "the extraxted text from the image is:\n" + text1
if text1 == 'UH8' :
        text1 = 'A'
elif text1 == 'L6R':
        text1 = 'B'
elif text1 == 'G7C' :
        text1 = 'C'
elif text1 == 'S1P':
        text1 = 'D'
elif text1 == 'JW3':
        text1 = 'E'
elif text1 == 'A2X':
        text1 = 'F'
print(text2)
file = open ("Text.txt", "w")
file.write(text2 + '\nplane type:' + text1)
file.close()
