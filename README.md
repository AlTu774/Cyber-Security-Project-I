# Cyber-Security-Project-I
A simple blog app for the Cyber Security Project course.

# Instructions
The app uses Django, and if it's not installed, it can be installed in a venv environment, which is initialized with
```
python3 -m venv .venv
```

and started with
```
source .venv/bin/activate
```

after which you can install the Django framework within the environment with
```
python -m pip install Django
```

you can then start the server by moving into the website directory and running command
```
python manage.py runserver
```
this will start a server on localhost, such as on address http://127.0.0.1:8000/, and the blog app will be found at http://127.0.0.1:8000/blog/

# Errors
On newer Django versions the unsalted MD5 hasher has been removed as well as SHA1 password hasher, so to get the app to work properly one can just remove the "PASSWORD_HASHERS" list in the settings.py file or use an older version of Django.
