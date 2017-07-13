from django.conf.urls import include, url
from django.contrib import admin
from App import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name="home"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout")
]

#urlpatterns = [
#    url(r'^api/',include(router.urls)),
#    url(r'^$', views.home, name="home"),
#    url(r'^create/',views.create_user,name="create_user"),
#    url(r'^validate_login/',views.log_in,name="log_user"),
#    url(r'^add_exam/',views.add_exam,name="add_exam"),
#    url(r'^add_question/',views.add_question,name="add_question"),
#    url(r'^test',views.get_data,name="getdata"),
#    url(r'^logout',views.log_out,name="log_out"),
#]