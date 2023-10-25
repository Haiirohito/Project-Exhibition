from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('made_by', views.made_by, name='made_by'),
    path('product_question', views.product_question, name='product_question'),
    path('user_question', views.product_result, name='user_question'),
    path('faq', views.faq, name='faq'),
]
