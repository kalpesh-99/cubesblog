from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from blog.models import Post



class PostCreateUpdateSerializer(ModelSerializer):
	class Meta: 
		model = Post
		fields = [
			'title',
			'content',
			'publish',
		]


post_detail_url = HyperlinkedIdentityField(  # for links to post via api, to be used in multiple places 
		view_name='blog-api:detail',
		lookup_field='slug'
		)


class PostListSerializer(ModelSerializer):
	url = post_detail_url
	user = SerializerMethodField()

	class Meta: 
		model = Post
		fields = [
			'url',
			'user',
			'title',
			'content',
			'created_date',
		]
	def get_user(self, obj):
		return str(obj.user.username)


class PostDetailSerializer(ModelSerializer):
	url = post_detail_url
	user = SerializerMethodField()
	image = SerializerMethodField()
	html = SerializerMethodField()

	class Meta: 
		model = Post
		fields = [
			'url',
			'user',
			'id',
			'title',
			'slug',
			'content',
			'html',
			'created_date',
			'image',
		]

	def get_html(self, obj):
		return obj.get_markdown()

	def get_user(self, obj):
		return str(obj.user.username)	

	def get_image(self, obj):
		try:
			image = obj.image.url
		except: 
			image = None
		return image

