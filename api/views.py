from rest_framework import generics, filters
from rest_framework import views
from rest_framework import status
from user_account.models import Account
from rest_framework.response import Response
from .serializers import UserSerializer, CreateAccountSerializer, PostSerializer, CommentSerializer, PostOnlySerializer, CategorySerializer
from blog.models import Post, Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer

class ProfileAPIView(views.APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get(self, request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user)
    return  Response(serializer.data, status=status.HTTP_200_OK)



class CreateAccountAPIView(generics.CreateAPIView):

  serializer_class = CreateAccountSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      self.perform_create(serializer)
      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def perform_create(self, serializer):
    serializer.save()


class PostSearchAPIView(generics.ListAPIView):

  def get(self, request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(title__icontains=query) | Post.objects.filter(body__icontains=query) | Post.objects.filter(category__name__icontains=query)
    serializer = PostOnlySerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class PostCreateAPIVew(generics.CreateAPIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAPIView(generics.RetrieveUpdateDestroyAPIView):
  
  permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

  def get(self, request, slug=None):
    if slug:
      post = get_object_or_404(Post, slug=slug)
      serializer = PostSerializer(post)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      posts = Post.objects.all()
      serializer = PostOnlySerializer(posts, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
  def put(self, request, slug):
    post = get_object_or_404(Post, slug=slug)
    serializer = PostOnlySerializer(post, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, slug):
    post = get_object_or_404(Post, slug=slug)
    serializer = PostOnlySerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return Response(status=status.HTTP_200_OK)

class PopularPostsView(views.APIView):

  permission_classes = [IsAuthenticatedOrReadOnly]

  def get(self, request):
    posts = Post.objects.all()[:3]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class CommentCreateAPIView(generics.CreateAPIView):
  permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = CommentSerializer

  def perform_create(self, serializer):
    post = get_object_or_404(Post, slug=self.kwargs['slug'])
    serializer.save(user=self.request.user, post=post)
  
  def post(self, request, slug):
    post = get_object_or_404(Post, slug=slug)
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      print(serializer.errors)  # Print the errors for debugging
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkAPIView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post.bookmark.filter(id=request.user.id).exists():
      post.bookmark.remove(request.user)
    else:
      post.bookmark.add(request.user)
    return Response(status=status.HTTP_200_OK)
  
class UserBookmarks(views.APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    posts = Post.objects.filter(bookmark=request.user)
    serializer = PostOnlySerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class CategoryAPIView(views.APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
