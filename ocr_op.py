import pytesseract    #   requires heroku buildpack!!!!!!!
from PIL import Image
import cv2
import difflib
import csv
import re
import datetime

m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

_CURRENT_MONTH = m[datetime.datetime.now().month - 1]
_NEXT_MONTH = m[datetime.datetime.now().month]
print("_CURRENT_MONTH: " + _CURRENT_MONTH)

_MONTH = "not set"
_GYM = "not set"
_DATE = "not set"

months = {
            'January': 'enero',
            'February': 'febrero',
            'March': 'marzo',
            'April': 'abril',
            'May': 'mayo',
            'June': 'junio',
            'July': 'julio',
            'August': 'agosto',
            'September': 'septiembre',
            'October': 'octubre',
            'November': 'noviembre',
            'December': 'diciembre'
        }


realisticMonthsENG = []
realisticMonthsSPN = []

realisticMonthsENG.append(_CURRENT_MONTH)
realisticMonthsENG.append(_NEXT_MONTH)
realisticMonthsSPN.append(months[_CURRENT_MONTH])
realisticMonthsSPN.append(months[_NEXT_MONTH])

print("this is a list of possible months -> ")
print(str(realisticMonthsENG))
print(str(realisticMonthsSPN))
# functions


def cropAndContrast(image):
    print("cropping")
    originalWidth = image.size[0]
    originalHeight = image.size[1]
    oneTenthWidth = originalHeight / 10
    oneQuarterHeight = originalHeight / 4
    x1 = oneTenthWidth
    y1 = oneQuarterHeight*.75
    x2 = (originalWidth-oneTenthWidth)
    y2 = (originalHeight-(oneQuarterHeight*2))
    cropped = image.crop((x1, y1, x2, y2))
    cropped.save('/Users/MurphDogg/Desktop/cropped.png')         # need to delete this i think after finished
    print("finished cropping")
    img = cv2.imread('/Users/MurphDogg/Desktop/cropped.png', 1)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # cv2.imshow("lab",lab)
    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    # cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    # cv2.imshow('CLAHE output', cl)
    limg = cv2.merge((cl,a,b))
    # cv2.imshow('limg', limg)
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    # cv2.imshow('final', final)
    return final



def getRaw(img):
    print("getRaw()")
    rawText = pytesseract.image_to_string(img, config ='--psm 6')
    return rawText



def getMonth(rawText):
    print("getMonthFromRaw()")
    monthFound = False
    
    for month in realisticMonthsENG:
        if rawText.find(month) > -1:
            print("month found in english")                                                       # ENGLISH
            monthFound = True
           
            extractedDate = rawText[rawText.find(month):rawText.find(month)+len(month)+25]
            strNoMonth = extractedDate[len(month):]
            strNoMonth = strNoMonth.strip()
            startTime = strNoMonth[:strNoMonth.find('M')+1]
            extractedDate = month + " " + startTime[:-2].strip() + " " + startTime[-2:]
            _DATE = extractedDate
            
            _MONTH = month
            print("_MONTH")
            print(_MONTH)
            print("_DATE")
            print(_DATE)
            
            return {"status":"success", "date": extractedDate, "rawText": rawText }

    for month in realisticMonthsSPN:
        if rawText.find(month) > -1:                                                           # SPANISH
            print("month found in spanish")
            monthFound = True

            print("processing spanish date -> ")
            rawText = rawText.split("\n")
            strippedText = [line for line in rawText if line.strip()]
            print(strippedText)
            i=0
            # extractedGym = "not set"
            for chunk in strippedText:
                
                if month in chunk:
                    print("month found in strippedText[" + str(i) + "]")
                    extractedDate = strippedText[i]
                    print(extractedDate)
                    dateParts = extractedDate.split(" ")
                    print("month")
                    print(dateParts[1])
                    print("day")
                    print(dateParts[0])
                    print("time")
                    print(dateParts[2])
                    print("Date converted to english format -> ")
                    for monthEnglish, monthSpanish in months.items():
                        if monthSpanish == month:
                            month = monthEnglish


                    englishDateFormat = (month + " " + dateParts[0] + " ")
                    
                    hour = dateParts[2]
                    hour = hour.split(":")
                    hourPartOne = int(hour[0])
                    hourPartTwo = int(hour[1])
                    if hourPartOne > 11:
                        if hourPartOne > 12:
                            hourPartOne =- 12
                        
                        englishDateFormat += str(hourPartOne) + ":" + str(hourPartTwo) + " PM"
                        print(str(englishDateFormat))
                        _MONTH = month
                        _DATE = englishDateFormat
                    else: 
                        englishDateFormat += str(hourPartOne) + ":" + str(hourPartTwo) + " AM"
                        print(str(englishDateFormat))
                        _MONTH = month
                        _DATE = englishDateFormat

                    
                    print("--------------------------------------")
                    print("raw text date BEFORE being replaced with english")
                    print(rawText)
                    print("--------------------------------------")
                    rawText = "\n".join(rawText)
                    rawText = rawText.replace(chunk,englishDateFormat)
                    print("raw text date AFTER being replaced with english")
                    print(rawText)
                    print("--------------------------------------")
                    print("_DATE")
                    print(_DATE)
                else:
                    i+=1


            
                # print("\n\n\n")
                # print("--------------------------------------")
                # print("DATE ->    " + englishDateFormat)
                # print("GYM ->     " + extractedGym)
                # print("--------------------------------------")
                # _GYM = extractedGym
                _DATE = englishDateFormat
                
                return {"status":"success", "date": englishDateFormat, "rawText": rawText }

    

    # inital for loop ended, no month found
    print("--------------------------------------")
    print("month not found in english or spanish")
    print("raw text -> ")
    print("--------------------------------------")
    print(rawText)
    print("--------------------------------------")
    print("searching with difflib for possible matches -> ")

    

    for month in realisticMonthsENG:
        found = runDiffSeqMatch(rawText, month)
        if found["status"] == "success":
            return {"status":"success",  "date": found["date"], "rawText": found["rawText"] }
    if not monthFound:
        for month in realisticMonthsSPN:
            found = runDiffSeqMatch(rawText, month)
            if found["status"] == "success":
                return {"status":"success",  "date": found["date"], "rawText": found["rawText"] }
                

        
    
  
    return {"status":"error", "rawText": rawText }








def runDiffSeqMatch(rawText, month):
    print("\n\n\n\nentering the runDiffSeqMatch()")
    extractedDate = "not set"
    lines = rawText.split("\n")
    for line in lines:
        print("loop should RUN now")
        print("\nline")
        print(line)
        print("\n\n")
        regex = re.compile('[^a-zA-Z]')
        #First parameter is the replacement, second parameter is your input string
        alphaOnly = regex.sub('', line)
        print("alpha only (after regex) -> ")
        print(alphaOnly)
        print("strip last 4 off alpha only -> ")
        alphaOnly = alphaOnly[:-4]
        print(alphaOnly)
        print("running difflib sequencematcher")
        print("mathcing month -> "  + month)
        print("with alphaonly -> "  + alphaOnly)
        percentage = difflib.SequenceMatcher(None, alphaOnly, month).ratio()
        print("result percentage -> " + str(percentage*100)[:5] + "%" + " similarity)")
        if percentage > .7:
            print("month found in alphaOnly (" + str(percentage*100)[:5] + "% match)")
            print( alphaOnly + "  possible match with  " + month)
            rawText = rawText.replace(alphaOnly, month)
            replacedLine = line.replace(alphaOnly, month)
            print("replacing in raw text -> ")
            print(rawText)
            print("date line")
            print(replacedLine)
            extractedDate = replacedLine.split(" ")
            _DATE = extractedDate[0] + " " + extractedDate[1] + " " + extractedDate[2][:-2].strip() + " " + extractedDate[2][-2:]
            print('Extracted date:')
            print(_DATE)
            print("_MONTH set to:")
            _MONTH = month
            print(_MONTH)
            print("Stopping loop")
            return {"status": "success", "date": _DATE, "rawText": rawText }

    return {"status":"error", "date": "not set", "rawText": rawText }    





def getGym(raw):
    print("getGym()")
  








  

    return True










# end of functions
# START PROGRAM


print("opening image")
# image = Image.open('/Users/MurphDogg/Desktop/image.png')
image = Image.open('/Users/MurphDogg/Desktop/image.jpg')
# image = Image.open('/Users/MurphDogg/Desktop/spanish.png')


croppedImg = cropAndContrast(image)
raw = getRaw(croppedImg)
results = getMonth(raw)
_DATE = results['date']
print("--------------------------------------")
print("--------------------------------------")
print("results from getMonth()")
print("results['status']")
print(results['status'])
print("results['date']")
print(results['date'])
print("results['rawText']")
print(results['rawText'])
print("--------------------------------------")
print("--------------------------------------")

if results["status"] == "success":
   
    _GYM = getGym(results["rawText"])

    #    push to firebase

elif results["status"] == "error":
    print("\n\n")
    print("--------------------------------------")
    print("unable to process screenshot       -> ")
    print("--------------------------------------")
    print("status -> ")
    print(raw["status"])
    print("--------------------------------------")
    print("rawtext -> ")
    print(raw["rawText"])
    print("--------------------------------------")
    

    #    DM admin    do not push to firebase
print("\n\nfinished.")
print("_DATE")
print(_DATE)
print("_GYM")
print(_GYM)