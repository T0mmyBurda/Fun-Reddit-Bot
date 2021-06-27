#This program will periodically check new posts of a subreddit then notify your desktop
#if any of the entered keywords are present in the post title

import praw
import os
import time

#creates reddit instance
creds = open("SecretStuff.txt", "r").read().split("\n")

try:
    reddit = praw.Reddit(client_id = creds[0] , client_secret = creds[1] , user_agent = creds[2])
except:
     print("Secret file configured incorrectly")


#notification code
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def searchNewImages(subName , searchTerms , last):

    newLast = ""
    firstLoop = True
    for submission in reddit.subreddit(subName).new(limit=10):
        if(firstLoop):
            newLast = submission
        if(submission == last):
            print("foundLast" , "   " , newLast)
            return newLast
        for term in searchTerms:
            if(term in submission.title.lower()):
                notify("CAM_BOT", term + " mentioned in " + subName)
        prev = submission
    last = submission

    return last


def isEmpacher():
    pass
    


subName = "marist"
searchTerms = ["rowing" , "crew" , "COVID"]
checkInterval = 60
last = ""

while (True):
    last = search(subName , searchTerms , last)
    print("LAST: " , last)
    time.sleep(checkInterval)
