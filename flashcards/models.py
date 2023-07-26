from django.db import models


# Create your models here.

class StudyProgram(models.Model):
    title = models.CharField(max_length=200, verbose_name="")


class FlashCard(models.Model):
    word = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)
    study_program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)
    photo = models.FileField(upload_to="card_images", null=True, blank=True)
