from rest_framework import serializers
from user_account.models import Account
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from blog.models import Post, Comment, Category
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = Account
    fields = ["email", "username"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)

    # Add custom claims (e.g., user's name)
    data['username'] = self.user.username
    data['email'] = self.user.email

    return data
    

class CategorySerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Category
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())
  post = serializers.PrimaryKeyRelatedField(read_only=True)
  
  class Meta:
    model = Comment
    fields = '__all__'
  
class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  comments = CommentSerializer(many=True, read_only=True, source='post_comment')  
  
  class Meta:
    model = Post
    fields = ['id', 'user', 'created', 'title', 'img','body','slug', 'bookmark', 'category', 'comments']

  def to_representation(self, instance):
    # Get the default representation
    representation = super().to_representation(instance)
    
    # Convert and format the 'created' field
    created_str = representation.get('created')
    representation['bookmark'] = len(representation['bookmark'])


    if created_str:
      datetime_obj = datetime.strptime(created_str, '%Y-%m-%dT%H:%M:%S.%fZ')
      representation['created'] = datetime_obj.strftime('%B %d, %Y')
  
    return representation

class PostOnlySerializer(serializers.ModelSerializer):
   class Meta:
    model = Post
    fields = ['id', 'title', 'user', 'slug','img', 'body', 'category']




class CreateAccountSerializer(serializers.ModelSerializer):

  password = serializers.CharField(write_only=True, style={'input_type': 'password'})
  confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})


  class Meta:
    model = Account
    fields = ["email", "username","password", "confirm_password"]
  
  def validate(self, data):
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
      raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
    
    try:
      validate_password(password)
    except ValidationError as e:
      raise serializers.ValidationError({"password": e.messages})
    
    return data
  
  def create(self, validated_data):
    password = validated_data.pop('confirm_password')
    account =  Account(**validated_data)
    account.set_password(password)
    account.save()
    return account
  


