from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from PhageBank.core import views as core_views


urlpatterns = [
    # Uncomment the next line to enable the admin:
    url(r'^$', core_views.index, name='index'),
    url(r'^new_index/', core_views.new_index, name='new_index'),
    url(r'^home/', core_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^mylogin/$', core_views.mylogin, name='mylogin'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^add/$', core_views.addphage, name='add'),
    url(r'^contact/$', core_views.contact, name='contact'),
    url(r'^view/$', core_views.viewphages, name='view'),
    url(r'^phage/$', core_views.viewPhage, name='phage'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^uploads/form/$', core_views.model_form_upload, name='model_form_upload'),
]
