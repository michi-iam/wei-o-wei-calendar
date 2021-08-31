import datetime


from django import forms
from django.utils import timezone
from django.forms import fields
from django.db.models.fields import files
from django.contrib.admin import widgets  
from django.contrib.auth.models import User


from .models import *
from . import kalender_config as CONF

class EventForm(forms.ModelForm):
    start_date = fields.DateField(label=CONF.Labels.event_start_date, required=True, widget=forms.widgets.TextInput(attrs={'type': 'date'}))
    start_time = fields.TimeField(label=CONF.Labels.event_start_time,required=False, widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    end_date = fields.DateField(label=CONF.Labels.event_end_date,required=False, widget=forms.widgets.TextInput(attrs={'type': 'date'}))
    end_time = fields.TimeField(label=CONF.Labels.event_end_time,required=False, widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = Event
        exclude = ("user", "last_updated")

    def __init__(self, *args, **kwargs):
        # Form Control
        super(EventForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
        })
        self.fields['title'].label = CONF.Labels.event_title
        self.fields['description'].label = CONF.Labels.event_description
        self.fields['start_time'].initial = CONF.Initials.start_time
        self.fields['start_date'].initial = datetime.date.today()
    
    def create_or_update_event(request, event_id):
        """
        No event_id --> create new event
        event_id    --> update event 
        """
        if "<script>" in str(request.POST):
            return [False, "kein JS!"] # TODO: Function to check user-input
        if not request.user.is_authenticated and CONF.Settings.must_auth_to_post:
            return [False, CONF.ErrorMessage.must_auth_to_post]
        eId = event_id
        if eId == None or eId == "None" or eId == "": # create new event
            eForm = EventForm(request.POST)
            if eForm.is_valid():
                event = eForm.save(commit=False)
                if request.user.is_authenticated:
                    event.user = request.user
                event.save()
                eExForm = EventExtrasForm(request, request.POST)
                if eExForm.is_valid():
                    category = eExForm.cleaned_data['category']
                    if request.user.is_authenticated:
                        status = eExForm.cleaned_data['status']
                        eventExtra=EventExtras.objects.create(
                            event=event,
                            category=category,
                            status=status
                        )
                    else:
                        eventExtra=EventExtras.objects.create(
                            event=event,
                            category=category,
                        )      
                    # new event created
                else:
                    pass
            else:
                pass
        else:
            event = Event.objects.get(pk=eId) #update event
            if event.user != None and event.user != request.user and CONF.Settings.update_same_user_only:
                return [False, CONF.ErrorMessage.update_same_user_only]
            eventform = EventForm(request.POST, instance=event)
            if eventform.is_valid():
                if hasattr(event, "eventextras"):
                    eventextra = EventExtras.objects.get(event=event)
                    eventextraform = EventExtrasForm(request, request.POST, instance=eventextra)
                    if eventextraform.is_valid():
                        event = eventform.save(commit=False)
                        if request.user.is_authenticated:
                            event.user = request.user
                        else:
                            event.user = None
                        event.save()
                        eventextraform.save()
              
                    else:
                        CONF.HandleErrors.form_error(eventextraform.errors)
        return [True, event]


    def delete_event(request, event_id):
        deleted = False
        if request.user.is_authenticated:
            eId = event_id
            ev = Event.objects.get(pk=eId)
            if ev.user == None:
                ev.delete()
                deleted = True
            else:
                if ev.user == request.user:
                    ev.delete()
                    deleted = True
            if deleted:
                msg = CONF.Message.event_deleted
            else:
                msg = CONF.ErrorMessage.requser_not_evuser
        else:
            msg = CONF.ErrorMessage.must_login_to_delete
        return [deleted, msg]


class EventExtrasForm(forms.ModelForm):
    class Meta:
        model = EventExtras
        fields = ("category","status",) # no status if not user.auth
    def __init__(self, request, *args, **kwargs):
        super(EventExtrasForm, self).__init__(*args, **kwargs)
        if request.user.is_authenticated == False:
            self.fields.pop("status")
        elif request.user.is_authenticated == True:
            self.fields['status'].label = CONF.Labels.status
        self.fields['category'].label = CONF.Labels.category

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        