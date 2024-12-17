from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, create=False, **kwargs):
    if create:
        Token.objects.create(user=instance)


class AdditionalInfo(models.Model):
    MOVIE_TYPES = {
        (0, 'Unnown'),
        (1, 'Sci-Fi'),
        (2, 'Drama'),
        (3, 'Thriller'),
        (4, 'Comedy'),
    }

    duration = models.IntegerField()
    type = models.IntegerField(choices=MOVIE_TYPES, default=0)

class Movie(models.Model):
    title = models.CharField(max_length=32)
    movie_description = models.TextField(max_length=255, null=True, blank=True )
    premiere = models.BooleanField(default=False)
    premiere_date = models.DateField(null=True, blank=True)
    year = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits=4,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)

    additional_info = models.OneToOneField(AdditionalInfo, on_delete=CASCADE, null=True, blank=True)
    def __str__(self):
        return self.str_description()

    def str_description(self):
        return f"{self.title} ({self.year})"

class Review(models.Model):
    review_description = models.TextField(max_length=255, default='')
    rating = models.PositiveSmallIntegerField(default=10)
    movie = models.ForeignKey(Movie, on_delete=CASCADE, related_name='reviews')