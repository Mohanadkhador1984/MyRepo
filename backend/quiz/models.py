from django.db import models


class Question(models.Model):
   
    
    question_en = models.TextField()
    question_ar = models.TextField()
    answer1_en = models.TextField()
    answer1_ar = models.TextField()
    answer2_en = models.TextField()
    answer2_ar = models.TextField()
    answer3_en = models.TextField()
    answer3_ar = models.TextField()
    answer4_en = models.TextField()
    answer4_ar = models.TextField()
    correct_answer = models.IntegerField()
    attached_text = models.TextField(null=True, blank=True)
    attached_text_ar = models.TextField(null=True, blank=True)
    year = models.IntegerField()
    type = models.CharField(max_length=50)

class Book(models.Model):
  
   
    title = models.CharField(max_length=255)
    page_number = models.IntegerField()
    content = models.TextField()
    type = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)