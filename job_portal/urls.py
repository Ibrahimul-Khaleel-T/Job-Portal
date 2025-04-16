"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from job_portal_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='menu'),
    path('seeker_signup',views.jobseeker_signup,name='seeker_signup'),
    path('employee_signup',views.employee_signup,name='employee_signup'),
    path('signin',views.signin,name='signin'),
    path('reset_password',views.password_reset_request,name='reset_password'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('set_new_password',views.set_new_password,name='set_new_password'),
    path('seeker_home',views.seeker_home,name='seeker_home'),
    path('seeker_profile',views.seeker_profile,name='seeker_profile'),
    path('logout',views.Logout,name='logout'),
    path('seeker_edit',views.seeker_edit,name='seeker_edit'),
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)