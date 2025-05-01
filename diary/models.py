from django.conf import settings
from django.db import models
import os
from datetime import datetime
from pathlib import Path

def generate_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    base_name = f'{instance.page_date.strftime("%Y%m%d")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    file_counter = 1
    new_filename = f'{base_name}_{file_counter:04d}{ext}'

    while os.path.exists(os.path.join(settings.MEDIA_ROOT, 'diary', new_filename)):
        file_counter += 1
        new_filename = f'{base_name}_{file_counter:04d}{ext}'

    return f'diary/{new_filename}'

class Page(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    address = models.TextField(verbose_name="Address", null=True, blank=True)
    page_date = models.DateField(verbose_name="Page date")
    picture = models.ImageField(upload_to=generate_filename, null=True, blank=True, verbose_name="Picture")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        picture = self.picture
        super().delete(*args, **kwargs)
        if picture:
            Path(picture.path).unlink(missing_ok=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old = Page.objects.get(pk=self.pk)
            if old and old.picture and old.picture != self.picture:
                Path(old.picture.path).unlink(missing_ok=True)
        super().save(*args, **kwargs)