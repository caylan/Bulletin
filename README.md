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
* /templates

## Virtual environment setup
*Pretty much how Heroku says to do it*
*PLEASE edit this, anybody*

cd Bulletin

virtualenv PYENV --distribute

source PYENV/bin/activate

pip install django psycopg2 dj-database-url

pip freeze > requirements.txt
