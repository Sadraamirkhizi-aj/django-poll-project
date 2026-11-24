from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'home'

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('polls/', views.index, name='index'),
    path('polls/<int:question_id>/', views.detail, name='detail'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/<int:question_id>/results/', views.results, name='results'),

    path('thanks/', views.thanks, name='thanks'),
    path('about-me/', views.about_me, name='about_me'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)