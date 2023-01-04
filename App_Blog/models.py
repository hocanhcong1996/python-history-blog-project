from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    """_summary_: Tạo Entity Blog gồm các thuộc tính cần có của một blog

        Args:
            models (_type_): Kế thừa Model có sẵn từ thư viện Django
        Returns:
            Blog Entity có các thuộc tính: 
                + author : tác giả được tạo từ User Model có sẵn của Django đã được authenticate sẵn username và password
                + blog_title(type = Character, maximum_length =250)
                + created_date(type = DateTime): thời gian được set tại lần đầu add vào database
                + updated_date(type = DateTime): mỗi lần được update và lưu lại vào database thì trường này sẽ được set lại thời gian
                + blog_content(type = Text): nội dung của blog
                + blog_image(type = Image): khi người dùng chọn hình ảnh thì file ảnh sẽ được lưu vào đường dẫn /media/blog_picture của project
    """           
    author = models.ForeignKey(User, related_name='post_author',on_delete=models.CASCADE);
    blog_title = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    blog_content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_picture')

    # Bổ sung trường slug để hiển thị trên URL
    slug = models.SlugField(max_length=250, unique=True)
    
    class Meta:
            ordering = ['-created_date']
    
    def __str__(self):
        return self.blog_title
    
class Comment(models.Model):
    """_summary_: Tạo Entity Comment gồm các thuộc tính cần có của một Comment

        Args:
            models (_type_): Kế thừa Model có sẵn từ thư viện Django để xây dựng một Comment Entity có các thuộc tính:
                + blog : một blog sẽ chứa nhiều comment, mối quan hệ One Blog - Many Comments,
                để CASCADE delete để khi xóa một Blog sẽ xóa hết các Comments của Blog đó
                + user : một User Model sẽ bình luận nhiều comment, mối quan hệ One User - Many Comments,
                để CASCADE delete để khi xóa một User sẽ xóa hết các Comments của User đó
                + comment: nội dung của comment bao gồm một text field String
                + comment_Date(type=DateTimeField): khi comment được post thì trường DateTime sẽ auto được add tại thời điểm đó
            
    """        

    blog =  models.ForeignKey(Blog,on_delete=models.CASCADE, related_name="blog_comment")
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            ordering = ['-comment_date']    

class Likes(models.Model):
    """_summary_: Tạo Entity Like gồm các thuộc tính cần có của một Like

        Args:
            models (_type_): Kế thừa Model có sẵn từ thư viện Django xây dựng Like Entity có các thuộc tính:
                        + blog : một blog sẽ chứa nhiều likes, mối quan hệ One Blog - Many Likes,
                        để CASCADE delete để khi xóa một Blog sẽ xóa hết các Likes của Blog đó
                        + user : một User Model sẽ để lại nhiều lượt Likes, mối quan hệ One User - Many Likes,
                        để CASCADE delete để khi xóa một User sẽ xóa hết các lượt Likes của User đó
            
    """        

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="liked_blog")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="liker_user")