from __future__ import print_function
import httplib2
import os, io
import urllib.request
import shutil
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
from shortid import ShortId
sid = ShortId()
from pymongo import MongoClient
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

client = MongoClient('mongodb://localhost:27017/')
db = client['friskyprod']
episodes = db.episodes

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename, "parents": ["1UFXxiR1vXMfMXG-8IhV7Xo7zT_DjpJzF"]}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='webContentLink').execute()
    return file.get('webContentLink')

print('Starting Upload')

count = 0

for data in episodes.find({"uploded": False}, {"poster": 1}):
    link=data["poster"]
    newLink = ''
    count=count+1
    print(count)
    if count%200 == 0: 
        shutil.rmtree('temp') 
        os.mkdir('temp')
    try:
        file_name=sid.generate()
        urllib.request.urlretrieve(link, 'temp/'+file_name+'.jpg')
        link = uploadFile(file_name+'.jpg','temp/'+file_name+'.jpg','image/jpeg')
        newLink=link.replace('download','view',1)
        print(newLink)
        update = episodes.update_one({"_id": data["_id"]},{"$set": {"poster": newLink, "uploded": True}})
    except:
        print(link)
        update = episodes.update_one({"_id": data["_id"]},{"$set": {"uploded": True}})
        continue

print("All Done")