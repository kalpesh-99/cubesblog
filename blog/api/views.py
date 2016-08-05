from django.db.models import Q 

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView, 
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView
	)

# from rest_framework.pagination import ( ** commented b/c we created custom way **
# 	LimitOffsetPagination,
# 	PageNumberPagination,
# 	)

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)


from blog.models import Post

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from .serializers import (
	PostCreateUpdateSerializer,
	PostDetailSerializer,
	PostListSerializer
	)


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	# lookup_url_kwarg = "slug"


class PostDeletelAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	# lookup_url_kwarg = "slug"

	def perform_delete(self, serializer):
		serializer.save(user=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	# lookup_url_kwarg = "slug"

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)


class PostListAPIView(ListAPIView):
	# queryset = Post.objects.all() // no longer needed becuase of below queryset_list
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter, OrderingFilter]  # this is using built in search filters; so we get both search and q now
	search_fields = ['title', 'content', 'user__first_name']
	pagination_class = PostPageNumberPagination #PostLimitOffsetPagination (replaced to try pages), #LimitOffsetPagination *again b/c using custom now*

	def get_queryset(self, *args, **kwargs):
		# same as Post.objects.all() so no need for it queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q") # note class based view so we need "self".request
		if query:
			queryset_list = queryset_list.filter(
					Q(title__icontains=query)|
					Q(content__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					).distinct()
		return queryset_list




