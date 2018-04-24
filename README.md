# Sliply
Scan receipts and control your expenses. Django, PostgreSQL, Celery, Redis, Google Vision API, OAuth

TODO:
1. REST API (work in progress)
2. Deploy MVP on Digital Ocean
3. Add more functionalities

Instalation
1. Download or clone repository
2. Create a virtual enviroment for the app (Open terminal in the project folder and us a comand: virtualenv venv)
3. Activate the venv with command: . venv/bin/activate
4. Install all required packages with: pip install -r requirements.txt
5. Create .env file with settings in the root directory. Remember to add Facebook credentials (if applicable).
6. Add Google API credentials to your enviroment variabiles or fill in credit.sh
7. Make sure you have Redis server installed and up and running
8. Run Celery worker and Django runsslserver (or runserver if no Facebook authentication will be used) or use run.sh 
