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


def search(subName , searchTerms):
    for submission in reddit.subreddit(subName).new(limit=10):
        for term in searchTerms:
            if(term in submission.title):
                notify("CAM_BOT", term + "mentioned in " + subName)


subName = "marist"
searchTerms = ["rowing" , "crew" , "covid"]

while (True):
    search(subName , searchTerms)
    time.sleep(60)
