from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
   path('',views.home,name='home'),
   path('accounts/register/',views.register,name="register"),
   path('accounts/login/',views.login,name="login"),
   path('upload/',views.upload_file,name="upload"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)