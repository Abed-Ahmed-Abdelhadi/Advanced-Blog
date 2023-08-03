from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(POSStatus=Post.Status.PUBLISHED)

class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    POSTitle = models.CharField(max_length=250, verbose_name=_("Post Title"))
    POSSlug = models.SlugField(blank=True, null=True, unique_for_date='POSPublish', verbose_name=_("Post Slug"))
    POSAuthor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name=_("Author"))
    POSBody = models.TextField(verbose_name=_("Post Body"))
    POSPublish = models.DateTimeField(default=timezone.now, verbose_name=_("Publish  At"))
    POSCreated = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    POSUpdated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    POSStatus = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Post Status"))
    POSObjects = models.Manager() # The default manager.
    POSPublished = PublishedManager() # Our custom manager.

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:blog_detail',args=[self.POSPublish.year,
                                                self.POSPublish.month,
                                                self.POSPublish.day,
                                                self.POSSlug])

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

class Comment(models.Model):
    COMPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    COMName = models.CharField(max_length=80, verbose_name=_("Name"))
    COMEmail = models.EmailField(verbose_name=_("Email"))
    COMBody = models.TextField(verbose_name=_("Body"))
    COMCreated = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    COMUpdated = models.DateTimeField(auto_now=True, verbose_name=_("Update At"))
    COMActive = models.BooleanField(default=True, verbose_name=_("Comment Active"))
    class Meta:
        ordering = ['COMCreated']
        indexes = [
            models.Index(fields=['COMCreated']),
        ]
    def __str__(self):
        return f'Comment by {self.COMName} on {self.COMPost}'