import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
#normalmente se testean modelos y vistas

class QuestionModelTest(TestCase):

    def setUp(self):
        #objeto con el que se estan realizando las pruebas
        self.question = Question(question_text= '¿Cual es el mejor Coursde director de Platzi?')
    
    def test_was_published_recently_with_future_dates(self):
        '''test_was_published_recently_with_future_dates 
           return false in case question whose pub_update is in the future
        '''
        time = timezone.now() + datetime.timedelta(days= 1)
        #future_question = Question(question_text= '¿Cual es el mejor Coursde director de Platzi?', pub_update=time)
        self.question.pub_update = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_two_days_before(self):
        time = timezone.now() - datetime.timedelta(days=2)
        self.question.pub_update = time
        self.assertIs(self.question.was_published_recently(), False)
                                # metodo de models que se estta probando

    def test_was_published_in_the_correct_timezone(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        self.question.pub_update = time
        self.assertIs(self.question.was_published_recently(), True)
                                # metodo de models que se estta probando


def create_question(question_text, days):
     """
    Create a question with the given question_text and published at the given numbers of days 
    offset to now (negative for questions in the past, positive for the ones in the future)
    """
     time = timezone.now() + datetime.timedelta(days=days)
     return Question.objects.create(question_text=question_text, pub_update = time) 


class QuestionIndexviewTests(TestCase):
    def setUp(self):
        #objeto con el que se estan realizando las pruebas
        self.question = Question(question_text= 'Pregunta para ver si esta en el futuro')

    def test_in_case_no_question(self):
        '''In case no question, return appropiate message'''
        response = self.client.get(reverse('polls:index'))
        #response = 'No polls are avaliable.'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are avaliable')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    
    def test_no_deploy_view_with_questions_whose_date_is_in_the_future(self):
        '''
        Question with future pub_updates aren't displayed in the index page
        '''
        time = timezone.now() + datetime.timedelta(days=1)
        self.question.pub_update = time
        response = self.client.get(reverse('polls:index'))
        self.assertNotIn(self.question,response.context['latest_question_list'])

    
    def test_with_past_questions(self):
        '''
        Question with past pub_update are avaliable to show in the index page.
        '''
        question = create_question('Text to prove the respective test', days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        '''
        The index page must be showed both questions if twice success the requirements
        '''
        past_question_1 = create_question(question_text='Past question text', days=-2)
        past_question_2 = create_question(question_text='Future question Text', days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_1,past_question_2], ordered=False)

'''    
    def test_future_and_past_question(self):
        
        #If past and future questions exists, only past question are avaliable to be displayed
        
        past_question = create_question(question_text='Past question', days=-30)
        future_question = create_question(question_text='Future question Text', days=2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question>'], ordered=False
                                 )
'''

class QuestionDetsilViewTest(TestCase):
    def test_future_question(self):
        '''
        The detail view in case question has a date in the future, return 404 not found error.
        '''
        future_question = create_question(question_text='Future question Text', days=30)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)    
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        The detail view in case question has a date in the  past, displays the detail view
        '''
        past_question = create_question(question_text='Past question Text', days=-1)
        url = reverse('polls:detail',args=(past_question.pk,))
        response = self.client.get(url)    
        self.assertContains(response, past_question.question_text)
      