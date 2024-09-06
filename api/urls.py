from django.urls import path
from .views import PostSearchAPIView, PopularPostsView,CreateAccountAPIView, PostCreateAPIVew, PostAPIView, CommentCreateAPIView, BookmarkAPIView, UserBookmarks, CategoryAPIView

urlpatterns = [
  path('create-account/', CreateAccountAPIView.as_view(), name='create-account'),
  path('posts/search/', PostSearchAPIView.as_view(), name='post_search'),
  path('post/create/', PostCreateAPIVew.as_view()),
  path('posts/', PostAPIView.as_view()),
  path('popular/posts/', PopularPostsView.as_view()),
  path('post/<str:slug>/', PostAPIView.as_view()),
  path('post/category/<str:category>/', CategoryAPIView.as_view()),
  path('comment/create/<str:slug>/', CommentCreateAPIView.as_view()),
  path('bookmark/post/<str:slug>/', BookmarkAPIView.as_view()),
  path('my/bookmarks/', UserBookmarks.as_view()),
]