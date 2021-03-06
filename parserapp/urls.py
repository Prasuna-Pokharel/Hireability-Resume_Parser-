from django.conf import settings
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('resumeparser/',views.resume_parser,name='resume_parser'),
    path('dataextraction/',views.data_extraction,name='data_extraction'),
    path('faq/',views.faq,name='faq'),
    path('terms/',views.terms,name='terms'),
    path('login/',views.login,name='login'),

]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)