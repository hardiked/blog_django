from rest_framework.generics import CreateAPIView,DestroyAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from django.db.models import Q

from comments.models import Comment
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly
	)
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostPageNumberPagination,PostLimitOffsetPagination
from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)
from .serializers import CommentSerializer,CommentDetailSerializer

# class PostCreateAPIView(CreateAPIView):
# 	queryset=Post.objects.all()
# 	serializer_class=PostCreateSerializer
# 	permission_classes=[IsAuthenticated]
#
# 	def perform_create(self,serializer):
# 		serializer.save(user=self.request.user)

class CommentListAPIView(ListAPIView):
	serializer_class=CommentSerializer
	pagination_class=PostPageNumberPagination

	def get_queryset(self,*args,**kwargs):
		queryset_list=Comment.objects.all()
		query=self.request.GET.get("q")
		if query:
			queryset_list=queryset_list.filter(
				Q(content__icontains=query)
				).distinct()
		return queryset_list

class CommentDetailAPIView(RetrieveAPIView):
	queryset=Comment.objects.all()
	serializer_class=CommentDetailSerializer

# class PostDeleteAPIView(DestroyAPIView):
# 	queryset=Post.objects.all()
# 	serializer_class=PostSerializer

# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset=Post.objects.all()
# 	serializer_class=PostSerializer
# 	permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#
# 	def perform_update  (self,serializer):
# 		serializer.save(user=self.request.user)
