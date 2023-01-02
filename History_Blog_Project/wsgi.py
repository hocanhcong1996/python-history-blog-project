"""
WSGI config for History_Blog_Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'History_Blog_Project.settings')

application = get_wsgi_application()

# 2/1/2023 Deploy to Vercel
app = application