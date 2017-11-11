from rest_framework.serializers import SerializerMethodField,HyperlinkedIdentityField,ModelSerializer

from posts.models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment


class PostSerializer(ModelSerializer):
	url=HyperlinkedIdentityField(
		view_name='posts-api:detail',
		)
	user=SerializerMethodField()
	image=SerializerMethodField()
	markdown=SerializerMethodField()
	delete_url=HyperlinkedIdentityField(
		view_name='posts-api:delete',
		)
	comments=SerializerMethodField()
	class Meta:
		model=Post
		fields=[
			'url',
			'user',
			'title',
			'content',
			'markdown',
			'image',
			'comments',
			'delete_url',
		]

	def get_comments(self,obj):
		c_qs=Comment.objects.filter_by_instance(obj)
		comments=CommentSerializer(c_qs,many=True).data
		return comments

	def get_user(self,obj):# get_x here x must be the anme we defined above here we get useer so get_user
		return str(obj.user.username)

	def get_image(self,obj):
		try:
			image=obj.image.url
		except:
			image=None
		return image

	def get_markdown(self,obj):
		return obj.get_markdown()

class PostCreateSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			'title',
			'content',
			'publish'
		]