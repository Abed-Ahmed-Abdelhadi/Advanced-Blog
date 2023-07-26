from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(POSStatus=Post.Status.PUBLISHED)

class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    POSTitle = models.CharField(max_length=250, verbose_name=_("Post Title"))
    POSSlug = models.SlugField(blank=True, null=True, verbose_name=_("Post Slug"))
    POSAuthor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    POSBody = models.TextField(verbose_name=_("Post Body"))
    POSPublish = models.DateTimeField(default=timezone.now, verbose_name=_("Publish  At"))
    POSCreated = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    POSUpdated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    POSStatus = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Post Status"))
    POSObjects = models.Manager() # The default manager.
    POSPublished = PublishedManager() # Our custom manager.

    def save(self, *args, **kwargs):
        if not self.POSSlug:
            self.POSSlug = slugify(self.POSTitle)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.POSTitle
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-POSPublish']
        indexes = [
            models.Index(fields=['-POSPublish']),
        ]