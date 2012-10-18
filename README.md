Bulletin
========

Bulletin is a communication platform aimed at small companies and groups. Check out the wiki for more information. 

Bulletin is being developed by 
- Caylan Lee  
- Yoong Woo Kim  
- Andrew Davies  
- Ivan Darmansyah  
- Peter Weisbeck  
- Brian Oliphant  
- Kyle Boone  

*When this project is done, Caylan is getting everyone on the team a beer*

## Directories

* /bulletin_project - project settings
* /bulletin - app directory
* /prototype - app prototype directory
* /templates - template files
* /static_resources - anything that python doesn't dynamically generate, e.g. css, js, img
  * when server is ran, you can find these files at /static/

## Virtual environment setup
*Pretty much how Heroku says to do it. PLEASE edit this, anybody*

Project settings are currently setup for running on Heroku. In order to run locally on your machine, 
you may need to comment out the two lines at the bottom of the settings file for dj_database_url, 
and change where static files are loaded

cd Bulletin

virtualenv PYENV --distribute

source PYENV/bin/activate

pip install django psycopg2 dj-database-url

pip freeze > requirements.txt
