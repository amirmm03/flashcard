from django.urls import path

from flashcards import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-set/", views.create_set, name='create_set'),
    path("set/<int:setpk>/", views.study_set, name='set'),
    path("set/<int:setpk>/delete", views.delete_set, name='delete_set'),
    path("set/<int:setpk>/create-flashcard", views.create_flashcard, {'is_edit': False}, name='create-flashcard'),
    path("set/<int:setpk>/flashcard/<int:cardpk>", views.flashcard, name='flashcard'),
    path("set/<int:setpk>/flashcard/<int:cardpk>/delete", views.delete_card, name='delete_card'),
    path("set/<int:setpk>/flashcard/<int:cardpk>/edit", views.create_flashcard, {'is_edit': True}, name='edit_card'),
]
