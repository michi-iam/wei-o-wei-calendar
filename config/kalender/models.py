import datetime
from datetime import timedelta


from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


from . import kalender_config as CONF


class Event(models.Model):
    class Meta:
        verbose_name ='Event'
        verbose_name_plural = 'Events'
        ordering: ["start_date"]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)
    start_date = models.DateField(default=now)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    class Meta:
        permissions = [
            ("edit_events", "edit events"),
            ("add_events", "add events"),
        ]
    def __str__(self):
        return F'{ self.start_date.day } { self.title }'
    def set_last_updated(self):
        try:
            self.last_updated = now
            self.save()
            return True
        except:
            return False



CATEGORY_CHOICES = [
    ("BD", CONF.Models.Choices.Category.BD),
    ("DR", CONF.Models.Choices.Category.DR),
    ("ANI", CONF.Models.Choices.Category.ANI),
    ("WED", CONF.Models.Choices.Category.WED),
    ("PRTY", CONF.Models.Choices.Category.PRTY),
    ("GOV", CONF.Models.Choices.Category.GOV)
]
STATUS_CHOICES = [
    ("OPN", CONF.Models.Choices.Status.OPN),
    ("PRVT", CONF.Models.Choices.Status.PRVT),
    ("FRNDS", CONF.Models.Choices.Status.FRNDS),
]
class EventExtras(models.Model):
    class Meta:
        verbose_name = 'EventExtra'
        verbose_name_plural = 'EventExtras'
    event = models.OneToOneField(Event, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="OPN", blank=True)
    def __str__(self):
        return F'{ self.event }'
    
