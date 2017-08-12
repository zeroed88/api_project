from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from main import views

urlpatterns = [
    url(r'register/$', views.register, name='register'),
    url(r'validate/$', views.validate, name='validate'),
    url(r'login/$', obtain_jwt_token, name='login'),
    url(r'profile/$', views.getUserInfo, name='getUserInfo'),
    url(r'reset_email/$', views.reset_email, name='reset_email'),
    url(r'set_new_email/$', views.set_new_email, name='set_new_email'),
    url(r'send_code_old_email/$', views.send_code_old_email, name='send_code_old_email'),
    url(r'check_old_email/$', views.check_old_email, name='check_old_email'),
    url(r'check_new_email/$', views.check_new_email, name='check_new_email'),
    url(r'update_password/$', views.update_password, name='update_password'),
    url(r'check_username/$', views.check_username, name='check_username'),
    url(r'check_password/$', views.check_password, name='check_password')

]
