import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django_extensions.db.fields import AutoSlugField


class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from="name")
    slug = models.SlugField(max_length=200, unique=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
