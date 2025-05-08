from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/new/', views.movie_create, name='movie_create'),
    path('movie/<int:pk>/edit/', views.movie_edit, name='movie_edit'),
    path('movie/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('movie/<int:movie_pk>/review/add/', views.review_create, name='review_create'),
    path('movie/<int:movie_pk>/review/<int:review_pk>/edit/', views.review_edit, name='review_edit'),
    path('movie/<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
]