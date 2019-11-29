# Move_Assets_To_Google_Drive
Using this repo a beginner will be able move assets from databases or file systems onto Google Drive 

## Getting started with the project

* Fork the repository on GitHub.

* Navigate to the folder of the repository.

* To run this project, you should have python3 and pip installed on your system.
If you don't have python3 and pip, you can visit [The official site of python3](https://www.python.org/download/releases/3.0/)
to install them on your system.

* Install python3 dependencies.  
  ```
  pip install -r requirement.txt
  ```

* Enable Google Drive API for your account and obtain credentials for the same. Please follow the [Codelab](https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#9) for all this

* Now run following command for generating token for our python app to use use Google Drive API.
    ```
    python3 GoogleDriveSetup.py
    ```
    This command will create a token.pickle file in the root directory