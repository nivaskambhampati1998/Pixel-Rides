"""PixelRides URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url, include
from .views import *
from userData import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',welcomeAnimation, name="welcome"),
    path('home/', landingPage, name="home"),
    path('about/',about, name="about"),
    path('chooseRide/',chooseRide, name="rides"),
    path('closeContacts/',closeContacts, name="closeContacts"),
    path('dashboard/',dashboard,name="dashboard"),
    path('user/',user,name="user"),
    path('wallet/',wallet,name="wallet"),
    path('security/',security,name="security"),
    path('locateMe/',locateMe,name="locateMe"),
    path('notifications/',notifications,name="notifications"),
    path('faq/',faq,name="faq"),
	path('checkRides/', checkRides, name="checkrides"),
    path('upgrade/',upgrade,name="upgrade"),
    path('chooseDriver/',chooseDriver,name="chooseDriver"),
	path('setBargain/',setBargain,name="setBargain"),
	path('getBargain/',getBargain,name="getBargain"),
	path('agreeRide/',agreeRide,name="agreeRide"),
	path('disagreeRide/',disagreeRide,name="disagreeRide"),
	path('checkAgreeRide/',checkAgreeRide,name="checkAgreeRide"),
	path('schedule/',scheduleRide,name="schedule_rides"),
	url(r'pay/(?P<driver>\w+?)/(?P<amount>\w+?)/$',pay,name="pay"),
	url(r'bargain/(?P<price>\w+?)/$',bargaining, name="bargain"),
	url(r'rideOn/(?P<driver>\w+?)/(?P<customer>\w+?)/$',rideOn,name="rideOn"),
	url(r'forgotPassword/(?P<username>\w+?)/(?P<hash_>\w+?)/$', forgotPassword, name="forgotPassword"),
	url(r'addingStops/(?P<source>\w+?)/(?P<destination>\w+?)/$',addingStops,name="addingStops"),
    url(r'confirmTransaction/(?P<sender>\w+?)/(?P<receiver>\w+?)/(?P<amount>\w+?)/$',confirmTransaction,name="confirmTransaction"),
    url(r'^userData/',include('userData.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'verifyOtp/(?P<hash_>\w+?)/(?P<pk>\w+?)/(?P<msg>\w+?)/(?P<pas>\w+?)/$', otpAuthentication, name="otp"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)