# rbz_canteen/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from canteen import views
from canteen.admin import admin_site

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='admin/login.html'), name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/department', views.reports, name='reports'),
    path('accounts/login/', RedirectView.as_view(url='/', permanent=True)),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]