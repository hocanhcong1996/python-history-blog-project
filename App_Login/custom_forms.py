from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    '''
    Custom lại form register từ UserCreationForm có sẵn của thư viện Django

            Input:
                    Kế thừa UserCreationForm của thư viện Django đã có sẵn trường username, password1, password2

            Output:
                    Returns: một form đăng ký mới sẽ có các trường username, password1, password2 và thêm một trường email
    '''
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        # Chọn field muốn hiển thị ra ngoài màn hình
        fields = ('username','email','password1','password2')
    
class UpdateUserProfileForm(UserChangeForm):
    '''
    Mục đích: 
    Custom lại form User Profile từ UserChangeForm có sẵn của thư viện Django

            Input:
                    Kế thừa UserChangeForm của thư viện Django
                    
            Output:
                    Returns: một form profile mới sẽ có các trường username, email, password, last_name, first_name
    ''' 
    class Meta:
        model = User
        # Chọn field muốn hiển thị ra ngoài màn hình
        fields = ('username','email','password','last_name','first_name')