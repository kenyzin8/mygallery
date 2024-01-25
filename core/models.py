from django.db import models
from django.core.files.base import ContentFile
from PIL import Image as PilImage
from io import BytesIO

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
    image = models.ImageField(upload_to='public/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, blank=True)

    thumbnail = models.ImageField(upload_to='public/images/', blank=True)

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image_height = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with self.image.open() as image_file:
            pil_image = PilImage.open(image_file)

            self.image_width, self.image_height = pil_image.size

            thumb_io = BytesIO()
            pil_image.save(thumb_io, format='JPEG', quality=50)  
            thumb_io.seek(0)  

            thumb_file = ContentFile(thumb_io.getvalue())
            thumb_filename = f'thumb-{self.image.name.split("/")[-1]}'

            self.thumbnail.save(thumb_filename, thumb_file, save=False)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Images'

class HelpIconContent(models.Model):
    content = models.TextField(max_length=1500, blank=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        verbose_name_plural = 'Help Icon Content'