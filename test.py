# import pytesseract    #   requires heroku buildpack!!!!!!!
# from PIL import Image
# import cv2
# import difflib
# import csv
# import re

# _MONTH = "not set"
# _GYM = "not set"
# _DATE = "not set"

# print("opening image")
# image = Image.open('/Users/MurphDogg/Desktop/image.png')
# # image = Image.open('/Users/MurphDogg/Desktop/image.jpg')

# print("cropping")
# originalWidth = image.size[0]
# originalHeight = image.size[1]
# oneTenthWidth = originalHeight / 10
# oneQuarterHeight = originalHeight / 4
# x1 = oneTenthWidth
# y1 = oneQuarterHeight*.75
# x2 = (originalWidth-oneTenthWidth)
# y2 = (originalHeight-(oneQuarterHeight*2))
# cropped = image.crop((x1, y1, x2, y2))
# cropped.save('/Users/MurphDogg/Desktop/cropped.png')         # need to delete this i think after finished

# print("finished cropping")
# img = cv2.imread('/Users/MurphDogg/Desktop/cropped.png', 1)

# lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# cv2.imshow("lab",lab)

# l, a, b = cv2.split(lab)
# cv2.imshow('l_channel', l)
# cv2.imshow('a_channel', a)
# cv2.imshow('b_channel', b)

# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# cl = clahe.apply(l)
# cv2.imshow('CLAHE output', cl)

# limg = cv2.merge((cl,a,b))
# cv2.imshow('limg', limg)

# final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
# cv2.imshow('final', final)

# rawText = pytesseract.image_to_string(final, config ='--psm 6')

# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'setiembre', 'octubre', 'noviembre', 'diciembre']
# monthFound = False
# for month in months:

    
#     if rawText.find(month) > -1:
#         monthFound = True
#         if month in ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'setiembre', 'octubre', 'noviembre', 'diciembre']:
           
#             spanishMonthToEnglish = {
#                 'enero': 'January',
#                 'febrero': 'February',
#                 'marzo': 'March',
#                 'abril': 'April',
#                 'mayo': 'May',
#                 'junio': 'June',
#                 'julio': 'July',
#                 'agosto': 'August',
#                 'septiembre': 'September',
#                 'setiembre': 'September',
#                 'octubre': 'October',
#                 'noviembre': 'November',
#                 'diciembre': 'December'
#             }
#             print("processing spanish date -> ")
#             rawText = rawText.split("\n")
#             strippedText = [line for line in rawText if line.strip()]
#             print(strippedText)
#             i=0
#             extractedGym = "not set"
#             for chunk in strippedText:
                
#                 if month in chunk:
#                     print("month found in strippedText[" + str(i) + "]")
#                     extractedDate = strippedText[i]
#                     print(extractedDate)
#                     dateParts = extractedDate.split(" ")
#                     print("month")
#                     print(dateParts[1])
#                     print("day")
#                     print(dateParts[0])
#                     print("time")
#                     print(dateParts[2])
#                     print("Date converted to english format -> ")
#                     englishMonth = spanishMonthToEnglish[dateParts[1]]
#                     englishDateFormat = (englishMonth + " " + dateParts[0] + " ")
#                     hour = dateParts[2]
#                     hour = hour.split(":")
#                     hourPartOne = int(hour[0])
#                     hourPartTwo = int(hour[1])
#                     if hourPartOne > 11:
#                         if hourPartOne > 12:
#                             hourPartOne =- 12
                        
#                         englishDateFormat += str(hourPartOne) + ":" + str(hourPartTwo) + " PM"
#                         _MONTH = month
#                     else: 
#                         englishDateFormat += str(hourPartOne) + ":" + str(hourPartTwo) + " AM"
#                         _MONTH = month
#                     # extractedGym = strippedText[i+1]
                    
#                 else:
#                     i+=1


         
#             # print("\n\n\n")
#             # print("--------------------------------------")
#             # print("DATE ->    " + englishDateFormat)
#             # print("GYM ->     " + extractedGym)
#             # print("--------------------------------------")
#             # _GYM = extractedGym
#             _DATE = englishDateFormat
#         else:
#             extractedDate = rawText[rawText.find(month):rawText.find(month)+len(month)+25]
#             strNoMonth = extractedDate[len(month):]
#             strNoMonth = strNoMonth.strip()
#             startTime = strNoMonth[:strNoMonth.find('M')+1]
#             extractedDate = month + " " + startTime[:-2].strip() + " " + startTime[-2:]
#             # rawText = rawText.split("\n")
#             # strippedText = [line for line in rawText if line.strip()]
#             # print(strippedText)
#             # i=0
#             # extractedGym = "not set"
#             # for chunk in strippedText:
                
#             #     if month in chunk:
#             #         extractedGym = strippedText[i+1]
#             #     else:
#             #         i+=1

 

           
#             # print("\n\n\n")
#             # print("--------------------------------------")
#             # print("DATE ->    " + extractedDate)
#             # print("GYM ->     " + extractedGym)
#             # print("--------------------------------------")
#             # _GYM = extractedGym
#             _DATE = extractedDate
#             _MONTH = month
#         break
    
        


# if not monthFound:  

#     print("--------------------------------------")
#     print("could not find a month in raw text -> ")
#     print(rawText)
#     print("--------------------------------------")
#     print("searching for possible matches -> ")

#     for month in months:

#             i=0
#             extractedDate = "not set"
#             lines = rawText.split("\n")
#             for line in lines:

#                 regex = re.compile('[^a-zA-Z]')
#                 #First parameter is the replacement, second parameter is your input string
#                 alphaOnly = regex.sub('', line)
#                 alphaOnly = alphaOnly[:-4]
#                 percentage = difflib.SequenceMatcher(None, alphaOnly, month).ratio()
#                 if percentage > .6:
#                     print("month found in alphaOnly")
#                     print(alphaOnly)
#                     print("possible match with " + month)
#                     alphaOnly = line.replace(alphaOnly, month)
#                     extractedDate = alphaOnly
#                     extractedDate = extractedDate.split(" ")
#                     _DATE = extractedDate[0] + " " + extractedDate[1] + " " + extractedDate[2][:-2].strip() + " " + extractedDate[2][-2:]

#             _MONTH = month
#             monthFound = True

# print("month set as " + _MONTH)
# print("starting loop to set gym")
# rawText = rawText.split("\n")
# print("raw text -> ")
# print(rawText)
# print("stripped text")
# strippedText = [line for line in rawText if line.strip()]
# print(strippedText)
# i=0
# extractedGym = "not set"
# print("loop for gym")
# for chunk in strippedText:

#     if _MONTH in chunk:
#         print()
#         extractedGym = strippedText[i+1]
#     else:
#         i+=1

# print("loop has found possible gym -> " + extractedGym)
# _GYM = extractedGym

# print("finished with text extraction")
# print("_GYM (verification needed still)-> " + _GYM)
# print("_DATE -> " + _DATE)
# print("begin comparing gym names")

# checkDay = _DATE.split(" ")
# day = checkDay[1]
# try:
#     dayInt = int(day)
# except ValueError:
#     print("ERROR: unable to parse day -> " + day)
#     #  dm admin for verification


# GYMS = []
# with open("gyms.txt", mode="r") as infile:
#     reader = csv.reader(infile)
#     for row in reader:
#         GYMS.append(row[0])


# matches = []
# for value in GYMS:
#     percentage = difflib.SequenceMatcher(None, _GYM, value).ratio()
#     if percentage > .9:
#         print(_GYM + "     " + str(percentage * 100)[:5] + "% match with  -> " + value)
#         matches.append(value)


# print('matches contains ' + str(len(matches)) + ' results')
# if len(matches) > 1:
    
#     print("matching gyms: \n")
#     for k in matches:
#         print(k)
        

# elif len(matches) == 1:
#     print("exactly one match -> ")
#     print(matches[0])
# elif len(matches) < 1:
#     print("no matches found.. sad day")

# print("\n\nDone.")