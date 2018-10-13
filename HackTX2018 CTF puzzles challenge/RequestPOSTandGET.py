#Post and Request to puzzle by UT



#importing the requests library
import requests
import random
import string
import json
import hashlib

catf = open("cats.txt", "r")
dogf = open("dogs.txt", "r")
kword = open("K-word.txt", "r")
kList = []
kLine = kword.readlines()
for a in kLine:
    kList.append(a)
catList = []
catLine = catf.readlines()
for x in catLine:
    catList.append(x)

dogList = []
dogLine = dogf.readlines()
for x in dogLine:
    dogList.append(x)
count = 0
URL = "http://18.224.118.57:2086/"
while count < 700:

    #CAPTCHAGET
    #print("CaptchaGet response:")
    captchaGet = requests.get("http://18.224.118.57:2086/captcha/get")
    text = captchaGet.json()
    textStr = str(text)
    #print(textStr)

    #Get challenge number
    challenge = textStr[15:47]

    #Get animal type
    animal = textStr[60:64]

    #Get imagesHashes
    Hashes = textStr[78:-2]

    imageHash = "["
    #Get correct hash
    correctHash = []
    counter = 0
    index = 0
    start = 0
    end = 38
    if animal == "cats":
        for i in range(9):
            index = index + 1
            imageNo = Hashes[start:end]
            start = end + 2;
            end = end + 40;
            imageNo = imageNo + "\n"
            for x in catList:
                if imageNo == str(x):
                    imageHash = imageNo[1:33]
                    correctHash.append(imageHash)
                    imageHash = ""

    if animal == "dogs":
        for i in range(9):
            index = index + 1
            imageNo = Hashes[start:end]
            start = end + 2;
            end = end + 40;
            imageNo = imageNo + "\n"
            for x in dogList:
                if imageNo == str(x):
                    imageHash = imageNo[1:33]
                    correctHash.append(imageHash)
                    imageHash = ""
    length = len(correctHash)
    if length == 0:
        payload = {'challenge': challenge}
    elif length == 1:
        payload = {'challenge': challenge,'selected': [correctHash[0]]}
    elif length == 2:
        payload = {'challenge': challenge,'selected': [correctHash[0],correctHash[1]]}
    elif length == 3:
        payload = {'challenge': challenge,'selected': [correctHash[0],correctHash[1], correctHash[2]]}
    elif length == 4:
        payload = {'challenge': challenge,'selected': [correctHash[0],correctHash[1], correctHash[2], correctHash[3]]}
    elif length == 5:
        payload = {'challenge': challenge,'selected': [correctHash[0], correctHash[1], correctHash[2], correctHash[3], correctHash[4]]}

    #CAPTCHAVERIFY
    #print("CaptchaVerify response: ")
    captchaVerify = requests.post("http://18.224.118.57:2086/captcha/verify", data = payload)
    #print(captchaVerify.text)
    verifyText = str(captchaVerify.text)
    verifiCation = verifyText[82:-2]

    #PROMO
    code = random.choice(kList)
    code = code[0:3]
    #print(code)
    #print("Promo response: ")
    headers = {'Host': '18.224.118.57:2086',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
               'Accept' : '*/*',
               'Accept-Language' : 'en-US,en;q=0.5',
               'Accept-Encoding' : 'gzip, deflate',
               'Referer': 'http://18.224.118.57:2086/',
               'content-type' : 'application/json',
               'origin' : 'http://18.224.118.57:2086',
               'Content-Length' : '112',
               'Cookie' : 'shopping-session=s%3AHWJg0dYEzE2smLUGwEjQBaB1aCmjkxof.hoWnNG3ylmAhHG4%2F0N96b2nd%2FHoWb0goxhCRurnc78c; puzzle-session=s%3A159SQf-VAv4GVVL21WNE9wRpR3-DfUsd.QfrIdLdpjcbV7mNkQigijYYQS3lNxtM1na2o1cQ6Uao'
               }
    #response = requests.get("http://18.224.118.57:2086/applypromo/", headers=headers)
    payload = {'code': code,'challenge': challenge,'verification': verifiCation}
    #promo = requests.post("http://18.224.118.57:2086/applypromo/", headers = headers)
    promo = requests.Request("POST", "http://18.224.118.57:2086/applypromo", json = payload, headers=headers)

    partnerInfoRequestPrepared = promo.prepare()
    requestSesh = requests.Session()
    partnerInfoResponse = requestSesh.send(partnerInfoRequestPrepared)
    print(partnerInfoResponse)

    #print(promo)  # should be 200
    print(str(count))
    count = count + 1

