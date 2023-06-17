import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
#Django automaticamente genera ese campo id, lo maneja por nosotros de formar autoincreental
class Question(models.Model):    
    question_text = models.CharField(max_length=200)# Se define el tipo de dato y como parametro va el maximo de caracteres
    pub_update = models.DateTimeField(auto_now_add=True)# Se define fecha de publicación

    def __str__(self) -> str:
        return self.question_text
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_update >= timezone.now() - datetime.timedelta(days=10)
    
class Choice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text
