import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


from django.test import TestCase


from . models import *
from . views import *
from . import kalender_config as CONF


class EventTestCase(TestCase):
    URL = CONF.URL.url
    URLADMIN = CONF.URL.url_admin
    PATH = CONF.Selenium.path  

    title = "New Event" 
    updated_title = " - updated event" 
    nr_add_btn = 1

    testuser_1 = CONF.Selenium.testuser_1
    testuser_2 = CONF.Selenium.testuser_2

    def test_form(self):
        """
        Test creates events in the actual database!
        Create event = only title, TODO: no category, status etc.
        """
        user_nr_add = 2
        user_nr_update = 2
        user_nr_delete = 2
        eventtitle= EventTestCase.title
        updatedtitle = EventTestCase.updated_title
        headless = True

        event_added = EventTestCase().add_event(eventtitle=eventtitle, headless=headless, usernr=user_nr_add)
        event_updated = EventTestCase().edit_event(eventtitle=eventtitle, headless=headless, updatedtitle=updatedtitle, usernr=user_nr_update)
        event_deleted = EventTestCase().delete_event(eventtitle=eventtitle+updatedtitle, headless=headless, usernr=user_nr_delete)
    #Create
        self.assertIs(event_added, True)
    #Edit
        if user_nr_add == 0:
            self.assertIs(event_updated, True)
        elif user_nr_add != 0 and user_nr_add != user_nr_update:
            self.assertIs(event_updated, False)
        elif user_nr_add != 0 and user_nr_add == user_nr_update:
            self.assertIs(event_updated, True)
    #Delete
        if user_nr_add == 0:
            self.assertIs(event_deleted, True)
        elif user_nr_add != 0 and user_nr_add != user_nr_delete:
            self.assertIs(event_deleted, False)
        elif user_nr_add != 0 and user_nr_add == user_nr_delete:
            self.assertIs(event_deleted, True)


    def add_event(self, eventtitle, headless, usernr=0):
        if usernr == 0:
            driver = EventTestCase.Helper.get_driver(self, headless)
        elif isinstance(usernr, int):
            driver = EventTestCase.Helper.login(self, headless, usernr)
            driver.get(EventTestCase.URL)
        
        btn_add = driver.find_elements_by_class_name("myKalShowFormBtn")
        btn_add[EventTestCase.nr_add_btn].send_keys(Keys.RETURN) 
        time.sleep(1)
        title = driver.find_element_by_id("id_title")
        title.send_keys(eventtitle)
        add_event_btn = driver.find_element_by_id("add_event_btn")
        add_event_btn.send_keys(Keys.RETURN)
        time.sleep(1)
        pageSource = driver.page_source
        if eventtitle in pageSource:
            event_added = True
        else:
            event_added = False
        driver.quit()
        return event_added



    def edit_event(self, eventtitle, headless, updatedtitle, usernr=0):
        if usernr == 0:
            driver = EventTestCase.Helper.get_driver(headless)
        elif isinstance(usernr, int):
            driver = EventTestCase.Helper.login(self, headless, usernr)
        
        driver.get(EventTestCase.URL)

        event = driver.find_element_by_link_text(eventtitle)
        event.click()
        time.sleep(1)
        btn_edit = driver.find_element_by_class_name("myKalEditEventBtn")
        btn_edit.click()
        time.sleep(1)
        title = driver.find_element_by_id("id_title")
        title.send_keys(updatedtitle)
        add_event_btn = driver.find_element_by_id("add_event_btn")
        add_event_btn.send_keys(Keys.RETURN)
        time.sleep(1)
        pageSource = driver.page_source
        if updatedtitle in pageSource:
            event_updated = True
        else:
            event_updated = False
        driver.quit()
        return event_updated

    def delete_event(self, headless, eventtitle, usernr=0):
        if usernr == 0:
            driver = EventTestCase.Helper.get_driver(self, headless)
        elif isinstance(usernr, int):
            driver = EventTestCase.Helper.login(self, headless, usernr)
        driver.get(EventTestCase.URL)
        event = driver.find_element_by_link_text(eventtitle)
        event.click()
        time.sleep(1)
        btn_edit = driver.find_element_by_class_name("myKalEditEventBtn")
        btn_edit.click()
        time.sleep(2)
        delete_btn = driver.find_element_by_id("delete_event_btn")
        delete_btn.send_keys(Keys.RETURN)
        time.sleep(2)
        pageSource = driver.page_source
        if eventtitle in pageSource:
            deleted = False
        else: 
            deleted = True
        driver.quit()
        return deleted
            



    class Helper():
            # open site + get driver
        def get_driver(self, headless): #klappt
            options = Options()
            options.headless = headless
            driver = webdriver.Chrome(executable_path=EventTestCase.PATH, options=options)
            driver.get(EventTestCase.URL)
            return driver

        def login(self, headless, testuser_nr):
            if testuser_nr == 1:
                username = EventTestCase.testuser_1["username"]
                password = EventTestCase.testuser_1["password"] 
            elif testuser_nr == 2:
                username = EventTestCase.testuser_2["username"]
                password = EventTestCase.testuser_2["password"] 

            driver = EventTestCase.Helper.get_driver(self, headless)
            driver.get(EventTestCase.URLADMIN)
            time.sleep(1)
            id_username = driver.find_element_by_id("id_username")
            id_password = driver.find_element_by_id("id_password")
            id_username.send_keys(username)
            id_password.send_keys(password)
            btn = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/div/form/div[3]/input")
            btn.send_keys(Keys.RETURN)
            time.sleep(1)
            pageSource = driver.page_source
            if "Website-Verwaltung" in pageSource:
                logged_in = True
            else:
                logged_in = False
            self.assertIs(logged_in, True)
            return driver 











































