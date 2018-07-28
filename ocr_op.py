import pytesseract    #   requires heroku buildpack!!!!!!!
from PIL import Image
import cv2
import difflib
import csv
import re
import datetime
import time
# import operator
import string

m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

_CURRENT_MONTH = m[datetime.datetime.now().month - 1]
_NEXT_MONTH = m[datetime.datetime.now().month]
print("_CURRENT_MONTH: " + _CURRENT_MONTH)

_MONTH = "not set"
_GYM = "not set"
_DATE = "not set"

performanceSummary = []


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




def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        performanceStamp = ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        performanceSummary.append(performanceStamp)
        return result
    return timed




@timeit
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





@timeit
def getRaw(img):
    print("getRaw()")
    rawText = pytesseract.image_to_string(img, config ='--psm 6')
    return rawText




@timeit
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







@timeit
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



@timeit
def verifyDate(date):
    valid = True
    print("verifying date")
    splitDate = date.split(" ")
    print("Checking DAY in date..")
    month = splitDate[0]
    day = splitDate[1]
    hour = splitDate[2]
    ampm = splitDate[3]

    translator = str.maketrans('','',string.punctuation)
    month = month.translate(translator)
    day = day.translate(translator)
    ampm = ampm.translate(translator)


    regex = re.compile('^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$')
    res = regex.match(hour)
    if res is not None:
        print("result is not none! valid hour")
    else:
        print("result is none! no bueno")
        valid = False

    try:
        dayInt = int(day)
        print("day is number, valid result -> " + str(dayInt))
    except ValueError:
        valid = False
        print("ERROR: unable to parse day -> " + str(day))
        #  dm admin for verification
    
    for char in ampm:
        if char == "A" or char == "M" or char == "P":
            break
        else:
            valid = False

    if valid:
        vDate = (month + " " + day + " " + hour + " " + ampm)
        print("valid date -> " + vDate)
        return {"status": "success", "date": vDate}
    else:
        print("invalid date -> " + date)
        return {"status": "error", "date": date}




@timeit
def getGym(raw, date):
    print("getGym()")
    rawText = raw.split("\n")
    print("raw text -> ")
    print(rawText)
    print("stripped text")
    strippedText = [line for line in rawText if line.strip()]
    print(strippedText)
    i=0
    extractedGym = "not set"
    print("loop for gym")
    date = date.split(" ")
    _MONTH = date[0]
    for chunk in strippedText:

        if _MONTH in chunk:
            print("month in chunk...")
            print("extractedGym")
            extractedGym = strippedText[i+1]
            print(extractedGym)
        else:
            i+=1

    print("loop has found possible gym -> " + extractedGym)
    _GYM = extractedGym
    print("_GYM (verification needed still) -> " + _GYM)
    print("begin comparing gym names")




    GYMS = []
    with open("gyms.txt", mode="r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            GYMS.append(row[0])


    matches = []
    for value in GYMS:
        percentage = difflib.SequenceMatcher(None, _GYM, value).ratio()
        if percentage > .7:
            print(_GYM + "     " + str(percentage * 100)[:5] + "% match with  -> " + value)
            matches.append({"gym": value, "percent": str(percentage * 100)[:6]})


    print('matches contains ' + str(len(matches)) + ' results')
    if len(matches) > 1:
        
        print("\n\n\n\n\nMATCHING GYMS: \n")
        for k in matches:
            print(k["gym"] + "  " + k["percent"])
        
        # maxResult = max(float(match["percent"]) for match in matches)
        maxResult = max(matches, key = lambda m: float(m["percent"]))

        print("best match from matches  ->  " + str(maxResult))
        print("\n\n\n")
        matches = []
        matches.append(maxResult)

    if len(matches) == 1:
        print("exactly one match -> ")
        print(matches[0]["gym"])
        return {"status": "success", "gym": matches[0]["gym"]}
    elif len(matches) < 1:
        print("no matches found.. sad day")
        return {"status": "error", "gym": "not found"}
   


    print("\n\nDone.")
    return {"status": "error", "gym": "multiple found"}




def runThisShit(file):
    print("hello from  ocr_op")
    image = Image.open(file)


    print("opening image")

    # image = Image.open('/Users/MurphDogg/Desktop/image.png')
    # image = Image.open('/Users/MurphDogg/Desktop/image.jpg')
    # image = Image.open('/Users/MurphDogg/Desktop/spanish.png')


    croppedImg = cropAndContrast(image)
    raw = getRaw(croppedImg)
    results = getMonth(raw)
    # _DATE = results['date']

    verifiedDateResult = verifyDate(results['date'])
    if verifiedDateResult["status"] == "success":
        print("YYYYYAAAAAAAAAYYY success, day is valid")
        _DATE = verifiedDateResult["date"]
    else:
        print("BOOOOOOOOOOOOOOOO error, date is not valid -> " + verifiedDateResult["date"])
        print("DM admin...")


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
    
        gymResults = getGym(results["rawText"], results["date"])
        if gymResults["status"] == "success":
            _GYM = gymResults["gym"]
        #    push to firebase
        elif gymResults["status"] == "error":
            _GYM = gymResults["gym"]
        #    push to firebase
        else:
            print("SOMETHING IS WRONG. wtf")

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
    # print("performance summary: ")
    # for entry in performanceSummary:
    #     print(entry)
    # print("\n\nfinal result -> ")


    print("_DATE")
    print(_DATE)
    print("_GYM")
    print(_GYM)



    return {"date": _DATE, "gym": _GYM }