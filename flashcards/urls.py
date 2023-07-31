from django.urls import path, include
from rest_framework.routers import DefaultRouter

from flashcards import views

API_router = DefaultRouter()
API_router.register(r'cards', views.CardViewSet, basename="card")
API_router.register(r'groups', views.GroupViewSet, basename="group")

urlpatterns = [
    path("", views.ProgramListView.as_view(), name="index"),
    path("create-program/", views.ProgramCreateView.as_view(), name='create_program'),
    path("program/<int:program_pk>/", views.ProgramDetailView.as_view(), name='program'),
    path("program/<int:program_pk>/delete", views.ProgramDeleteView.as_view(), name='delete_program'),
    path("program/<int:program_pk>/create-flashcard", views.FlashcardCreateView.as_view(), name='create-flashcard'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>", views.CardDetailView.as_view(), name='flashcard'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>/delete", views.CardDeleteView.as_view(), name='delete_card'),
    path("program/<int:program_pk>/flashcard/<int:card_pk>/edit", views.CardUpdateView.as_view(), name='edit_card'),
    path("api/", include(API_router.urls))
]
