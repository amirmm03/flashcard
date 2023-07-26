from django.urls import path

from flashcards import views

urlpatterns = [
    path("", views.ProgramListView.as_view(), name="index"),
    path("create-program/", views.ProgramCreateView.as_view(), name='create_program'),
    path("program/<int:program_pk>/", views.ProgramDetailView.as_view(), name='program'),
    path("program/<int:program_pk>/delete", views.delete_program, name='delete_program'),
    path("program/<int:program_pk>/create-flashcard", views.FlashcardCreateView.as_view(), name='create-flashcard'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>", views.CardDetailView.as_view(), name='flashcard'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>/delete", views.delete_card, name='delete_card'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>/edit", views.CardUpdateView.as_view(), name='edit_card'),
]
