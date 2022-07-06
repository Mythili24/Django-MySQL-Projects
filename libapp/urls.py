from django import views
from django.contrib import admin
from django.urls import path
from libapp import views

app_name = 'libapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('books/<int:book_id>', views.detail, name='detail'),
    path('add/', views.add_book, name='add_book'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('admin_login/',views.adminloginPage,name='admin_login'),
    path('logout/',views.logoutUser,name='logout'),
    path('members/',views.members,name='members'),
    path('members/<int:id>',views.member_detail,name='member_detail'),
    path('issue_detail/<int:member_id>',views.issue_detail,name='issue_detail'),
    path('add_member/', views.add_member, name='add_member'),
    path('update_member/<int:id>', views.update_member, name='update_member'),
    path('delete_member/<int:id>/',views.delete_member,name='delete_member'),
    path('issue_book/<int:member_id>', views.issue_book, name='issue_book'),
    path('return_book/<int:id>', views.return_book, name='return_book'),
    path('profile/',views.profile,name='profile'),
    path('viewmember/<slug:user>/',views.viewmember,name='viewmember'),
#    path('search/',views.search,name='search'),
]