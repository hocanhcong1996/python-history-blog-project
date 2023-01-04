from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    """_summary_: Custom lại form register từ UserCreationForm có sẵn của thư viện Django

        Args:
            UserCreationForm (_type_): Kế thừa UserCreationForm của thư viện Django đã có sẵn trường username, password1, password2
            nên RegisterFrom sẽ có các trường trên và bổ sung thêm trường email
    """        

    email = forms.EmailField(required=True)
    class Meta:
        model = User
        # Chọn field muốn hiển thị ra ngoài màn hình
        fields = ('username','email','password1','password2')
    
class UpdateUserProfileForm(UserChangeForm):
    """_summary_: Custom lại form User Profile từ UserChangeForm có sẵn của thư viện Django

        Args:
            UserChangeForm (_type_): Kế thừa UserChangeForm của thư viện Django để xây dựng UpdateUserProfileForm
            có các trường username, email, password, last_name, first_name
    """        

    class Meta:
        model = User
        # Chọn field muốn hiển thị ra ngoài màn hình
        fields = ('username','email','password','last_name','first_name')