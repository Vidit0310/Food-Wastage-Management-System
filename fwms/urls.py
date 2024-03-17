"""
URL configuration for garbage_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import settings
from . import views

urlpatterns = [
    path('', views.landing_page,name='landing_page'),
    path('admin/', admin.site.urls),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('user_side_nav/', views.user_side_nav, name="user_side_nav"),
    path('FC_side_nav/', views.FC_side_nav, name="FC_side_nav"),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('index/', views.index, name='index'),
    path('Create_food_collection_request/<str:email>', views.Create_food_collection_request, name='Create_food_collection_request'),
    path('feedbacks_master_byUsers/<str:email>', views.feedbacks_byUsers, name='feedbacks_master_byUsers'),
    path('feedbacks_byFC/<str:email>', views.feedbacks_byFC, name='feedbacks_byFC'),
    path('User_profile/<str:email>', views.User_profile, name='User_profile'),
    path('FC_profile/<str:email>', views.FC_profile, name='FC_profile'),
    path('User_view_fcrs/<str:email>', views.User_view_fcrs, name='User_view_fcrs'),
    path('User_view_fcr/<str:email>/<int:id>', views.User_view_fcr, name='User_view_fcr'),
    path('FC_view_fcrs/<str:email>', views.FC_view_fcrs, name='FC_view_fcrs'),
    path('FC_view_fcr/<str:email>/<int:id>', views.FC_view_fcr, name='FC_view_fcr'),


]+ static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static') + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
