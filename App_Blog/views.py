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
# Create your views here.

def list_all_blog(request):
    return render(request, 'App_Blog/blog_list.html',context={})

class BlogList(ListView):
    '''
        Input:
            + Tạo BlogList Class kế thừa Class ListView để hiển thị một list các objects
        Output:
            + Trả ra một context_object_name variable (là cải tiến của object_list được query set dưới DB)
            đưa vào model là Blog và render ra giao diện blog_list.html
    '''
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'

# LoginRequiredMixin chặn users chưa logged in truy cập vào form để Blog này. 
# Nếu bỏ sót bước này, cần phải xử lý users chưa được cấp quyền trong form_valid()
class BlogCreation(LoginRequiredMixin, CreateView):
    '''
        Input:
            + Tạo BlogCreation Class kế thừa Class LoginRequiredMixin và Class Create View
        Output:
            + Blog Creation bao gồm model là tất cả các thuộc tính trong Blog. 
            Tuy nhiên ta chỉ custom hiển thị ra views các trường để tạo blog bao gồm: blog_title, blog_content, blog_image
    '''
    model = Blog
    template_name = 'App_Blog/write_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')
    
    def form_valid(self, form):
        # form.save(commit=False) lấy ra một model object chưa được commit, vì vậy chúng ta có thể add thêm data vào model này sau đó mới save xuống database
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.slug = blog_obj.blog_title.replace(' ','-')
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))
        
def blog_details(request,slug):
    '''
        Input:
            + Request truy cập trang blog details
            + Slug để biết truy cập vào bài viết cụ thể nào
        Output:
            + Trường hợp 1: User mới chỉ truy cập đến trang Web 
            => render ra giao diện blog_details.html có sẵn một comment form
            
            + Trường hợp 2: User để lại comment sẽ mang phương thức POST trong form 
            => Validate form, add user, blog chủ quản vào comment đó rồi save vào db. Tiếp theo là redirect lại trang details này.
    '''
    blog = Blog.objects.get(slug=slug)
    commentForm = CommentForm()
    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':slug}))
            
    return render(request,'App_Blog/blog_details.html',context={'blog':blog,'comment_form':commentForm})

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'

class UpdateBlog(LoginRequiredMixin, UpdateView):
    '''
        Input:
            + Viết CLass UpdateBlog kế thừa LoginRequiredMixin và Class UpdateView
            bao gồm model form là Blog Entity cho chỉnh sửa các field của Blog như
            blog_title, blog_content, blog_image
        Output:
            + Nếu thay đổi thông tin của Blog entity thành công thì sẽ trả về lại trang blog_details
            của blog đang chỉnh sửa với thông tin mới được cập nhật
    '''
    model = Blog
    fields =('blog_title','blog_content','blog_image')
    template_name = 'App_Blog/edit_blog.html'   
    
    # get_success_url(): Determine the URL to redirect to when the form is successfully validated. Returns success_url by default.
    # https://docs.djangoproject.com/en/4.1/ref/class-based-views/mixins-editing/
    def get_success_url(self,**kwargs):
        #reverse_lazy() https://docs.djangoproject.com/en/4.1/ref/urlresolvers/
        return reverse_lazy('App_Blog:blog_details',kwargs={'slug':self.object.slug})