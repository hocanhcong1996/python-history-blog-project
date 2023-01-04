from django import forms
from App_Blog.models import Blog, Comment

class CommentForm(forms.ModelForm):
    """_summary_: Tạo ra một comment form cho người dùng bình luận

    Args:
        forms (_type_): thư viện Django
    """    
    class Meta:
        model = Comment
        fields = ('comment',)