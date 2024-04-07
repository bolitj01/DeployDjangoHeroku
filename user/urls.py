from django.urls import path
from user import views;

urlpatterns = [
    # For testing, get CSRF token
    path('get_csrf/', views.GetCSRFToken.as_view(), name='get_csrf'),
    path('create_user/', views.CreateUser.as_view(), name='create_user'),
    path('delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('is_logged_in/', views.IsLoggedInView.as_view(), name='is_logged_in'),
]
