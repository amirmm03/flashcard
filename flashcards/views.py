from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework import viewsets

from flashcards.models import StudyProgram, FlashCard
from flashcards.serializers import StudyProgramSerializer, FlashCardSerializers


class ProgramListView(ListView):
    model = StudyProgram
    template_name = "flashcards/index.html"
    context_object_name = "programs"


class ProgramCreateView(CreateView):
    model = StudyProgram
    fields = ["title"]
    template_name = "flashcards/create_program.html"


class ProgramDetailView(DetailView):
    queryset = StudyProgram.objects.all()
    context_object_name = "program"
    pk_url_kwarg = "program_pk"
    template_name = "flashcards/study_program.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context["id"] = self.kwargs["program_pk"]

        return context


class ProgramDeleteView(DeleteView):
    model = StudyProgram
    success_url = reverse_lazy("index")
    pk_url_kwarg = "program_pk"
    template_name = "flashcards/delete_group.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["program_pk"]
        return context


class FlashcardCreateView(CreateView):
    model = FlashCard
    fields = ["word", "definition", "photo"]
    template_name = "flashcards/create_flashcard.html"

    def form_valid(self, form):
        form.instance.study_program = StudyProgram.objects.get(pk=self.kwargs["program_pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["program"] = get_object_or_404(StudyProgram, pk=self.kwargs["program_pk"])
        context["group_id"] = self.kwargs["program_pk"]

        return context


class CardUpdateView(UpdateView):
    fields = ["word", "definition", "photo"]
    template_name = "flashcards/edit_flashcard.html"
    queryset = FlashCard.objects.all()
    pk_url_kwarg = "card_pk"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["program"] = get_object_or_404(StudyProgram, pk=self.kwargs["program_pk"])
        context["card"] = get_object_or_404(FlashCard, pk=self.kwargs["card_pk"])
        context["group_id"] = self.kwargs["program_pk"]

        return context


class CardDetailView(DetailView):
    queryset = FlashCard.objects.all()
    context_object_name = "flashcard"
    pk_url_kwarg = "card_pk"
    template_name = "flashcards/flashcard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["program_id"] = self.kwargs["program_pk"]
        context["card_id"] = self.kwargs["card_pk"]

        return context


class CardDeleteView(DeleteView):
    model = FlashCard
    pk_url_kwarg = "card_pk"
    template_name = "flashcards/delete_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["card_pk"]
        context["gr"] = self.kwargs["program_pk"]

        return context

    def get_success_url(self):
        return reverse("program", args=[self.kwargs["program_pk"]])


########################################## api views ##########################################
class GroupViewSet(viewsets.ModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializers
