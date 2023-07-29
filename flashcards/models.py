from django.db import models
from django.urls import reverse


# Create your models here.

class StudyProgram(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ساخت")
    updated = models.DateTimeField(auto_now=True, verbose_name="اخرین تغییر")

    def get_absolute_url(self):
        return reverse("program", kwargs={"program_pk": self.pk})

    def __str__(self):
        return self.title


class FlashCard(models.Model):
    word = models.CharField(max_length=200, verbose_name="کلمه")
    definition = models.CharField(max_length=200, verbose_name="معنی")
    study_program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE, verbose_name="برنامه ی مطالعه")
    photo = models.FileField(upload_to="card_images", null=True, blank=True, verbose_name="عکس")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ساخت")
    updated = models.DateTimeField(auto_now=True, verbose_name="اخرین تغییر")

    def get_absolute_url(self):
        return reverse("flashcard", kwargs={"program_pk": self.study_program.pk, "card_pk": self.pk})

    def __str__(self):
        return self.word
