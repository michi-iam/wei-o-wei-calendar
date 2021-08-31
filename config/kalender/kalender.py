from calendar import *
from itertools import groupby
import datetime
from datetime import datetime as dtime, date, time, timedelta


from django.db.models import Q


from .models import Event, EventExtras

def date_in_range(current_date, end_date):
    inrange = current_date <= end_date
    return inrange

class EventCalendar(HTMLCalendar):
    def __init__(self):
        super(EventCalendar, self).__init__()

    def formatmonth(self, username, theyear, themonth, withyear=True):
        """
        Input: year, month, username
            { username } -> show (private) events  
                                formatmonth(self, request.user.username) 
        
            -> Get events (month, year)
        """
        the_current_date = dtime(theyear, themonth, 1).date()
        events = Event.objects.all()
        Liste = []
        for e in events:
            if e.end_date:
                in_range = date_in_range(the_current_date, e.end_date)
                if in_range:
                    Liste.append(e)
            else:
                if e.start_date.month == themonth and e.start_date.year == theyear:
                    Liste.append(e)
        events= Liste
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s table">' % ( # +class:table
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
  
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events, username, theyear, themonth))
            a('\n')
     
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatweek(self, theweek, events, username, theyear, themonth):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events, username, theyear, themonth) for (d, wd) in theweek) # pass events -> formatday
        return '<tr>%s</tr>' % s 

    def formatday(self, day, weekday, events, username, theyear, themonth):
        """
        Return a day as a table cell.

        Input:  Events matching year+month
                username to get private events
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            """
            each_ev_html = html for each event/day
            """
            date = str(day) + "." + str(themonth) + "." + str(theyear)
            each_ev_html =""
            for e in events:#.order_by("start_date"):
                show = False
                if e.end_date != None: # event = from day a to day b        
                    dT = datetime.datetime.strptime(date, "%d.%m.%Y").date()         
                    if e.start_date <= dT <= e.end_date: # check if day = event 
                        if hasattr(e, "eventextras"):
                            if e.eventextras.status == "OPN" or EventExtras.status == "" or EventExtras.status == None: 
                                show = True # public event 
                            else:
                                if e.eventextras.status == "PRVT":
                                    if e.user:
                                        if e.user.username == username:
                                            show = True # event.username = request.username (views.get_username_year_and_month())
                                else:
                                    if e.eventextras.status == "FRNDS": # Kalender-User Freunde einrichten TODO Myinfo
                                        if username in return_names.Benutzer.superuser:
                                            show = True
                        else:
                            show=True # no eventextra = no status = public

                else: # event = day a - no end_date
                    if e.start_date.day == day:
                        if hasattr(e, "eventextras"):
                            if e.eventextras.status == "OPN" or e.eventextras.status == "" or e.eventextras.status == None:
                                show = True
                            else:
                                if e.eventextras.status == "PRVT":
                                    if e.user:
                                        if e.user.username == username:
                                            show = True
                                else:
                                    if e.eventextras.status == "FRNDS": # TODO add friends
                                        if username in return_names.Benutzer.superuser:
                                            show = True
                        else:
                            show=True
                if show == True:   
                    each_ev_html += F'<div><button><a class="myKalEditEventBtn" option="show" '
                    each_ev_html += F'eventid = "{ e.id }" >'
                    each_ev_html += F'{ e.title }</a></button></div>'
             
                      
            retString = F'<td class="{ self.cssclasses[weekday] }">' 
            retString += F'<button class="myKalShowFormBtn" option="show" date="{ date }">' # --> kalender.js + views    
            retString += F'<span>{ day }</span>'        
            retString += F'</button>'        
            retString += F'<div>{ each_ev_html }</div>' # all events that day       
            retString += F'</td>'      
            return retString
