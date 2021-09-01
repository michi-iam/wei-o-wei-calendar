# wei-o-wei-calendar

## install
1. start a new django-project **or** add to an existing project
2. clone wei-o-wei-calendar repostitory
    * add the config/kalender to your project
    * add config/config/templates to your projects templates
    * add config/config/static/ to your projects static-dir 
    * add "kalender" to your settings.py
3. add "kalender.urls" to your project urls.py (path("yourpathname", include("kalender.urls")),)
4. Comment out in kalender/urls.py:
    * all paths
    * from . import views
5. python manage.py makemigrations
6. python manage.py migrate
7. **undo** Step 4
8. if your **project-name is not "config"** 
    * go to config/kalender/kalender_config.py and change the import (line 1) according to your projects name. 
    * Scroll down to "Tests" and change "url", "url_admin" and "path" according to your settings. 
    * Those are only needed to run the selenium-test. If you don't want to run test_selenium.py, you may delete the section and also the import in line 1.

9. python manage.py runserver