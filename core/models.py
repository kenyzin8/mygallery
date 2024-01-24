from django.db import models
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, blank=True)

    thumbnail = models.ImageField(upload_to='images/thumbnail/', blank=True)

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image_height = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pil_image = PilImage.open(self.image.path)

        self.image_width, self.image_height = pil_image.size

        thumb_io = BytesIO()

        pil_image.save(thumb_io, format='JPEG', quality=50) 

        thumb_file = ContentFile(thumb_io.getvalue(), name=f'thumb-{self.image.name}.jpeg')

        self.thumbnail.save(thumb_file.name, thumb_file, save=False)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Images'

class HelpIconContent(models.Model):
    content = models.TextField(max_length=1500, blank=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        verbose_name_plural = 'Help Icon Content'