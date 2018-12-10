from django.contrib import admin
from django.urls import path,include

urlpatterns = [
	path('micro/', include('micro.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

]



admin.site.site_header = 'SAGCE'
admin.site.index_title = 'SAGCE'
admin.site.site_title = 'SAGCE'