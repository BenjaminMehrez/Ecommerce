from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.conf import settings


def landingpage_middleware(get_response):
    def middleware(request):
        
        # Before middleware
        if page_is_enabled('Maintenance'):
            if  request.path != reverse('maintenance'):
                if '/jefe/' not in request.path:
                    if settings.STAGING != 'True':
                        return HttpResponseRedirect(reverse('maintenance'))
            
        if page_is_enabled('Staging'):
            if request.path != reverse('locked'):
                if '/jefe/' not in request.path:
                    if settings.STAGING != 'True':
                        if 'staging_access' not in request.session:
                            return HttpResponseRedirect(reverse('locked'))
            
        response = get_response(request)
        
        # After middleware
        
        return response
    
    return middleware



def page_is_enabled(page_name):
    page = LandingPage.objects.filter(name=page_name).first()
    if page:
        return page.is_enabled
    else:
        return False