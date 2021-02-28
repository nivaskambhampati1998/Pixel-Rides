from django.conf.urls import url
from userData import views

app_name = 'userData'

urlpatterns=[
    url(r'^registration/$',views.registration,name='registration'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^enterNumber/$',views.sendOtp,name='sendOtp'),
]