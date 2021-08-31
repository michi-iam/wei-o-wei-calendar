from django.urls import path

from . import views

app_name = 'kalender'
urlpatterns = [
    #Kalender
    path('', views.KalenderView.index, name='index'),
    path(r'rindex', views.KalenderView.index, name="rindex"),
    path(r'rforbidden/<str:msg>', views.KalenderView.rforbidden, name="rforbidden"),

    
        #Ajax
    path('get_prev_next_month', views.Kalender.get_prev_next_month, name='get_prev_next_month'),
    #Events
    path('event/<int:event_id>/', views.EventView.detail, name='detail'),
    path('get_show_or_edit_form', views.KalenderView.get_show_or_edit_form, name='get_show_or_edit_form'),
    path('post_event', views.KalenderView.post_event, name='post_event'),
    path('delete_event', views.KalenderView.delete_event, name='delete_event'),


]

    #<li><a href="{% url 'kalender:detail' question.id %}">{{ question.question_text }}</a></li>