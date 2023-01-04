from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, DeleteView
from App_Blog.models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from App_Blog.custom_forms import CommentForm
from unidecode import unidecode
import re
# Create your views here.

def list_all_blog(request):
    return render(request, 'App_Blog/blog_list.html',context={})

class BlogList(ListView):
    """_summary_: xây dựng Class BlogList để generate tất cả các blogs đã được viết
    
    Args:
        ListView (_type_): Từ thư viện Django chứa phương thức as_view() mang context_object_name variable (là cải tiến của object_list được query set dưới DB)
        đưa vào model là Blog và render ra giao diện blog_list.html
    """    

    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'

# LoginRequiredMixin chặn users chưa logged in truy cập vào form để Blog này. 
# Nếu bỏ sót bước này, cần phải xử lý users chưa được cấp quyền trong form_valid()
class BlogCreation(LoginRequiredMixin, CreateView):
    """_summary_: Tạo BlogCreation Class kế thừa Class LoginRequiredMixin và Class Create View

    Args:
        LoginRequiredMixin (_type_): Thư viện Django
        CreateView (_type_): Thư viện Django

    Returns:
        Output:
            + Blog Creation bao gồm model là tất cả các thuộc tính trong Blog. 
            Tuy nhiên ta chỉ custom hiển thị ra views các trường để tạo blog bao gồm: blog_title, blog_content, blog_image
    """    

    model = Blog
    template_name = 'App_Blog/write_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')
    
    def form_valid(self, form):
        # form.save(commit=False) lấy ra một model object chưa được commit, vì vậy chúng ta có thể add thêm data vào model này sau đó mới save xuống database
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        # Xử lý slug 
        # blog_obj.slug = unidecode(blog_obj.blog_title.replace(' ','-'))
        blog_obj.slug = re.sub('[^A-Za-z0-9]+', '', unidecode(blog_obj.blog_title.replace(' ','-')))
        if blog_obj.slug == '':
            blog_obj.slug = 'anonymous'
        list_blog_obj = Blog.objects.all()
        is_duplicate_title = False
        count_duplicate_title = 0
        for blog_obj_child in list_blog_obj:
            if blog_obj_child.blog_title == blog_obj.blog_title:
                is_duplicate_title = True
                count_duplicate_title += 1
        if is_duplicate_title and count_duplicate_title > 0:
            blog_obj.slug += '-ver-' + str(count_duplicate_title)
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))
    
    # def form_valid(self, form):
    #     # form.save(commit=False) lấy ra một model object chưa được commit, vì vậy chúng ta có thể add thêm data vào model này sau đó mới save xuống database
    #     blog_obj = form.save(commit=False)
    #     blog_obj.author = self.request.user
    #     blog_obj.slug = unidecode(blog_obj.blog_title.replace(' ','-'))
    #     blog_obj.save()
    #     return HttpResponseRedirect(reverse('index'))
        
def blog_details(request,slug):
    """_summary_: Chức năng xem chi tiết một bài viết blog

    Args:
        request (_type_): Request mang hoặc không mang phương thức POST
        slug (_type_): param chứa slug của bài viết

    Returns:
        Output:
            + Trường hợp Request không mang phương thức POST: render ra giao diện blog_details.html có sẵn một Comment Form
            
            + Trường hợp Request có mang phương thức POST: User để lại comment sẽ mang phương thức POST trong form 
            => Validate form, add user, blog chủ quản vào comment đó rồi save vào db. Tiếp theo là redirect lại trang details này.
    """    

    blog = Blog.objects.get(slug=slug)
    commentForm = CommentForm()
    is_LoggedIn = None
    is_Comment = None
    if request.user.is_authenticated:
        is_LoggedIn = True
    if request.method == 'POST':
        is_Comment = True
    if request.method == 'POST' and request.user.is_authenticated:
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':slug}))
            
    return render(request,'App_Blog/blog_details.html',context={'blog':blog,'comment_form':commentForm,'is_logged_in':is_LoggedIn,'is_comment':is_Comment})

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'

class UpdateBlog(LoginRequiredMixin, UpdateView):
    """_summary_: Xây dựng Class để edit một số field cụ thể của Blog 

    Args:
        LoginRequiredMixin (_type_): Thư viện Django
        UpdateView (_type_): Thư viện Django

    Returns:
        Trả về trang có bài viết đã được edit với nội dung mới
    """    

    model = Blog
    fields =('blog_title','blog_content','blog_image')
    template_name = 'App_Blog/edit_blog.html'   
    
    # get_success_url(): Determine the URL to redirect to when the form is successfully validated. Returns success_url by default.
    # https://docs.djangoproject.com/en/4.1/ref/class-based-views/mixins-editing/
    def get_success_url(self,**kwargs):
        #reverse_lazy() https://docs.djangoproject.com/en/4.1/ref/urlresolvers/
        return reverse_lazy('App_Blog:blog_details',kwargs={'slug':self.object.slug})