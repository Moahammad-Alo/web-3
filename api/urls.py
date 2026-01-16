"""API URL Configuration"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication views (Django templates)
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main SPA (authenticated users only)
    path('', views.main_spa, name='home'),
    
    # CSRF token endpoint
    path('api/csrf/', views.get_csrf_token, name='csrf_token'),
    
    # User API
    path('api/user/status/', views.api_user_status, name='api_user_status'),
    path('api/profile/', views.api_profile, name='api_profile'),
    
    # Items API
    path('api/items/', views.api_items, name='api_items'),
    path('api/items/<int:item_id>/', views.api_item_detail, name='api_item_detail'),
    path('api/items/<int:item_id>/bids/', views.api_item_bids, name='api_item_bids'),
    path('api/items/<int:item_id>/questions/', views.api_item_questions, name='api_item_questions'),
    
    # Questions API
    path('api/questions/<int:question_id>/answers/', views.api_question_answer, name='api_question_answer'),
]
