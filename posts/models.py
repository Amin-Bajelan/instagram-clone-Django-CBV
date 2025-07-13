from django.db import models
from accounts.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=False, null=False)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    caption = models.TextField(max_length=200, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.likes} "


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following_related", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_related', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"follow from :{self.follower} to {self.following} at {self.date_followed}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('follow', 'Follow'),
        ('comment', 'Comment'),
    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} → {self.to_user} [{self.notification_type}]"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # نویسنده کامنت
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # پست مربوطه
    text = models.TextField(max_length=500)  # متن کامنت
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # برای حذف منطقی یا فیلتر کردن

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"