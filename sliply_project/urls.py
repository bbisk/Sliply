"""sliply_project URL Configuration

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
from django.contrib.auth import views as auth_views
from sliply.views import FileUploadView, SlipListView, SlipDetailView, SlipUpdateView, SlipDeleteView, SearchView, \
    UserProfileView, UserUpdateView, ItemListView, ItemDetailView, SlipCreateView, ItemUpdateView, ItemDeleteView, \
    ItemCreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', FileUploadView.as_view(), name='upload'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^slips/$', SlipListView.as_view(), name='slips'),
    url(r'^slips/create/$', SlipCreateView.as_view(), name='slip_create'),
    url(r'^slips/(?P<pk>(\d)+)/$', SlipDetailView.as_view(), name='slip_details'),
    url(r'^slips/(?P<pk>(\d)+)/edit/$', SlipUpdateView.as_view(), name='slip_edit'),
    url(r'^slips/(?P<pk>(\d)+)/delete/$', SlipDeleteView.as_view(), name='slip_delete'),
    url(r'^slips/search/$', SearchView.as_view(), name='slips_search'),
    url(r'^items/$', ItemListView.as_view(), name='items'),
    url(r'^items/(?P<pk>(\d)+)/$', ItemDetailView.as_view(), name='item_details'),
    url(r'^items/(?P<pk>(\d)+)/edit/$', ItemUpdateView.as_view(), name='item_edit'),
    url(r'^items/(?P<pk>(\d)+)/delete/$', ItemDeleteView.as_view(), name='item_delete'),
    url(r'^items/create/$', ItemCreateView.as_view(), name='item_create'),
    url(r'^profile/(?P<pk>(\d)+)/$', UserProfileView.as_view(), name='profile_details'),
    url(r'^profile/(?P<pk>(\d)+)/edit/$', UserUpdateView.as_view(), name='profile_edit'),

]
