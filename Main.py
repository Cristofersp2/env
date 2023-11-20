import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import os

#credential's settings
creds = None

#json path
credentials_path = "/env/Json/credentials_path.json"

#load credentials
credentials = Credentials.from_service_account_file(credentials_path)

#specify the api´s scope
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

#build the api service
youtube = build("youtube", "v3", credentials=credentials, scopes=scopes)



#if the credentials are save and are updated, else just authentificate
if os.path.exists("token.pickle"):
    with open("open.token.pickle", "rb") as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, scopes)
        creeds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
            
    #build the youtube service
youtube = build("youtube", "v3", credentials=creds)

# Videos to upload's data
video_path = "video_path.mp4"
video_title ="Video title"
video_description = "Video description"
video_tags = ["tag1", "tag2"]
video_category_id = "22" # Video Category ID

#upload the video
media = MediaFileUpload

# Video resources

body = {
    "snippet": {
        "title": video_title,
        "description": video_description,
        "tags": video_tags,
        "categoryId": video_category_id
    },
    "status": {
        "privacystatus": "public"
     }
}

# sending token of the uploading
request = youtube.video().insert(
    part="snippet.status",
    body=body,
    media_body=media,
)
response = request.execute()

#print the ID video
print("The video has been uploaded correctly. Video ID: %s" % response["id"])
