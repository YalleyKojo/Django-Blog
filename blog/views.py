from django.shortcuts import render,get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views.generic.base import View

from .models import  Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentForm

# Create your views here.
def home(request):
    cont={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',cont)

def about(request):
    return render(request,'blog/about.html',{'title':"About"})   



class PostListView(LoginRequiredMixin,ListView):
    model=Post
    template_name='blog/home.html' 
    context_object_name='posts'  
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(LoginRequiredMixin,ListView):
    model=Post
    template_name='blog/user_post.html'
    context_object_name='posts'  
    
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin,View):

     def get(self,request,pk,*args,**kwargs):
         post=Post.objects.get(pk=pk)
         form=CommentForm()
         comments=Comment.objects.filter(post=post).order_by('-date_posted')   
         context={
            'post':post,
            'form':form,
            'comments':comments
         }
         return render(request,'blog/Post_detail.html',context)
     def post(self,request,pk,*args,**kwargs):
         post=Post.objects.get(pk=pk)
         form=CommentForm(request.POST)

         if form.is_valid():
             new_comment=form.save(commit=False)
             new_comment.author=request.user
             new_comment.post=post
             new_comment.save()

         comments=Comment.objects.filter(post=post).order_by('-date_posted')     
         context={
            'post':post,
            'form':form,
            'comments':comments
         }
         return render(request,'blog/Post_detail.html',context)     

         
    
        
class PostCreateView(LoginRequiredMixin,CreateView):
     model=Post
     fields=['title','image','content',] 


     def form_valid(self, form):
         form.instance.author=self.request.user  
         return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
     model=Post
     fields=['title','image','content'] 


     def form_valid(self, form):
         form.instance.author=self.request.user  
         return super().form_valid(form)         

     def test_func(self):     
        post=self.get_object()
        if self.request.user==post.author:
            return True
             
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post 
    success_url='/'
    def test_func(self):     
        post=self.get_object()
        if self.request.user==post.author:
            return True            

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Comment
    template_name='blog/comment_delete.html'


    def get_success_url(self) :
        pk=self.kwargs['post_pk']
        return reverse_lazy('post-detail',kwargs={'pk':pk})
    def test_func(self):     
        post=self.get_object()
        if self.request.user==post.author:
            return True     

