from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # HTML views for login and register pages
    path('', views.index, name='index'),
    path('<int:topic_id>/', views.detail, name='detail'),
    path('<int:topic_id>/results/', views.results, name='results'),
    path('<int:topic_id>/vote/', views.vote, name='vote'),
    # path('login/', views.login, name='login'),   # Login HTML view
    path('register/', views.register_view, name='register'),   # Register HTML view
    
    # # API endpoints for login and register (for token-based authentication)
    path('login/', views.login_view, name='login'),   # API Login endpoint
    # path('api/register/', views.api_register, name='register_api'),   # API Register endpoint
]
