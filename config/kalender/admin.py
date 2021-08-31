from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


from . models import Event, EventExtras


def linkify(field_name, short_desc):
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = short_desc  
    return _linkify


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('last_updated',)
    list_display = ['title', 'user','start_date','end_date', linkify(field_name="eventextras", short_desc="zu den Extras")]
    list_filter = ['start_date']
    search_fields = ['title']
    

class EventExtrasAdmin(admin.ModelAdmin):
    list_display = ('event','category', 'status', linkify(field_name="event", short_desc="zum Event")) #image_tag -> def in Models
    list_filter = ['event__start_date']
    search_fields = ['event__title']


admin.site.register(Event, EventAdmin)
admin.site.register(EventExtras, EventExtrasAdmin)
