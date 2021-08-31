# wei-o-wei-calendar

## install
1. start a new django-project
2. clone wei-o-wei-calendar repostitory
3. add the config/kalender to your project
4. add kalender to your settings.py
5. add kalender.urls to your project urls.py
6. if your **project-name is not "config"** 
    * go to config/kalender/kalender_config.py and change the import (line 1) according to your projects name. 
    * Scroll down to "Tests" and change "url", "url_admin" and "path" according to your settings. 
    * Those are only needed to run the selenium-test. If you don't want to run test_selenium.py, you may delete the section and also the import in line 1.
7. python manage.py makemigrations
8. python manage.py migrate