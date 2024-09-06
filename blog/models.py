from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()



class Category(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Post(models.Model):
  user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='post_author')
  img = models.ImageField(upload_to='blog/display_images')
  title = models.CharField(max_length=150)
  slug = models.SlugField(blank=True, null=True, unique=True)
  body = models.TextField()
  created =  models.DateTimeField(auto_now=True)
  updated = models.DateTimeField(auto_now_add=True)
  bookmark = models.ManyToManyField(User, related_name='user_bookmark', blank=True)
  category =  models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

  class Meta:
    ordering = ['-created']
    
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    super(Post, self).save(*args, **kwargs)
  
  def __str__(self) -> str:
    return f"{self.title} by {self.user.username} on the {self.created}"


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comment_author')
  body = models.CharField(max_length=150)
  created = models.DateTimeField(auto_now=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')

  def __str__(self):
    return f"Comment '{self.body}' by {self.user.username} on {self.post.title}"

