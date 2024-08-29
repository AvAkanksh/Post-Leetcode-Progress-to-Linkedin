import requests
import os
import datetime
import time
import json
from linkedin_automate import LinkedAutomate

#Linkedin Credentials
LINKEDIN_USERNAME = os.environ['Linkedin_UID']
LINKEDIN_PASSWORD = os.environ['Linkedin_PWD']
ACCESSTOKEN = os.environ['accessTokenLinkedin']

#Leetcode Details
LEETCODE_USERNAME = os.environ['Leetcode_UID']
LIMIT = 25

TODAY = datetime.date.today().strftime("%d/%m/%Y")

# POST_TEMPLATE = post = f"""
# 🚀 LeetCode Progress Update: {today}

# I'm excited to share that I solved {today_solved} LeetCode problems today! 💻 

# #LeetCode #Python #Coding #Algorithm #DataStructures #Progress 
# """

# Function for getting the progress for the day in leetcode
def get_leetcode_progress(days=1):
    url = "https://leetcode.com/graphql/"

    payload = json.dumps({
    "query": "query recentAcSubmissions($username: String!, $limit: Int!) {recentAcSubmissionList(username: $username, limit: $limit){id title titleSlug timestamp}}",
    "variables": {
        "username": LEETCODE_USERNAME,
        "limit": LIMIT
    },
    "operationName": "recentAcSubmissions"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    recent_ac_list = json.loads(requests.post( url, headers=headers, data=payload).text)['data']['recentAcSubmissionList']
    SECONDS_IN_ONE_DAY = 86400*days
    YESTERDAY_EPOCH = int(time.time()) - SECONDS_IN_ONE_DAY
    todays_ac = []
    for i in recent_ac_list:
        if(int(i['timestamp']) > YESTERDAY_EPOCH):
            todays_ac.append(i)
        else:
            break
    return todays_ac

def getDescription():
    todays_ac = get_leetcode_progress()
    final_description = f'''
    I'm excited to share that I solved {len(todays_ac)} LeetCode problems today! 💻

'''
    print(todays_ac)
    for i in range(len(todays_ac)):
        final_description += f'{i+1}. [{todays_ac[i]["title"]}] - 🔗: (https://leetcode.com/problems/{todays_ac[i]["titleSlug"]}) \n'

    connectWithMe = f'''
Connect with me!

LeetCode: https://leetcode.com/u/avakanksh/
GitHub: https://github.com/AvAkanksh'''
    note = "NOTE : This is an AUTOMATED post made using Python and Linkedin Developer API."
    hashtags = "#LeetCode #Python #Coding #Algorithm #DataStructures #Progress #Linkedin #LinkedinDeveloperAPI #Automation" 
    final_description += f'{connectWithMe}\n{note}\n\n{hashtags}'
    return final_description

def post_on_linkedin():

    postTitle = f'💻 LeetCode progress update as on {TODAY}'
    postDescription = getDescription()
    linkedAutomate = LinkedAutomate(ACCESSTOKEN,postTitle,postDescription)
    linkedAutomate.main()

if __name__ == '__main__':
    post_on_linkedin()



