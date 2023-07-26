from django.db import models
from django.urls import reverse


# Create your models here.

class StudyProgram(models.Model):
    title = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse("program", kwargs={"program_pk": self.pk})


class FlashCard(models.Model):
    word = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)
    study_program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)
    photo = models.FileField(upload_to="card_images", null=True, blank=True)
    last_modified = models.DateTimeField()

    def get_absolute_url(self):
        return reverse("flashcard", kwargs={"program_pk": self.study_program.pk, "card_pk": self.pk})
