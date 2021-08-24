import pytesseract
import cv2
import argparse
import os

ap = argparse.ArgumentParser()
group = ap.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--path", help="Folder Path for bulk check")
group.add_argument("-f", "--file", help="Image Path for single check")
args = vars(ap.parse_args())

imageList = []

if args['file']:
    print("Checking single file: " + args['file'])
    imageList += os.path.join(os.getcwd(), args['file'])

if args['path']:
    print("Checking multiple files in folder: " + args['path'])
    imageList = os.listdir(args['path'])
    imageList = list(map(lambda x: args['path'] + x , imageList))

backListWord = open('Blacklistwords.txt', 'r')
lines = backListWord.readlines()
lines = list(map(lambda x: x.replace('\n', ''), lines))

try:
    lines.remove('')
    lines.remove(' ')
except:
    pass

forbiddenWordDetected = False

"""
From tesseract documentation:

Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific.


Only the first 7 mode are required for our case:
"""

for image in imageList:
    img = cv2.imread(image)

    for i in range(1,7):
        forbiddenWordDetected = False
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
        print ("Danger detected in: " + image)
    else:
        print("The danger could not be detected in: " + image)
