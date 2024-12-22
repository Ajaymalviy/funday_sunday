from django.db import models
from django.contrib.auth.models import User

# Model to store Google credentials for each user
class GoogleUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's user model
    google_credentials = models.JSONField()  # Store the OAuth credentials as JSON (Use carefully)
    google_user_id = models.CharField(max_length=255, unique=True)  # The unique Google user ID

    def __str__(self):
        return f"Google User - {self.user.username}"

# Model to store metadata of photos that are fetched from Google Photos
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each photo to a user
    google_photo_id = models.CharField(max_length=255, unique=True)  # Google Photos unique ID for each photo
    filename = models.CharField(max_length=255)  # File name of the photo
    base_url = models.URLField()  # URL to access/download the photo
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the photo was uploaded
    selected_for_transfer = models.BooleanField(default=False)  # Track if the photo is selected for transfer

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
