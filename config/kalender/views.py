from calendar import *
import datetime


from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django_ajax.decorators import ajax
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.utils.html import format_html


from . import kalender_config as CONF
from . models import Event, EventExtras
from . forms import EventForm, EventExtrasForm
from . kalender import EventCalendar as Rememberry


templates = CONF.templates
now = datetime.datetime.now()

class KalenderView(View):
    def index(request):
        uym = Helper.get_username_year_and_month(request, now.year, now.month, "now") # get calendar as context - start_date = now
        kal = Kalender.get_calendar(uym) # 
        context = Helper.get_context(kal, uym) # 
        return render(request, templates["index"], context)
    
    def rforbidden(request, msg): # show error-msg
        """
        redirect if not authenticated / no permission ...
        """
        return render(request, templates["forbidden"], {"msg": msg})
    
    @ajax
    def get_show_or_edit_form(request):
        """
        (kalender.js)
        2 ajax options: show/edit +/- event_id
            show + event_id --> show existing event (no form)
            show w/o event_id --> empty form to add new event 
            
            edit + event_id --> form: instance=existing event; to update / delete event
        """
        context = {}
        if request.method == "GET":
            option = request.GET.get("option")
            if option=="show": # show existing event - w/o form (only show, not edit)
                eId = request.GET.get("event_id")
                if eId != None and eId != "" and eId != "None": 
                    see = KalenderView.Getter.show_existing_event(context, eId) 
                    return render(request, see[0], see[1])
                else: # no event_id -> get empty form to add new event
                    date = request.GET.get("date")
                    if date != "" and date != None:
                        see = KalenderView.Getter.get_empty_form(request, context, date) 
                    return render(request,see[0] ,see[1])
            elif option == "edit": # get event as form to update event
                eId = request.GET.get("event_id")
                see = KalenderView.Getter.get_event_as_form(request, context, eId) 
                return render(request, see[0], see[1])

    def post_event(request): # update or create new event
        """
        No event_id --> create new event
        event_id    --> update event 
        """
        if request.method == "POST":
            eId = request.POST.get("event_id")
            eventArray = EventForm.create_or_update_event(request, eId) # Create or update - eId = None = create
            if not eventArray[0] == True:# event created/updated False/True
                return redirect(reverse("kalender:rforbidden",kwargs={"msg":eventArray[1]}))  
            return redirect(reverse("kalender:rindex"))

    def delete_event(request):
        if request.method == "POST":
            eId = request.POST.get("event_id")
            deleted = EventForm.delete_event(request, eId) # delete event if event.user = None or event.user == request.user
            if deleted[0] == True:
                return redirect(reverse("kalender:rindex"))
            elif deleted[0] == False:  
                return redirect(reverse("kalender:rforbidden",kwargs={"msg":deleted[1]}))  
    
    class Getter():
        """
        Show event-details / Get forms 
        """
        def show_existing_event(context, event_id):
            """
            show event (not as form)
            """
            ev = Event.objects.get(pk=event_id)
            context["event"] = ev
            if hasattr(ev, "EventExtras"):
                evEx = EventExtras.objects.get(event=ev)
                context["eventextra"] = evEx
                context["event"] = ev
            context["event_id"] = ev.id
            template = templates["show_event"]
            return [template, context]
        
        def get_empty_form(request, context, date):
            """ 
            empty form to add new event
            """
            d = datetime.datetime.strptime(date, "%d.%m.%Y").date()
            eventForm = EventForm(initial={"start_date": d})
            context["eventform"] = eventForm
            eventExtrasForm = EventExtrasForm(request=request)
            context["eventextraform"] = eventExtrasForm
            template = templates["add_or_edit_event"]
            return [template, context]
        
        def get_event_as_form(request, context, event_id):
            """
            existing event as form to update event
            """
            event = Event.objects.get(pk=event_id)
            eventForm = EventForm(instance=event)
            context["eventform"] = eventForm
            if hasattr(event, "eventextras"):
                eventextra = EventExtras.objects.get(event=event)
                eventExtrasForm = EventExtrasForm(request=request, instance=eventextra)
                context["eventextraform"] = eventExtrasForm
            template = templates["add_or_edit_event"]
            context["event_id"] = event.id
            return [template, context]

#TODO: unnötig, löschen
class EventView(View):
    def detail(request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        return render(request, templates["detail"], {'event': event})
    

class Kalender():
    kalender_today = Rememberry().formatmonth(username=None, theyear=2021, themonth=7) # löschen TODO 
    directions = ["prev", "now", "next"]  #keys in ajax: get next month ...

    def get_calendar(username_year_month):
        uym = username_year_month 
        username = uym["username"]
        year = int(uym["year"])
        month = int(uym["month"])
        kalender = Rememberry().formatmonth( # get the calendar - username = get private dates
            username=username,
            theyear=year,
            themonth=month,
            withyear=True
        )
        return format_html(kalender) # TODO: best practice??

    @ajax  # ajax input = current(!) month
    def get_prev_next_month(request):
        if request.method == "GET":
            # get values 
            year = request.GET.get("year")
            month = request.GET.get("month")
            direction = request.GET.get("direction")
            # Check direction 
            uym = Helper.get_username_year_and_month(request, year, month, direction) # User? Month? Year?
            kalender = Kalender.get_calendar(uym)
            context = Helper.get_context(kalender, uym)  # get calendar as context
            response = render(request, templates["kalender"], context)
            return response

    

class Helper():
    def get_username_year_and_month(request, year, month, direction):
        """
        input = current(!) month
        filter input
        get username
        check direction 
        """
        if direction not in Kalender.directions:
            return redirect(reverse("kalender:rforbidden",kwargs={"msg":"Da läuft was gewaltig falsch!"}))  
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = None
        if str(direction) == "prev":
            if month == str(1):
                year = int(year) -1
                month = 12
            else:
                month = int(month) -1
        elif str(direction) == "now":
            now = datetime.datetime.now()
            year = now.year
            month = now.month
        elif str(direction) == "next":
            if month == str(12):
                year = int(year) + 1
                month = 1
            else:
                month = int(month) + 1
        username_year_month = {
            "username": username,
            "year": year,
            "month": month
        }
        return username_year_month
    
    def get_context(kalender, username_year_month):
            uym = username_year_month
            context = {
            "calendar":kalender,
            "username": uym["username"],
            "year": uym["year"],
            "month": uym["month"],
        }
            return context

