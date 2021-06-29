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

    for submission in reddit.subreddit("rowing").new(limit=):

        url = str(submission.url)

        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            urllib.request.urlretrieve(url, f"EmpacherImagesTemp/image{submission}")
            print("image found")

            path = "EmpacherImagesTemp/image" + str(submission)
            print(str(submission.title))
            if(isEmpacher(path , str(submission))):
                submission.reply("Is that a yellow WinTech?")
                #notify("CAM_BOT", "Empacher found at " + url)
                print("empacher found\n")
            else:
                print("no empacher\n")
        else:
            print(str(submission.title))
            print()



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

    thresh = .009
    leeway = 25
    empPix = 0

    img = Image.open(imgPath)
    #ogImg = img
    #ImageShow.show(img , imgPath)
    pixels = img.load()

    imgX = img.size[0]
    imgY = img.size[1]
    
    for x in range(0 , imgX):
        for y in range(0 , imgY):
            curPix = pixels[x , y]
            r = curPix[0]
            g = curPix[1]
            b = curPix[2]

            if(abs(r - rAvg) < leeway and abs(g - gAvg) < leeway and abs(b - bAvg) < leeway):
                empPix += 1
                pixDiff =  abs(r - rAvg) + abs(g - gAvg) + abs(b - bAvg)
                if(pixDiff <= 15):
                    pixels[x , y] = (245, 75, 66, 255)
                elif(pixDiff <= 30):
                    pixels[x , y] = (255, 140, 0, 255)
                else:
                    pixels[x , y] = (255, 247, 0, 255)

    # print(empPix)
    # print(imgX * imgY)
    print(empPix / (imgX * imgY))

    time = datetime.datetime.now()
    stringTime = time.strftime("%m-%d %H:%M")
    
    if(empPix / (imgX * imgY) > thresh):
        img.save("EmpacherTestImagesResults/" + subID + "::" + str(round(empPix / (imgX * imgY) , 4)) + ".png")
        #ogImg.save("EmpacherImagesUnmarked/" + subID + "::" + str(empPix / (imgX * imgY)) + ".png")
        #EmpacherImagesUnmarked

    return (empPix / (imgX * imgY) > thresh)
    



searchSubreddit()
