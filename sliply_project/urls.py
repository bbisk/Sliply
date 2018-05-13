import registration
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from sliply.views import FileUploadView, SlipListView, SlipDetailView, SlipUpdateView, SlipDeleteView, SearchView, \
    UserProfileView, UserUpdateView, ItemListView, ItemDetailView, SlipCreateView, ItemUpdateView, ItemDeleteView, \
    ItemCreateView
from sliply_api.views import SlipListViewAPI
from sliply_project.settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', UserProfileView.as_view(), name='main'),
    url(r'^upload/$', FileUploadView.as_view(), name='upload'),
    url(r'^login/$', auth_views.login, {'redirect_field_name': 'next'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^accounts/', include('registration.backends.default.urls')),
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
    url(r'^profile/$', UserProfileView.as_view(), name='profile_details'),
    url(r'^profile/(?P<pk>(\d)+)/edit/$', UserUpdateView.as_view(), name='profile_edit'),
    url(r'^api/$', SlipListViewAPI.as_view(), name='slip_api'),
]

if DEBUG is True:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)