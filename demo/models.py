from django.db import models

import uuid
import os


LOGFILE_DIR = os.path.join(__file__, "logs/")


class Person(models.Model):
    """Simplest possible model utilizing one field."""

    name = models.CharField(max_length=255)


class Country(models.Model):
    """Alternative Autofield test."""

    country_id = models.SmallAutoField(primary_key=True)
    country_code = models.CharField()


class Recipe(models.Model):
    """Moderately complex model utilizing the most common fields.

    Tests the following fields:
      - AutoField
      - BooleanField
      - CharField
      - DateField
      - DateTimeField
      - DecimalField
      - EmailField
      - FloatField
      - IntegerField
      - TextField
      - TimeField
    """

    id = models.AutoField(primary_key=True)

    archived = models.BooleanField(blank=False)

    name = models.CharField(max_length=255, blank=False)
    author = models.EmailField(blank=False)

    created_date = models.DateField(auto_now_add=True, blank=False)
    created_time = models.TimeField(auto_now_add=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False)

    ingredients_cost = models.DecimalField(max_digits=5, decimal_places=2)
    ingredients_weight = models.FloatField()
    ingredients_count = models.IntegerField()
    instructions = models.TextField()


# Models with foreign relations
class Library(models.Model):
    address = models.CharField()


class Author(models.Model):
    name = models.CharField(unique=True)


class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    libraries = models.ManyToManyField(Library)


class BenchmarkResults(models.Model):
    """Model utilizing lesser used specialty fields.

    Tests the following fields:
      - BigAutoField
      - BigIntegerField
      - BinaryField
      - DurationField
      - FileField
      - FileField and FieldFile
      - FilePathField
      - GenericIPAddressField
      - ImageField
      - JSONField
      - PositiveBigIntegerField
      - PositiveIntegerField
      - PositiveSmallIntegerField
      - SlugField
      - SmallIntegerField
      - URLField
      - UUIDField

    Does NOT test:
      -  SmallAutoField (models cannot have multiple AutoFields)
    """

    benchmark_id = models.BigAutoField(primary_key=True)
    checksum = models.BinaryField()

    runtime = models.DurationField(blank=False)
    seed = models.BigIntegerField(blank=False)

    log = models.FileField(upload_to=LOGFILE_DIR)
    log_path = models.FilePathField(path=LOGFILE_DIR)

    uploader_ip = models.GenericIPAddressField()
    uploader_avatar = models.ImageField()
    uploader_website = models.URLField()
    configuration = models.JSONField()

    runtime_nanoseconds = models.PositiveBigIntegerField()
    runtime_milliseconds = models.PositiveIntegerField()
    runtime_seconds = models.PositiveSmallIntegerField()
    runtime_hours = models.SmallIntegerField()

    slug = models.SlugField()

    uuid = models.UUIDField(default=uuid.uuid4)
