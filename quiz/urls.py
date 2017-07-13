"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from App import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('App.urls')),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^add_quiz_home/', views.add_quiz_home, name="add_quiz_home"),
    url(r'^add_quiz/', views.add_quiz, name="add_quiz"),
    url(r'^load_quiz/', views.load_quiz, name="load_quiz"),
    url(r'^update_question/', views.update_question, name="update_question"),
    url(r'^submit_answer/', views.submit_answer, name="submit_answer"),
    url(r'^complete_test/', views.complete_test, name="complete_test"),
#    url(r'^login',views.welcome,name="login"),
#    url(r'^',include('django.contrib.auth.urls')),
#    url(r'^$',views.welcome,name="home"),
]
