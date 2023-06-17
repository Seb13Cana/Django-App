from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    #ejemplo rutas en Chrome
    #/polls/
    path('', views.IndexView.as_view(), name='index'),
    #/polls/id_pregunta/
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    #/polls/id_pregunta/result/
    path('<int:pk>/result/', views.ResultView.as_view(), name='result'),
    #/polls/id_pregunta/vote/
    path('<int:question_id>/vote/', views.vote, name='vote')
]