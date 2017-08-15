from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signin/$', views.signin, name='login'),
    url(r'^signout/$', views.signout, name='logout'),
    url(r'^signup/$', views.signup, name='register'),
    url(r'^chatbots/list$', views.chatbots00, name='chatbots00'),
    url(r'^chatbots//?(?P<bot_id>\d+)?/chat$',
        views.chatbots01, name='chatbots01'),
    url(r'^guide/$', views.guide, name='guide'),
    url(r'^faqs/$', views.faqs, name='faqs'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^teach/edit$', views.teach00, name='teach00'),
    url(r'^teach/upload$', views.teach01, name='teach01'),
    url(r'^setting/bot$', views.setting00, name='setting00'),
    url(r'^setting/user$', views.setting01, name='setting01'),
    url(r'^embed$', views.embed, name='embed')
]
