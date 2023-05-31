"""HealthPredictionSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from predictionapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,homee, name="homee"),
    path('homee/' ,home, name="home"),
    path('index/' ,index, name="index"),
    path('contact/' ,contact, name="contact"),
    path('services/' ,services, name="services"),
    path('about/' ,about, name="about"),
    path('admin-login/', adminLogin, name="admin_login"),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-doctor/', add_doctor, name="add_doctor"),
    path('view-doctors/', view_doctors, name="view_doctors"),
    path('edit-doctor/<int:pid>/', edit_doctor, name="edit_doctor"),
    path('delete-product/<int:pid>/', delete_doctor, name="delete_doctor"),
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    path('profile/', profile, name="profile"),
    path('logout/', logoutuser, name="logout"),
    path('change-password/', change_password, name="change_password"),
    path('user-feedback/', user_feedback, name="user_feedback"),
    path('manage-feedback/', manage_feedback, name="manage_feedback"),
    path('delete-feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    path('feedback-read/<int:pid>/', read_feedback, name="read_feedback"),
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
    path('register-for-blood-donation/', register_for_blood_donation, name="register_for_blood_donation"),
    path('view-all-blood-donor/', view_blood_donor, name="view_blood_donor"),
    path('manage-blood/', manage_blood, name="manage_blood"),
    path('delete-blood/<int:pid>/', delete_blood, name="delete_blood"),
    path('blood-read/<int:pid>/', read_blood, name="read_blood"),
    path('blood-unread/<int:pid>/', unread_blood, name="unread_blood"),
    path('add-donor/', add_donor, name="add_donor"),
    path('check-disease/', checkdisease, name="checkdisease"),
    path('predicted-disease/', predicteddisease, name="predicteddisease"),
    path('history-disease/', showhistory, name="showhistory"),
    path('view-search/', view_search, name="view_search"),
]
