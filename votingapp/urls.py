
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:topic_id>/', views.detail, name='detail'),
    path('<int:topic_id>/results/', views.results, name='results'),
    path('<int:topic_id>/vote/', views.vote, name='vote'),
]
