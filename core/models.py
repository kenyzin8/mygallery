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
    title = models.CharField(max_length=200, blank=True, help_text="Type N/A if you don't want to add a title.")
    image = models.ImageField(upload_to='public/images/', blank=True, null=True, help_text="Leave blank if you want to upload a video.")
    video = models.FileField(upload_to='public/images/', blank=True, null=True, help_text="Leave blank if you want to upload an image.")
    video_thumbnail = models.ImageField(upload_to='public/images/', blank=True, null=True, help_text="The size of the thumbnail should be similar to the video size.")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, blank=True, help_text="Optional description for the image only.")

    thumbnail = models.ImageField(upload_to='public/images/', blank=True)

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Select a category for the image or video.")

    image_height = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            with self.image.open() as image_file:
                pil_image = PilImage.open(image_file)

                self.image_width, self.image_height = pil_image.size
                original_width, original_height = pil_image.size

                new_width = int(original_width * 0.50)
                new_height = int(original_height * 0.50)

                pil_image = pil_image.resize((new_width, new_height), PilImage.Resampling.LANCZOS)

                thumb_io = BytesIO()
                pil_image.save(thumb_io, format='JPEG', quality=50)
                thumb_io.seek(0)

                thumb_file = ContentFile(thumb_io.getvalue())
                thumb_filename = f'thumb-{self.image.name.split("/")[-1]}'

                self.thumbnail.save(thumb_filename, thumb_file, save=False)

        if self.video:
            with self.video_thumbnail.open() as image_file:
                pil_image = PilImage.open(image_file)

                self.image_width, self.image_height = pil_image.size
                original_width, original_height = pil_image.size

                new_width = int(original_width * 0.50)
                new_height = int(original_height * 0.50)

                pil_image = pil_image.resize((new_width, new_height), PilImage.Resampling.LANCZOS)

                thumb_io = BytesIO()
                pil_image.save(thumb_io, format='JPEG', quality=20)
                thumb_io.seek(0)

                thumb_file = ContentFile(thumb_io.getvalue())
                thumb_filename = f'thumb-{self.video_thumbnail.name.split("/")[-1]}'

                self.video_thumbnail.save(thumb_filename, thumb_file, save=False)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Contents (Images and Videos)'

class ImageView(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=128, blank=True, null=True) 
    ip_address = models.CharField(max_length=40, blank=True, null=True) 
    view_date = models.DateTimeField(auto_now_add=True)

class HelpIconContent(models.Model):
    content = models.TextField(max_length=1500, blank=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        verbose_name_plural = 'Help Icon Content'

class GridColumns(models.Model):
    number_of_columns = models.IntegerField()

    def __str__(self):
        return str(self.number_of_columns)

    class Meta:
        verbose_name_plural = 'Grid Columns'