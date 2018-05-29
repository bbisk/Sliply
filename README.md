# Sliply
Scan receipts and control your expenses. Django, PostgreSQL, Celery, Redis, Google Vision API, OAuth

TODO:

~~1. REST API~~ :heavy_check_mark 

~~2. Deploy MVP on Digital Ocean~~ :heavy_check_mark: http://thrifter.pl/

3. Add more functionalities

![alt text](https://raw.githubusercontent.com/tallpol3/Sliply/master/media/screenshot.png)


Instalation
1. Download or clone repository
2. Create a virtual enviroment for the app (Open terminal in the project folder and us a comand: virtualenv venv)
3. Activate the venv with command: . venv/bin/activate
4. Install all required packages with: pip install -r requirements.txt
5. Create a database and fill in .env file with settings in the root directory. Remember to add Facebook credentials (if applicable).
6. Use ./manage.py migrate to migrate database.
7. Add Google API credentials to your enviroment variabiles or fill in credit.sh
8. Make sure you have Redis server installed and up and running
9. Run Celery worker and Django runsslserver (or runserver if no Facebook authentication will be used) or use run.sh 
10. Run tests: ./manage.py test
11. Sample receipts can be found in sliply/test_image

Slides in Polish: https://docs.google.com/presentation/d/17U9NjcWHSSF8_KBE3UxH-vBhG57a6gTKTdGNwQYw4W0/edit?usp=sharing
