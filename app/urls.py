from django.urls import path,include
from .views import *
from django.conf.urls.static import static
urlpatterns=[
    path('Login/',Login,name="login"),
    path('Logout/',Logout,name="logout"),
    path('',homepage,name="home"),
    path('register/',register,name="register"),
    path('profile/edit',editprofile,name="editprofile"),
    path('profile/uploadImage',uploadprofile,name="uploadprofile"),
    path('profile/<int:id>',profile,name="profile"),
    path('assessment/<int:id>',view_assessment,name="assessment"),
    path('result/<int:id>',view_result,name="result"),
    path('activate/<str:id>',activate_account,name="activate"),
  #  path('Analytics/<int:id>',viewanalytics,name="analytics"),
]+ static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)