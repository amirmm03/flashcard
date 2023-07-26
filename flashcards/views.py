from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView

from flashcards.models import StudyProgram, FlashCard


# Create your views here.

def index(request):

    programs = StudyProgram.objects.all()
    template = loader.get_template("flashcards/index.html")
    context = {
        "programs": programs,
    }

    return HttpResponse(template.render(context))


class ProgramListView(ListView):
    model = StudyProgram
    template_name = "flashcards/index.html"
    context_object_name = "programs"



def create_program(request):
    template = loader.get_template("flashcards/create_program.html")
    context = {

    }

    if request.method == "POST":

        context = request.POST

        try:
            s = StudyProgram.objects.create(title=context['title'])
            return HttpResponseRedirect(reverse("program", args=[s.id]))

        except:
            pass

    return HttpResponse(template.render(context, request))


def study_program(request, program_pk):
    program = get_object_or_404(StudyProgram, pk=program_pk)
    template = loader.get_template("flashcards/study_program.html")
    context = {
        "program": program,
        "flashcards": program.flashcard_set.all()
    }
    return HttpResponse(template.render(context, request))


def delete_program(request, program_pk):
    if request.method == "POST":
        this_program = get_object_or_404(StudyProgram, pk=program_pk)
        this_program.delete()
    return HttpResponseRedirect(reverse("index"))


def create_flashcard(request, program_pk, is_edit, card_pk=None, ):
    program = get_object_or_404(StudyProgram, pk=program_pk)

    template = loader.get_template("flashcards/create_flashcard.html")
    context = {

    }

    if request.method == "POST":

        context = request.POST

        try:
            if is_edit:
                card = get_object_or_404(FlashCard, pk=card_pk)
                card.word = context["word"]
                card.definition = context["definition"]
                if "pic" in request.FILES:
                    card.photo = request.FILES["pic"]
                else:
                    card.photo = None
                card.save()
                return HttpResponseRedirect(reverse("flashcard", args=[program.id, card.id]))
            else:
                card = FlashCard(word=context["word"], definition=context["definition"], study_program=program)

                if "pic" in request.FILES:
                    card.photo = request.FILES["pic"]
                card.save()

                return HttpResponseRedirect(reverse("program", args=[program.id]))

        except:
            pass

    context = {
        "program": program,
        "is_edit": is_edit
    }
    if is_edit:
        context["card"] = get_object_or_404(FlashCard, pk=card_pk)

    return HttpResponse(template.render(context, request))


def get_program_and_card(program_pk, card_pk):
    program = get_object_or_404(StudyProgram, pk=program_pk)
    card = get_object_or_404(FlashCard, pk=card_pk)
    if card.study_program != program:
        raise Http404("card is not in this program")
    return program, card


def flashcard(request, program_pk, card_pk):
    program, card = get_program_and_card(program_pk, card_pk)

    template = loader.get_template("flashcards/flashcard.html")
    context = {
        "program": program,
        "flashcard": card
    }

    return HttpResponse(template.render(context, request))


def delete_card(request, program_pk, card_pk):
    program, card = get_program_and_card(program_pk, card_pk)
    if request.method == "POST":
        card.delete()
    return HttpResponseRedirect(reverse("program", args=[program_pk]))
