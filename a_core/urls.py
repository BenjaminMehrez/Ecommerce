"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
# from a_users.views import profile_view

# Sitemaps
from django.contrib.sitemaps.views import sitemap
from a_store.sitemaps import *
sitemaps = {
    'static': StaticSitemap,
    'categories': CategorySitemap,
    'productpages': ProductpageSitemap,
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('jefe/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',  include('a_store.urls')),
    path('users/', include('a_users.urls')),
    path('useradmin/', include('a_useradmin.urls')),
    path('_/', include('a_landingpages.urls')),
    # path('@<username>/', profile_view, name='profile'),
]


# Only used when DEBUG=True, whitenoise can serve files when DEBUG=False
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)