from config import settings #config = project-name, replace with your projects name


templates = {
    "index": 'kalender/index.html',
    "kalender": "kalender/kalender/kalender.html",
    "detail": 'kalender/events/detail.html',
    "show_event": 'kalender/kalender/show_event.html',
    "add_or_edit_event": 'kalender/kalender/add_or_edit_event.html',
    "forbidden": "kalender/kalender/kal_forbidden.html"
}


class Settings():
    must_auth_to_post = False
    update_same_user_only = True

class Labels():
    event_start_date = "Start (Datum)"
    event_start_time = "Start (Zeit)"
    event_end_date = "Ende (Datum)"
    event_end_time = "Ende (Zeit)"
    event_title = "Titel"
    event_description = "Notizen"
    status = "sichtbar?"
    category = "Kategorie"

class Initials():
    start_time = "12:00"

class Message():
    event_deleted = "gelöscht"

class ErrorMessage():
    must_auth_to_post = "not auth"
    update_same_user_only = "not ev user"
    requser_not_evuser = "RequUser not EvUser"
    must_login_to_delete = "must_login_to_delete"

class HandleErrors():
    def form_error(errors):
        print(errors) #TODO


class Models():
    class Choices(): # Names in model.CHOICES
        class Category():
            BD = "Geburtstag"
            DR = "Ärzt*innen-Termin"
            ANI = "Jahrestag"
            WED = "Hochzeit"
            PRTY = "Party"
            GOV = "Bürokratiegedöns"
        
        class Status():
            OPN = "öffentlich"
            PRVT = "privat"
            FRNDS = "Freunde"


# Tests 
class URL():
    url = settings.selenium_url # Kalender-Url
    url_admin = settings.selenium_url_admin # Admin site login 

class Selenium():
    path = settings.selenium_chromedriver_path 
    testuser_1 = {
        "username": "testuser",
        "password": "testpasswort"
    }
    
    testuser_2 = {
        "username": "testuser2",
        "password": "testpasswort2"
    }