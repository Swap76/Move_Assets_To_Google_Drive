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

client = MongoClient('mongodb://localhost:27017/') # URL of MongoDB Database
db = client['prod'] # Database Name 
episodes = db.episodes # Collection from the Database

# This function uploads file to google drive
# Arguments:- filename, filepath, filetype
def uploadFile(filename,filepath,mimetype):
    # In parent put ID of Folder in which files to be uploaded please give appropriate permisssions to the folder if you want to access the files without login give public access to the folder
    file_metadata = {'name': filename, "parents": ["1UFXxiR1vXMfMXG-8IfV7Xo7zT_DjpJzF"]}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='webContentLink').execute()
    # Returns a link for the the file
    return file.get('webContentLink') 

print('Starting Upload')

# Keeps track of the count
count = 0

# For tracking the upload of files we have added a new field in mongodb object called uploaded this tells us about the status of upload
for data in episodes.find({"uploded": False}, {"poster": 1}):
    link=data["poster"]
    newLink = ''
    count=count+1
    print(count)
    if count%200 == 0: # This ensures files don't pile up in our system by deleting the whole folder and creating it again
        shutil.rmtree('temp') 
        os.mkdir('temp')
    try:
        file_name=sid.generate() # This generates unique filenames
        urllib.request.urlretrieve(link, 'temp/'+file_name+'.jpg') # Downloades the image
        link = uploadFile(file_name+'.jpg','temp/'+file_name+'.jpg','image/jpeg') # Uploads the image
        newLink=link.replace('download','view',1) # Make the link viewable 
        print(newLink) # Print the link
        # Update the MongoDB object with new link
        update = episodes.update_one({"_id": data["_id"]},{"$set": {"poster": newLink, "uploded": True}})
    except:
        print(link) # Print link in which error occured
        # Update the MongoDB with uploaded true if you want to skip this link else make it false
        update = episodes.update_one({"_id": data["_id"]},{"$set": {"uploded": True}})
        continue

print("All Done")