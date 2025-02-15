from django.urls import path
from ..views.note_views import note_view

urlpatterns=[
    path('note',note_view.get_note,name='get_note'),
    path('noteid',note_view.get_noteid,name='get_noteid'),
    path('note/create',note_view.create_note,name='create_note'),
    path('note/update/<int:pk>',note_view.update_note,name='update_note'),
    path('note/delete/<int:pk>',note_view.delete_note,name='delete_note'),

]