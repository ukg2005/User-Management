from django.urls import path
from . import views
# Import the fixes directly
from accounts.fix_view import fix_user_types

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('fix-user-types/', fix_user_types, name='fix_user_types'),
]