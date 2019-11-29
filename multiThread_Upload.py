from __future__ import print_function
import multiprocessing 
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

# This function fetches records from MongoDB and Performs the diffrent operations
# Arguments:- folderName, number
# In this case of Multithreading we want processes to work in isolated environments because of that we are passing folder or the thread 
# Also a number argument which will ensure that every thread works on diffrent MongoDB objects
def ProcessUpload(folderName,number):
    # Every Process has given a seprate connection to MongoDB
    client = MongoClient('mongodb://localhost:27017/') # URL of MongoDB Database
    db = client['prod'] # Database Name 
    episodes = db.episodes # Collection from the Database
    # Keeps track of the count
    count = 0
    for x in range(5000): # This range can very depending on your threads and dataset
        for data in episodes.find({"uploded": False}, {"poster": 1}).skip(number).limit(2):
            link=data["poster"]
            newLink = ''
            count=count+1
            print(data["_id"])
            print(count)
            if count%200 == 0: # This ensures files don't pile up in our system by deleting the whole folder and creating it again
                shutil.rmtree(folderName) 
                os.mkdir(folderName)
            try:
                file_name=sid.generate() # This generates unique filenames
                urllib.request.urlretrieve(link, folderName+'/'+file_name+'.jpg') # Downloades the image
                link = uploadFile(file_name+'.jpg', folderName+'/'+file_name+'.jpg','image/jpeg') # Uploads the image
                newLink=link.replace('download','view',1) # Make the link viewable 
                print(newLink) # Print the link
                # Update the MongoDB object with new link
                update = episodes.update_one({"_id": data["_id"]},{"$set": {"poster": newLink, "uploded": True}})
            except:
                print(link) # Print link in which error occured
                # Update the MongoDB with uploaded true if you want to skip this link else make it false
                update = episodes.update_one({"_id": data["_id"]},{"$set": {"uploded": True}})
                continue

print('Starting Upload')

# Please find out how many threads your CPU has then start that many processes only

# Call multiprocessing functions 
p1 = multiprocessing.Process(target=ProcessUpload, args=('temp1',0, )) 
p2 = multiprocessing.Process(target=ProcessUpload, args=('temp2',100, )) 
p3 = multiprocessing.Process(target=ProcessUpload, args=('temp3',200, )) 
p4 = multiprocessing.Process(target=ProcessUpload, args=('temp4',300, )) 
p5 = multiprocessing.Process(target=ProcessUpload, args=('temp5',400, )) 
p6 = multiprocessing.Process(target=ProcessUpload, args=('temp6',500, )) 
p7 = multiprocessing.Process(target=ProcessUpload, args=('temp7',600, )) 
p8 = multiprocessing.Process(target=ProcessUpload, args=('temp8',700, )) 

# starting processes 
p1.start() 
p2.start() 
p3.start() 
p4.start()
p5.start() 
p6.start() 
p7.start() 
p8.start()

# wait until processes are finished 
p1.join() 
p2.join() 
p3.join() 
p4.join()
p5.join() 
p6.join() 
p7.join() 
p8.join()

# All processes finished 
print("All Done")