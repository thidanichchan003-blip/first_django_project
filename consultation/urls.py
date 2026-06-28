from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.consultation_list,
        name='consultation_list'
    ),

    path(
        'create/',
        views.consultation_create,
        name='consultation_create'
    ),

    path(
    'chat/<int:consultation_id>/',
    views.consultation_chat,
    name='consultation_chat'
),
]