from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.AppLoginView.as_view(), name='login'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.logout_view, name='logout'),

    path('appplicayions/create/', views.ApplicationCreateView.as_view(), name='application_create'),
    path('appplicayions/<int:pk>>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),

    #дописать пути

    #админка хз какая из

]