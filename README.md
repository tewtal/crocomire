# crocomire
Speedrunning Strategy Database

Requires the following Flask addons to be installed:
  * Flask-SQLAlchemy
  * Flask-Login
  * Flask-Migrate
  * Flask-WTForms

Configuration settings needs to be set in the "crocomire/settings.py" file.
If using WSGI then edit "crocomire.wsgi" and set the correct path.

Database migrations are done using the "manage.py" script in the root directory of the app, for example:
```
python manage.py db migrate       - This will scan the app for database changes and create a migration file
python manage.py db upgrade       - This will store the changes to the database
```

The app can be run standalone by executing the "runserver.py" script in the root directory of the app.
