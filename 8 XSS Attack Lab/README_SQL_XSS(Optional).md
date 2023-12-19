eRequirements: any machine with python/python3

General Info:

Webapplication is created using Flask web framework
Database used is sqlite3

install all the required libraries using this command

# pip install -r requirements.txt

start the webserver using this command

# python server.py

Exercise:

1. go to http://127.0.0.1/login why this is vulnerable and can implement a fix in the code.

2. go to http://127.0.0.1/img/4 can you construct a payload which can display information from other tables(Eg: users). can implement a fix in this code.

3. Try to explore various attack vectors to perform XSS in this application. Note: XSS can be run on client and it can also be stored in server side which makes it more vulnerable
