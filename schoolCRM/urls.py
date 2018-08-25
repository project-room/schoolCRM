"""schoolCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from operators.views import LoginIndexView, LogOutView, StudyListView, StudyInfoTrashListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^log_in/$', LoginIndexView.as_view(), name="log_in"),
    url('^log_out/$', LogOutView.as_view(), name="log_out"),
    url('^$', StudyListView.as_view(), name="index"),
    url(r'^course/$', StudyListView.as_view(), name="lesson"),
    url(r'^teacher/', include("teacher.urls")),
    url(r'^student/', include("student.urls")),
    url(r'^operators/', include("operators.urls")),

]
