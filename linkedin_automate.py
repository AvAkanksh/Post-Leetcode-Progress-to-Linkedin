import requests
import os
import json
import datetime

class LinkedAutomate:
    def __init__(self,accessToken,postTitle,postDescription):
        self.accessToken = accessToken
        self.postTitle = postTitle
        self.postDescription = postDescription
        self.headers = {
            'Authorization' : f'Bearer {self.accessToken}'
        }
        self.today = datetime.date.today().strftime("%d/%m/%Y")
        self.uploadUrl = None
        self.asset = None

    def getUserId(self):
        url = 'https://api.linkedin.com/v2/userinfo'
        response = requests.get(url,headers=self.headers)
        # print(json.loads(response.text))
        self.userId = json.loads(response.text)['sub']
    

    def payloadTemplate(self):
        payload = {
            "author": f"urn:li:person:{self.userId}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": self.postDescription
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": f'{self.postTitle}\n {self.postDescription}'
                            },
                            "title": {
                                "text": self.postTitle
                            },
                            "media": self.asset
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        return json.dumps(payload)

    def postToFeed(self):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self.payloadTemplate()
        return requests.post(url, headers=self.headers, data=payload)
    
    def registerImageOrVideo(self):
        url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        data = {
            "registerUploadRequest": {
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "owner": f"urn:li:person:{self.userId}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        response =  requests.post(url, headers=self.headers, data=json.dumps(data))
        self.uploadUrl = json.loads(response.text)['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        self.asset = json.loads(response.text)['value']['asset']

    def uploadImage(self):
        response = requests.post(self.uploadUrl, headers=self.headers,files={'file': open('LeetCode_Sharing.png', 'rb')})

    def main(self):
        self.getUserId()
        self.registerImageOrVideo()
        self.uploadImage()
        postToFeedresponse = self.postToFeed() 


if __name__ == '__main__':
    postTitle = 'LeetCode Daily Problem'
    today = datetime.date.today().strftime("%d/%m/%Y")
    postDescription = f'Solved LeetCode Daily Problem on {today}'
    accessToken = os.environ['accessTokenLinkedin']
    linkedAutomate = LinkedAutomate(accessToken,postTitle,postDescription)
    linkedAutomate.main()    




