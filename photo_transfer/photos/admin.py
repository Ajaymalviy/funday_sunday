from django.contrib import admin
from .models import GoogleUser, Photo

# Register GoogleUser model in admin panel
@admin.register(GoogleUser)
class GoogleUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_user_id')
    search_fields = ('user__username', 'google_user_id')

# Register Photo model in admin panel
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'filename', 'google_photo_id', 'uploaded_at', 'selected_for_transfer')
    search_fields = ('user__username', 'filename', 'google_photo_id')
    list_filter = ('selected_for_transfer', 'uploaded_at')
