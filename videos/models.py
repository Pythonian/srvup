from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from .utils import get_vid_for_direction


class VideoQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True)

	def has_embed(self):
		return self.filter(embed_code__isnull=False).exclude(embed_code__exact="")


class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQuerySet(self.model, using=self._db)

	def get_featured(self):
		return self.get_queryset().active().featured()

	def all(self):
		return self.get_queryset().active().has_embed()


DEFAULT_MESSAGE = "Check out this awesome video."

'''

from analytics.models import PageView
from videos.models import Video
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType


#top items
 PageView.objects.filter(primary_content_type=video_type)\
 .values("primary_object_id")\
 .annotate(the_count=Count("primary_object_id"))\
 .order_by("-the_count")


# one item
PageView.objects.filter(primary_content_type=video_type, primary_object_id=21).count()

'''


class Video(models.Model):
	title = models.CharField(max_length=120)
	embed_code = models.CharField(max_length=500, null=True, blank=True)
	share_message = models.TextField(default=DEFAULT_MESSAGE)
	order = models.PositiveIntegerField(default=1)
	tags = GenericRelation("TaggedItem", null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	free_preview = models.BooleanField(default=False)
	category = models.ForeignKey("Category", default=1, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	objects = VideoManager()

	class Meta:
		unique_together = ('slug', 'category')
		ordering = ['order', '-timestamp']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("video_detail", kwargs={"vid_slug": self.slug, "cat_slug": self.category.slug})

	def get_share_link(self):
		full_url = "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
		return full_url

	def get_share_message(self):
		full_url = "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
		return "%s %s" %(self.share_message, full_url)

	def get_next_url(self):
		video = get_vid_for_direction(self, "next")
		if video is not None:
			return video.get_absolute_url()
		return None

	def get_previous_url(self):
		video = get_vid_for_direction(self, "previous")
		if video is not None:
			return video.get_absolute_url()
		return None
	
	@property 
	def has_preview(self):
		if self.free_preview:
			return True
		return False


def video_post_save_receiver(sender, instance, created, *args, **kwargs):
	if created:
		slug_title = slugify(instance.title)
		new_slug = "%s %s %s" % (instance.title, instance.category.slug, instance.id)
		try:
			obj_exists = Video.objects.get(slug=slug_title, category=instance.category)
			instance.slug = slugify(new_slug)
			instance.save()
		except Video.DoesNotExist:
			instance.slug = slug_title
			instance.save()
		except Video.MultipleObjectsReturned:
			instance.slug = slugify(new_slug)
			instance.save()
		except:
			pass

post_save.connect(video_post_save_receiver, sender=Video)


class CategoryQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True)


class CategoryManager(models.Manager):
	def get_queryset(self):
		return CategoryQuerySet(self.model, using=self._db)

	def get_featured(self):
		return self.get_queryset().active().featured()

	def all(self):
		return self.get_queryset().active()


class Category(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(max_length=5000, null=True, blank=True)
	tags = GenericRelation("TaggedItem", null=True, blank=True)
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	slug = models.SlugField(default='abc', unique=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	objects = CategoryManager()

	class Meta:
		ordering = ['title', 'timestamp']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("project_detail", kwargs={"cat_slug": self.slug})

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)


TAG_CHOICES = (
	("python", "python"),
	("django", "django"),
	("css", "css"),
	("bootstrap", "bootstrap"))


class TaggedItem(models.Model):
	tag = models.SlugField(choices=TAG_CHOICES)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	def __str__(self):
		return self.tag
