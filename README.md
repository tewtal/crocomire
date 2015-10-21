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
python manage.py db migrate 
python manage.py db upgrade
```
This will first look for changes to the database schema in the app and create a migration file, and the upgrade command will then commit the changes to the database.

When installing with a blank database, create a new database and set it up in settings.py, and then run
```
python manage.py db upgrade
```
This will create all the tables properly in the new database.

The app can be run standalone by executing the "runserver.py" script in the root directory of the app.
