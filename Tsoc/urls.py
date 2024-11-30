from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from xml.dom.minidom import Document
from django.conf.urls.static import static

urlpatterns = [
    path('deltadmin/', admin.site.urls),
    path('',include('tango.urls')),
    path('accounts/', include('allauth.urls')),
    path('captcha/',include('captcha.urls')),
    
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
