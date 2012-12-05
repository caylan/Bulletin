Bulletin 
========

Bulletin is a communication platform aimed at small companies and groups. Check out the [wiki](https://github.com/caylan/Bulletin/wiki) for more information, or see what we have running so far at http://www.bulletinapp.net!

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
*Pretty much how Heroku says to do it.* (for reference - https://devcenter.heroku.com/articles/django)

Project settings are currently setup for running on Heroku. In order to run locally on your machine, 
you may need to comment out the two lines at the bottom of the settings file for dj_database_url.

        cd Bulletin

        virtualenv PYENV --distribute

        source PYENV/bin/activate

At this point, the virtual environment has been activated.  As the project
continues to change, so too will the requirements, which must be stored in the
requirements.txt file in order for Heroku to know which apps to install.  To get
up to speed if there is already a requirements.txt folder, run:

        pip install -r requirements.txt

If not, then install some base programs, and then create the requirements.txt
file.

        pip install django psycopg2 dj-database-url   # for example.

After installing any new apps, always make sure to update the new requirements:

        pip freeze > requirements.txt
        
For testing from the root using nose

        ./manage.py test

