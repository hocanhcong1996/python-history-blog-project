from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.custom_forms import RegisterForm,UpdateUserProfileForm
# Create your views here.
def register_user(request):
    '''
    API cho người dùng giao tiếp với giao điện trang đăng ký
            Input:
                -Case 1: Request của client vào trang đăng ký
                
                -Case 2: Request của client mang phương thức POST có thông tin 
                username password để tạo tài khoản
            
            Output:
                -For Case 1: Một form đăng ký RegisterForm trống có username password 
                của thư viện Django được trả ra cho giao diện để người dùng nhập vào
                
                -For Case 2: Form đăng ký đã được điền đầy đủ thông tin để lưu thông tin 
                User vào database, nếu thông tin được lưu thành công thì trả ra giao diện 
                thông báo đã đăng ký thành công
    '''
    register_form = RegisterForm()
    is_registered = False
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            is_registered = True
    
    form_model = {'register_form':register_form,'is_registered':is_registered}
    return render(request,'App_Login/register.html',context=form_model)
    
def login_page(request):
    '''
    API cho người dùng giao tiếp với giao điện trang đăng nhập
            Input:
                -Case 1: Request của client vào trang đăng nhập
                
                -Case 2: Request của client mang phương thức POST có thông tin 
                username password từ Authentication Form để verify xem đăng ký 
                tài khoản chưa trước khi cấp quyền vào trang index
            
            Output:
                -For Case 1: Một form đăng nhập Authentication Form trống có username password 
                của thư viện Django được trả ra cho giao diện để người dùng nhập vào
                
                -For Case 2: Form đăng nhập đã được điền đầy đủ thông tin để verify 
                thông tin user, nếu thông tin user được verify là có tồn tại thì sẽ điều hướng vào trang index
                còn nếu thông tin user sai thì sẽ quay lại trang login
    '''
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None: 
                login(request,user)
                return HttpResponseRedirect(reverse('index'))                                   
    return render(request,'App_Login/login.html',context={'login_form':login_form})     

@login_required
def logout_user(request):
    '''
    API cho người thoát tài khoản ra khỏi website
            Input:
                - Request từ Client muốn thoát tài khoản
            
            Output:
                - Điều hướng về trang login
    '''
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))

@login_required
def show_profile_user(request):
    '''
    API cho người xem user profile
            Input:
                - Request từ Client xem thông tin tài khoản
            
            Output:
                - Returns trang user-profile với thông tin của user đó
    '''
    
    # The currently logged-in user and their permissions are made available in the template context when you use RequestContext.
    # When rendering a template RequestContext, the currently logged-in user, either a User instance or an AnonymousUser instance, is stored in the template variable {{ user }}:
    return render(request,'App_Login/user-profile.html',context={})

@login_required
def update_user_profile(request):
    '''
    API cho người dùng giao tiếp với trang cập nhật thông tin tài khoản
            Input:
                -Case 1: Request của client muốn vào trang chỉnh sửa thông tin cá nhân của họ
                
                -Case 2: Request của client mang phương thức POST mang thông tin đã được chỉnh sửa
                từ profile xuống để verify trước khi lưu thay đổi xuống database
            
            Output:
                -For Case 1: Trả về giao diện Form với các thông tin của current_logged_user 
                được lấy ra từ session truy xuất thông qua phương thức request.user
                
                -For Case 2: Nếu form chứa thông tin đã được user thay đổi là:
                    + Hợp lệ: Lưu các thông tin thay đổi này xuống database và trả về giao diện 
                    thông tin tài khoản mới được thay đổi
                    + Không hợp lệ: Trả lại kết quả như case 1
                
    '''
    
    # Django uses sessions and middleware to hook the authentication system into request objects.
    # These provide a request.user attribute on every request which represents the current user.
    current_user = request.user
    form = UpdateUserProfileForm(instance = current_user)
    if request.method == 'POST':
        form = UpdateUserProfileForm(request.POST,instance = current_user)
        if form.is_valid():
            form.save()
            form = UpdateUserProfileForm(instance = current_user) 
    return render(request,'App_Login/update-user-profile.html',context={'form':form})

@login_required
def change_password(request):
    '''
    API cho người dùng giao tiếp với trang thay đổi password
            Input:
                -Case 1: Request của client muốn vào trang chỉnh sửa password
                
                -Case 2: Request của client mang phương thức POST mang thông tin password được chỉnh sửa
                xuống để verify trước khi lưu thay đổi xuống database
            
            Output:
                -For Case 1: Trả về giao diện Form với các thông tin old_password, new_password, confirm_password
                để user thay đổi nhập vào
                                                
                -For Case 2: Nếu form chứa password cũ, mới đã được user thay đổi là:
                    + Hợp lệ: Lưu thông tin password thay đổi này xuống database và trả về giao diện 
                    password tài khoản mới được thay đổi
                    + Không hợp lệ: Trả lại kết quả như case 1
                
    '''
    current_user = request.user
    form = PasswordChangeForm(current_user)
    is_password_changed = False
    if request.method == 'POST':
        # form = PasswordChangeForm(request.POST,instance=current_user)
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            is_password_changed = True
    
    return render(request,'App_Login/change-password.html',context={'form':form, "is_password_changed":is_password_changed})
        
    