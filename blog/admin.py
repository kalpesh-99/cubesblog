from django.contrib import admin

# Register your models here.
from .models import Post
# from .models import Category

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "created_date", "updated_date"]
	list_filter = ["created_date", "updated_date"]
	search_fields = ['title', "content"]
	class Meta:
		model = Post


admin.site.register(Post, PostModelAdmin)
# admin.site.register(Category)