
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf.urls.static import static
from Earning import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login/',views.login),
    path('signup/', views.signup),
    path('me/', views.me),
    path('recharge/', views.recharge),
    path('withdrawn/', views.withdrawn),
    path('withd/', views.withd),
    path('shop/', views.shop),
    path('rdetails/', views.rdetails),
    path('invite/', views.invite),
    path('idetails/', views.idetails),
    path('wdetails/', views.wdetails),
    path('bdetails/', views.bdetails),
    path('generate/<int:num>', views.income),
    path('updatewithdrawn/', views.updatewithdrawn),
    path('logout/', views.logout),
    path('singleproduct/<int:num>/',views.singleproduct),
    path('forgetusername/', views.forgetusername),
    path('forgetotp/', views.forgetotp),
    path('forgetpassword/', views.forgetpassword),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)