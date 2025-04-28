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
from job_portal_app.views import JobDeleteView

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
    path('job_ajax_details/<int:job_id>/', views.job_ajax_details, name='job_ajax_details'),
    path('job_ajax_details/<int:job_id>/', views.job_ajax_details, name='job_ajax_details'),
    path('seeker_profile',views.seeker_profile,name='seeker_profile'),
    path('logout',views.Logout,name='logout'),
    path('seeker_edit',views.seeker_edit,name='seeker_edit'),
    path('employee_home',views.employee_home,name='employee_home'),
    path('employee_profile',views.employee_profile,name='employee_profile'),
    path('employee_edit',views.employee_edit,name='employee_edit'),
    path('job_post',views.job_post,name='job_post'),
    path('select_edit_job_post',views.select_edit_job_post,name='select_edit_job_post'),
    path('edit_job_post/<int:id>',views.edit_job_post,name='edit_job_post'),
    path('job_details/<int:id>', views.job_details, name='job_details'),
    path('<int:pk>/job_post_delete',JobDeleteView.as_view(),name='job_post_delete'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('load_applicant_details/<int:id>/', views.load_applicant_details, name='load_applicant_details'),
    path('job_application_response/<int:application_id>',views.job_application_response,name='job_application_response'),
    path('seeker_notification',views.seeker_notification,name='seeker_notification'),
]    
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)