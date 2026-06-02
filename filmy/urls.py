from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('filmy/', views.filmy_lista, name='filmy_lista'),
    path('filmy/dodaj/', views.filmy_dodaj, name='filmy_dodaj'),
    path('filmy/szukaj/', views.filmy_szukaj, name='filmy_szukaj'),
    path('filmy/edytuj/<int:film_id>/', views.filmy_edytuj, name='filmy_edytuj'),
    path('filmy/usun/<int:film_id>/', views.filmy_usun, name='filmy_usun'),

    path('rezyserzy/', views.rezyserzy_lista, name='rezyserzy_lista'),
    path('rezyserzy/dodaj/', views.rezyserzy_dodaj, name='rezyserzy_dodaj'),
    path('rezyserzy/szukaj/', views.rezyserzy_szukaj, name='rezyserzy_szukaj'),
    path('rezyserzy/edytuj/<int:rezyser_id>/', views.rezyserzy_edytuj, name='rezyserzy_edytuj'),
    path('rezyserzy/usun/<int:rezyser_id>/', views.rezyserzy_usun, name='rezyserzy_usun'),

    path('recenzje/', views.recenzje_lista, name='recenzje_lista'),
    path('recenzje/dodaj/', views.recenzje_dodaj, name='recenzje_dodaj'),
    path('recenzje/szukaj/', views.recenzje_szukaj, name='recenzje_szukaj'),
    path('recenzje/edytuj/<int:recenzja_id>/', views.recenzje_edytuj, name='recenzje_edytuj'),
    path('recenzje/usun/<int:recenzja_id>/', views.recenzje_usun, name='recenzje_usun'),
]