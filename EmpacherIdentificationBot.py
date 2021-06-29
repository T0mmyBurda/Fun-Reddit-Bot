#This program will periodically check new posts on r/rowing
#if any of the entered keywords are present in the post title

import praw
import os
import time
import datetime
import urllib
from PIL import Image , ImageShow

#creates reddit instance
creds = open("SecretStuff.txt", "r").read().split("\n")

try:
    reddit = praw.Reddit(client_id = creds[0] , client_secret = creds[1] ,
                         user_agent = creds[2] , username = creds[3] , password=creds[4])
except:
     print("Secret file configured incorrectly")


#notification code
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def searchSubreddit():#(subName , searchTerms , last):

    for submission in reddit.subreddit("rowing").new(limit=200):

        url = str(submission.url)

        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            urllib.request.urlretrieve(url, f"EmpacherImagesTemp/image{submission}")
            print("image found")

            path = "EmpacherImagesTemp/image" + str(submission)
            print(path)
            if(isEmpacher(path , str(submission))):
                submission.reply("Is that a yellow WinTech?")
                #notify("CAM_BOT", "Empacher found at " + url)
                print("empacher found\n")
            else:
                print("no empacher\n")



def folderEmpty(path):

    dir = os.listdir(path)
    if len(dir) == 0:
        return True
    else:
        return False


def isEmpacher(imgPath , subID):
    rAvg = 214
    gAvg = 205
    bAvg = 125

    thresh = .006
    leeway = 25
    empPix = 0

    img = Image.open(imgPath)
    #ImageShow.show(img , imgPath)
    pixels = img.load()

    imgX = img.size[0]
    imgY = img.size[1]

    examp = pixels[0 , 0]
    r = examp[0]
    print(examp)
    print(abs(r - rAvg))
    
    for x in range(0 , imgX):
        for y in range(0 , imgY):
            curPix = pixels[x , y]
            r = curPix[0]
            g = curPix[1]
            b = curPix[2]

            if(abs(r - rAvg) < leeway and abs(g - gAvg) < leeway and abs(b - bAvg) < leeway):
                empPix += 1
                pixels[x , y] = (245, 75, 66, 255)

    print(empPix)
    print(imgX * imgY)

    time = datetime.datetime.now()
    stringTime = time.strftime("%m-%d %H:%M")
    
    if(empPix / (imgX * imgY) > thresh):
        img.save("EmpacherTestImagesResults/" + subID + "::" + str(empPix / (imgX * imgY)) + ".png")

    return (empPix / (imgX * imgY) > thresh)
    



searchSubreddit()
