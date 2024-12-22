from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),  # Home page that renders 'home.html'
    path('start_oauth/', views.start_oauth, name='start_oauth'),  # New view to initiate OAuth2 flow
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),  # OAuth2 callback route
    path('list_photos/', views.list_photos, name='list_photos'),  # List photos from Google Photos
    path('upload_photos/', views.upload_photos, name='upload_photos'),
        # Upload photos to another Google Photos account
    path('', views.home, name='home'),
]
