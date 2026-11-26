from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.AppLoginView.as_view(), name='login'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.logout_view, name='logout'),

    path('applications/create/', views.ApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),

    path('admin/', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('admin/app/<int:pk>/accept/', views.AcceptApplicationView.as_view(), name='admin_accept'),
    path('admin/app/<int:pk>/done/', views.DoneApplicationView.as_view(), name='admin_done'),
    # path('admin/categories/', views.CategoryListView.as_view(), name='admin_categories'),
    # path('admin/categories/add/', views.CategoryCreateView.as_view(), name='admin_category_add'),
    # path('admin/categories/delete/', views.CategoryDeleteView.as_view(), name='admin_category_delete'),
]