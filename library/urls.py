from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('authors/', views.authors, name='authors'),
    path('members/', views.members, name='members'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrowing_id>/', views.return_book, name='return_book'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
]

