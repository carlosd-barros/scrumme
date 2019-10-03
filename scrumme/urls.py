# https://docs.djangoproject.com/en/2.2/topics/http/urls/

from django.conf import settings
from django.urls import path, include
from django.urls.base import reverse_lazy
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from django.contrib import admin

urlpatterns = [
    path(
        '',
        RedirectView.as_view(
            url=reverse_lazy(
                'core:dashboard'
            ),
            permanent=False
        ),
        name="home"
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'auth/',
        include(
            'accounts.urls',
            namespace='auth'
        ),
        name='auth'
    ),
    path(
        'core',
        include(
            'core.urls',
            namespace='core'
        ),
        name='core'
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += [
    path(
        'favicon.ico',
        RedirectView.as_view(
            url='/static/images/favicon.ico',
            permanent=True
        )
    )
]