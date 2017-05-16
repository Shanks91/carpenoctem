from django.db import models
from django.contrib.auth.models import User
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writen_by")
    title = models.CharField(max_length=400)
    content = models.TextField()
    pic = models.ImageField(upload_to='blog/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    pic_med = ImageSpecField(source='pic',
                               processors=[SmartResize(900, 300)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self):
        return self.title

    def publish_article(self):
        self.publish = True
        self.save()

    def get_article_id(self):
        return self.id

    def get_content_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)


class BlogComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_on = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)



