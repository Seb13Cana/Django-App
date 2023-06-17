from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self) -> QuerySet[Any]:
        '''return LAST 5 PUBLISHED QUESTIONS'''#super().get_queryset()
        #return Question.objects.order_by('-pub_update')[:5]
        return Question.objects.filter(pub_update__lte=timezone.now()).order_by('-pub_update')[:5]
    

class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_queryset(self) -> QuerySet[Any]:
        '''
        Exclude any question that aren't published yet
        '''
        return Question.objects.filter(pub_update__lte= timezone.now())


class ResultView(generic.DetailView):
    template_name = 'polls/result.html'
    model = Question
'''
def index(request):
    latest_question_list = Question.objects.all() 
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list
    })


#Funcion para ver en detalle el template de cada pregunta // 
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{
        'question': question
    })


#Funcion para ver template de resultados a la pregunta
def result(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/result.html', {
        'question': question
    })

'''
#Funcion para ver template de votos
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': 'No elegiste una respuesta valida'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))



