from django.urls import path
from .views import *

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz/create/', quiz_create, name='quiz_create'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('result/<int:answer_id>/', quiz_result, name='quiz_result'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
]