from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from flashcards.models import StudySet, FlashCard


# Create your views here.

def index(request):
    sets = StudySet.objects.all()

    template = loader.get_template("flashcards/index.html")
    context = {
        "sets": sets,
    }
    return HttpResponse(template.render(context))


def create_set(request):
    template = loader.get_template("flashcards/create_set.html")
    context = {

    }

    if request.method == "POST":

        context = request.POST

        try:
            s = StudySet.objects.create(title=context['title'])
            return HttpResponseRedirect(reverse("set", args=[s.id]))

        except:
            pass

    return HttpResponse(template.render(context, request))


def study_set(request, setpk):
    this_set = get_object_or_404(StudySet, pk=setpk)
    template = loader.get_template("flashcards/study_set.html")
    context = {
        "set": this_set,
        "flashcards": this_set.flashcard_set.all()
    }
    return HttpResponse(template.render(context, request))


def delete_set(request, setpk):
    if request.method == "POST":
        this_set = get_object_or_404(StudySet, pk=setpk)
        this_set.delete()
    return HttpResponseRedirect(reverse("index"))


def create_flashcard(request, setpk, is_edit, cardpk=None, ):
    this_set = get_object_or_404(StudySet, pk=setpk)

    template = loader.get_template("flashcards/create_flashcard.html")
    context = {
        "set": this_set,
        "is_edit": is_edit
    }
    if is_edit:
        context["card"] = get_object_or_404(FlashCard, pk=cardpk)

    if request.method == "POST":

        context = request.POST

        try:
            if is_edit:
                card = get_object_or_404(FlashCard, pk=cardpk)
                card.word = context["word"]
                card.definition = context["definition"]
                card.save()
                return HttpResponseRedirect(reverse("flashcard", args=[this_set.id, card.id]))
            else:
                card = FlashCard.objects.create(word=context["word"], definition=context["definition"],
                                                study_set=this_set)
                return HttpResponseRedirect(reverse("set", args=[this_set.id]))

        except:
            pass

    return HttpResponse(template.render(context, request))


def get_set_and_card(setpk, cardpk):
    this_set = get_object_or_404(StudySet, pk=setpk)
    card = get_object_or_404(FlashCard, pk=cardpk)
    if card.study_set != this_set:
        raise Http404("card is not in this set")
    return this_set, card


def flashcard(request, setpk, cardpk):
    this_set, card = get_set_and_card(setpk, cardpk)

    template = loader.get_template("flashcards/flashcard.html")
    context = {
        "set": this_set,
        "flashcard": card
    }

    return HttpResponse(template.render(context, request))


def delete_card(request, setpk, cardpk):
    this_set, card = get_set_and_card(setpk, cardpk)
    if request.method == "POST":
        card.delete()
    return HttpResponseRedirect(reverse("set", args=[setpk]))
