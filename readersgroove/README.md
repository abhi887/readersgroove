# Project 1

Web Programming with Python and JavaScript



1.Project1 consists of the book review website using flask by name 'Readers Groove'.

2.The project contains total of 8 webpages or html documents located under folder templates.

3.The project contains total 7 stylesheet documents or css files located under folder static.

4.Import.py file is a python application that is used to import the data into database using the books.csv file provided.

5.app.py is the python flask application that handles complete working of the website once the database is setup.

6.login.html is the login page of the website that requires the email and password of already registered member to access other features of the site.

7.signup.html is the signup\registration page of the website that requires the users firstname,lastname,email,sex and password to get registered on the website and login in future sessions.

8.relogin.html and resignup.html are the webpages fetched if the user submitts an empty form or wrong credentials in case of login page.

9.app.py uses the flask micro-framework, it has several routes for the websites funtionality.

10.specifically the app.py consists of '/' i.e root ,signup,ssignup,login,slogin,search and book routes and it's respective funtions.

11.'/' or root route fetches the login page as default root homepage.

12.All the other routes take care of the funtions such as login,signup,book quering using book name,isbn number and author name, getting details of the book from the goodreads api, and users review submission etc.