from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        verbose_name = "artiste"

class Contact(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name = "prospect"

class Album(models.Model):
    reference = models.IntegerField('référence',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField()
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)
    class Meta:
        verbose_name = "disque"
class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "réservation"