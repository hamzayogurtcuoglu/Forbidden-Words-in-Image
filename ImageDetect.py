import pytesseract
import cv2
import matplotlib.pyplot as plt
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True,help="Image Path")
args = vars(ap.parse_args())

imgPath = os.path.join(os.getcwd(), args['path']);
img = cv2.imread(imgPath)

backListWord = open('Blacklistwords.txt', 'r')
lines = backListWord.readlines()
lines = list(map(lambda x: x.replace('\n', ''), lines))

try:
    lines.remove('')
    lines.remove(' ')
except:
    print("")

forbiddenWordDetected = False

for i in range(1,7):
    try:
        custom_config = r'--oem 3 -l tur --psm '
        custom_config += str(i)
        text = pytesseract.image_to_string(img, config=custom_config)
        for l in lines:
            if text.lower().find(l.lower()) != -1 :
                forbiddenWordDetected = True
    except:
        continue

if forbiddenWordDetected:
    print ("Danger detected.")
else:
    print("The danger could not be detected.")
