from rest_framework.generics import CreateAPIView,DestroyAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from django.db.models import Q

from posts.models import Post
from .serializers import PostSerializer,PostCreateSerializer
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly
	)
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)
from .pagination import PostPageNumberPagination,PostLimitOffsetPagination

class PostCreateAPIView(CreateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostCreateSerializer
	permission_classes=[IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
	serializer_class=PostSerializer
	pagination_class=PostPageNumberPagination

	def get_queryset(self,*args,**kwargs):
		queryset_list=Post.objects.all()
		query=self.request.GET.get("q")
		if query:
			queryset_list=queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query)
				).distinct()
		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset=Post.objects.all()
	serializer_class=PostSerializer

class PostDeleteAPIView(DestroyAPIView):
	queryset=Post.objects.all()
	serializer_class=PostSerializer

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset=Post.objects.all()
	serializer_class=PostSerializer
	permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

	def perform_update  (self,serializer):
		serializer.save(user=self.request.user)
