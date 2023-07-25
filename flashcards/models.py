from django.db import models


# Create your models here.

class StudySet(models.Model):
    title = models.CharField(max_length=200)


class FlashCard(models.Model):
    word = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE)
