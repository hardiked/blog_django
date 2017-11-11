from rest_framework.serializers import SerializerMethodField,HyperlinkedIdentityField,ModelSerializer,ValidationError

from comments.models import Comment
from django.contrib.contenttypes.models import  ContentType


def create_comment_serializer(model_type='post',object_id=None,parent_id=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model=Comment
            fields=[
                'id',
                'parent',
                'content',
            ]
    def __init__(self,*args,**kwargs):
        self.model_type=model_type
        self.object_id=object_id
        self.parent_obj=None
        if self.parent_id:
            parent_qs=Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count==1:
                self.parent_obj=parent_qs.first()
        return super(CommentCreateSerializer,self).__init__(*args,**kwargs)

    def validate(self,data):
        model_type=self.model_type
        model_qs=ContentType.objects.filter(model=model_type)
        if not model_qs.exists() or model_qs.count()!=1:
            raise ValidationError("Not a valid content type")
        someModel=model_qs.first().model_class()
        obj_qs=someModel.objects.filter(id=self.object_id)
        return data

    return CommentCreateSerializer

class CommentSerializer(ModelSerializer):
    reply_count=SerializerMethodField()
    class Meta:
        model=Comment
        fields=[
            'id',
			'content_type',
			'object_id',
			'parent',
            'reply_count',
            'content',
		]
    def get_reply_count(self,obj):
        if obj.is_parent:
            return obj.children().count()
        else:
            return 0

class CommentChildSerializer(ModelSerializer):
	class Meta:
		model=Comment
		fields=[
            'id',
            'content',
            'timestamp'
		]

class CommentDetailSerializer(ModelSerializer):
    replies=SerializerMethodField()
    class Meta:
        model=Comment
        fields=[
            'id',
            'content_type',
            'object_id',
            'content',
            'timestamp',
            'replies',
        ]
    def get_replies(self,obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(),many=True).data
        return  None