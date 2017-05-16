from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Ngo(models.Model):
    name = models.CharField(max_length=300)
    moderator = models.OneToOneField(User)
    address = models.CharField(max_length=500, default='Vadodara')
    contact_no = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default='Children')
    web_url = models.URLField(default='web link')
    email = models.EmailField(default='name@emample.com')
    logo = models.ImageField(upload_to='logos/', null=True)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    rating = models.FloatField(default=0.0)
    likes = models.ManyToManyField(User, related_name='liked_by', blank=True)
    bio = models.TextField(null=True)
    logo_list = ImageSpecField(source='logo',
                                  processors=[ResizeToFill(223, 150)],
                                  format='JPEG',
                                  options={'quality': 60})

    def __str__(self):
        return self.name

    def rate(self):
        self.rating += 1
        self.save()

    def get_live_id(self):
        return self.pk

    def calculate_ratings(self):
        five_star_count = NgoRatings.objects.filter(ngo=self).filter(rating=5).count()
        four_star_count = NgoRatings.objects.filter(ngo=self).filter(rating=4).count()
        three_star_count = NgoRatings.objects.filter(ngo=self).filter(rating=3).count()
        two_star_count = NgoRatings.objects.filter(ngo=self).filter(rating=2).count()
        one_star_count = NgoRatings.objects.filter(ngo=self).filter(rating=1).count()

        sum_star = five_star_count + four_star_count + three_star_count + two_star_count + one_star_count

        a = 5 * five_star_count
        b = 4 * four_star_count
        c = 3 * three_star_count
        d = 2 * two_star_count
        e = one_star_count

        ratings = (a + b + c + d + e) / sum_star

        self.rating = ratings
        self.save()

    def get_round_ratings(self):
        rating_rounded = round(self.rating, 2)
        return rating_rounded


class Happening(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Ngo, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='thumbs_up_by')

    def get_ngo_key(self):
        return self.author.id

    def user_liked(self, user):
        if user in self.likes.all():
            return True
        else:
            return False


class Gallery(models.Model):
    photo = models.ImageField(upload_to='gallery/')
    owner = models.ForeignKey(Ngo, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True, blank=True)


class HapComments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_on = models.ForeignKey(Happening, on_delete=models.CASCADE, related_name='comment_of')
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now=True, blank=True)


class NgoRatings(models.Model):
    ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE, related_name='ratings_of')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_by')
    rating = models.IntegerField()
