import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from flashcards.models import StudyProgram, FlashCard


# Create your views here.

# def index(request):
#
#     programs = StudyProgram.objects.all()
#     template = loader.get_template("flashcards/index.html")
#     context = {
#         "programs": programs,
#     }
#
#     return HttpResponse(template.render(context))
#

class ProgramListView(ListView):
    model = StudyProgram
    template_name = "flashcards/index.html"
    context_object_name = "programs"


# def create_program(request):
#     template = loader.get_template("flashcards/create_program.html")
#     context = {}
#
#     if request.method == "POST":
#
#         context = request.POST
#
#         try:
#             s = StudyProgram.objects.create(title=context['title'])
#             return HttpResponseRedirect(reverse("program", args=[s.id]))
#
#         except:
#             pass
#
#     return HttpResponse(template.render(context, request))

class ProgramCreateView(CreateView):
    model = StudyProgram
    fields = ["title"]
    template_name = "flashcards/create_program.html"

    def form_valid(self, form):
        form.instance.created_date = datetime.datetime.now()
        return super().form_valid(form)


# def study_program(request, program_pk):
#     program = get_object_or_404(StudyProgram, pk=program_pk)
#     template = loader.get_template("flashcards/study_program.html")
#     context = {
#         "program": program,
#         "flashcards": program.flashcard_set.all()
#     }
#     return HttpResponse(template.render(context, request))
#

class ProgramDetailView(DetailView):
    queryset = StudyProgram.objects.all()
    context_object_name = "program"
    pk_url_kwarg = "program_pk"
    template_name = "flashcards/study_program.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context["flashcards"] = self.object.flashcard_set.all()
        return context


def delete_program(request, program_pk):
    if request.method == "POST":
        this_program = get_object_or_404(StudyProgram, pk=program_pk)
        this_program.delete()
    return HttpResponseRedirect(reverse("index"))


# def create_flashcard(request, program_pk, is_edit, card_pk=None, ):
#     program = get_object_or_404(StudyProgram, pk=program_pk)
#
#     template = loader.get_template("flashcards/create_flashcard.html")
#     context = {
#
#     }
#
#     if request.method == "POST":
#
#         context = request.POST
#
#         try:
#             if is_edit:
#                 card = get_object_or_404(FlashCard, pk=card_pk)
#                 card.word = context["word"]
#                 card.definition = context["definition"]
#                 if "pic" in request.FILES:
#                     card.photo = request.FILES["pic"]
#                 else:
#                     card.photo = None
#                 card.save()
#                 return HttpResponseRedirect(reverse("flashcard", args=[program.id, card.id]))
#             else:
#                 card = FlashCard(word=context["word"], definition=context["definition"], study_program=program)
#
#                 if "pic" in request.FILES:
#                     card.photo = request.FILES["pic"]
#                 card.save()
#
#                 return HttpResponseRedirect(reverse("program", args=[program.id]))
#
#         except:
#             pass
#
#     context = {
#         "program": program,
#         "is_edit": is_edit
#     }
#     if is_edit:
#         context["card"] = get_object_or_404(FlashCard, pk=card_pk)
#
#     return HttpResponse(template.render(context, request))


class FlashcardCreateView(CreateView):
    model = FlashCard
    fields = ["word", "definition", "photo"]
    template_name = "flashcards/create_flashcard.html"

    def form_valid(self, form):
        form.instance.study_program = StudyProgram.objects.get(pk=self.kwargs["program_pk"])
        form.instance.last_modified = datetime.datetime.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["program"] = get_object_or_404(StudyProgram, pk=self.kwargs["program_pk"])

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

        return context

    def form_valid(self, form):
        form.instance.last_modified = datetime.datetime.now()
        return super().form_valid(form)



def get_program_and_card(program_pk, card_pk):
    program = get_object_or_404(StudyProgram, pk=program_pk)
    card = get_object_or_404(FlashCard, pk=card_pk)
    if card.study_program != program:
        raise Http404("card is not in this program")
    return program, card


# def flashcard(request, program_pk, card_pk):
#     program, card = get_program_and_card(program_pk, card_pk)
#
#     template = loader.get_template("flashcards/flashcard.html")
#     context = {
#         "program": program,
#         "flashcard": card
#     }
#
#     return HttpResponse(template.render(context, request))


class CardDetailView(DetailView):
    queryset = FlashCard.objects.all()
    context_object_name = "flashcard"
    pk_url_kwarg = "card_pk"
    template_name = "flashcards/flashcard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["program"] = get_object_or_404(StudyProgram, pk=self.kwargs["program_pk"])

        return context


def delete_card(request, program_pk, card_pk):
    program, card = get_program_and_card(program_pk, card_pk)
    if request.method == "POST":
        card.delete()
    return HttpResponseRedirect(reverse("program", args=[program_pk]))
