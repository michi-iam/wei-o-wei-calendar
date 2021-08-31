# wei-o-wei-calendar

start a new django-project
clone wei-o-wei-calendar repostitory
add the config/kalender to your project
add kalender to your settings.py
add kalender.urls to your project urls.py
if project-name is not "config", go to config/kalender/kalender_config.py and change the import (line 1) according to your projects name. Also scroll down to "Tests" and change "url", "url_admin" and "path" according to your settings. Those are only needed to run the selenium-test. If you don't want to run test_selenium.py, you may delete the section and also the import in line 1.
python manage.py makemigrations
python manage.py migrate