from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe #6.4
from django.utils.text import slugify
from markdown_deux import markdown #6.2

from .utils import get_read_time # atb 20

# import tagging
# from tagging.fields import TagField

# Create your models here.


""" class Author(models.Model):
	name = models.CharField(max_lenght=50)
	bio = models.TextField()
	email = models.EmailField(unique=True)


class Category(models.Model):
	title = models.CharField(max_length=100, db_index=True)
	# slug = models.SlugField(max_length=100, db_index=True)

	def __unicode__(self):
		return '%s' % self.title

	#@permalink
	#def get_absolute_url(self):
	#	return ('view_blog_category', None, { 'slug': self.slug })
"""

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())




def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length = 200)
	slug = models.SlugField(max_length = 300, unique=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field="height_field", width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	read_time = models.IntegerField(default=0) # atb 20 assume minutes
	created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
	# author = models.CharField(max_length = 50)
	# categories = models.ManyToManyField(Category)
	# tags = TagField()
	
	objects = PostManager()

	def __unicode__(self):
		return '%s' % self.title

	def get_absolute_url(self):
		return reverse("blog:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-created_date", "-updated_date"]

	def get_markdown(self): # 6.3
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)





def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	if instance.content:
		html_string = instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var



pre_save.connect(pre_save_post_receiver, sender=Post)

	#@permalink
	#def get_absolute_url(self):
	#	return ('view_blog_post', None, { 'slug': self.slug })

