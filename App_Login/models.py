from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    """
        _Summary_: Tạo Entity UserProfile gồm các thuộc tính cần có của một UserProfile:
                        + profile_picture(type=ImageField): hình ảnh của profile user
                        + user : một User Model sẽ có một UserProfile, mối quan hệ One User - One UserProfile,
                        để CASCADE delete để khi xóa một User sẽ xóa luôn UserProfile

        Args:
            models (_type_): _Class UserProfile kế thừa models.Model của thư viện Django_
            
    """      

    # File sẽ được upload đến đường dẫn media/profile_picture
    profile_picture = models.ImageField(upload_to='profile_picture')

    # Thêm cascade để khi xóa user sẽ xóa hết các profile_picture liên quan
    user = models.OneToOneField(User, on_delete = models.CASCADE,related_name='user_profile')