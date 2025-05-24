from django.urls import path
from . import views
from .debug_view import debug_user_type

urlpatterns = [
    path('doctor/blogs/', views.doctor_blog_list, name='doctor_blog_list'),
    path('doctor/blogs/create/', views.create_blog, name='create_blog'),
    path('doctor/blogs/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('doctor/blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('blogs/', views.patient_blog_list, name='patient_blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('debug-user-type/', debug_user_type, name='debug_user_type'),
]
