from rest_framework.serializers import EmailField,CharField,SerializerMethodField,HyperlinkedIdentityField,ModelSerializer,ValidationError
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.db.models import Q

User=get_user_model()

class UserCreateSerializer(ModelSerializer):
    email=EmailField(label="Email")
    email2=EmailField(label="Confirm Email")
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs={"password":
                          {"write_only":True}
                      }

    def validate(self,data):
        email=data["email"]
        user_qs=User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("User already exists")
        return data

    def validate_email(self,value):
        data=self.get_initial()
        email1=data.get("email")
        email2=data.get("email2")
        print(data)
        print(email1)
        print(email2)
        if email1 != email2:
            raise ValidationError("Email does not match")
        return value

    def create(self,validated_data):
        username=validated_data['username']
        email=validated_data['email']
        password=validated_data['password']
        user_obj=User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token=CharField(allow_blank=True,read_only=True)
    username=CharField(required=False,allow_blank=True)
    email=EmailField(label="Email")
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs={"password":
                          {"write_only":True}
                      }

    def validate(self,data):
        user_obj=None
        email=data.get("email",None)
        username=data.get("username",None)
        password=data.get("password")
        if not email or not username:
            raise ValidationError("A username and email required to login")
        user=User.objects.filter(
            Q(email=email)|
            Q(username=username)
        ).distinct()
        if user.exists() and user.count()==1:
            user_obj=user.first()
        else:
            raise ValidationError("This username/email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")
        data["token"]="SOME RANDOM TOKEN"
        return data