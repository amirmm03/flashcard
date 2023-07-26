from django.urls import path

from flashcards import views

urlpatterns = [
    path("", views.ProgramListView.as_view(), name="index"),
    path("create-program/", views.create_program, name='create_program'),
    path("program/<int:program_pk>/", views.study_program, name='program'),
    path("program/<int:program_pk>/delete", views.delete_program, name='delete_program'),
    path("program/<int:program_pk>/create-flashcard", views.create_flashcard, {'is_edit': False}, name='create-flashcard'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>", views.flashcard, name='flashcard'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>/delete", views.delete_card, name='delete_card'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>/edit", views.create_flashcard, {'is_edit': True}, name='edit_card'),
]
