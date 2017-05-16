from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ordinem.models import Ngo
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True,)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default='Male')
    photo = models.FileField(blank=True, null=True, upload_to='profile/')
    city = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(null=True, blank=True)
    follows = models.ManyToManyField(Ngo, blank=True)
    photo_avatar = ImageSpecField(source='photo',
                                  processors=[ResizeToFill(64, 64)],
                                  format='JPEG',
                                  options={'quality': 60})

    def __str__(self):
        return self.user.username

    def is_user_following(self, ngo):
        if ngo in self.follows.all():
            return True
        else:
            return False

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()
