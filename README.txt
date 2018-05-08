Submission Made by Nagaarjun Nagarajan 
========================================

Requirements
************
1. Good connection to internet 
	- Uses an online Wikipedia website as a backend 
2. Flask-API library in Python
	- pip install flask
3. pywikibot library in Python 
	- pip install pywikibot
4. datetime 
	- pip install datetime
5. CURL to transfer and receive data from server
	- https://curl.haxx.se/download.html

Getting Started
****************
Simply, run the API.py using the command "python API.py" to get the rest API started. 
On a seperate command bash/prompt, 
	- To use the GET command:
		curl <url> -L
		
	- To use the POST command:
		curl -H "Content-Type: application/json" -X POST -d "{\"content\":\"<your-content>\"}" <URL>
		If it asks for password on the server window, the password is 123

Tips
****
When entering the timestamp, make sure it does not contain speech marks (an error will be thrown)
Make sure user-config.py stays in this folder. Otherwise, pywikibot will not work 

