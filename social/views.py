from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from msilib.schema import ListView
from multiprocessing import context
from django import views
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import PostForm,CommentForm
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from social.models import Comment, Post,UserProfile

# Create your views here.
#class Index(View):
#    def get(self,request,*args,**kwargs):
#        return render(request , 'social/index.html')


class PostListView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            creator__profile__followers__in =[logged_in_user.id]
        ).order_by('-posted_on')
        form = PostForm()

        context = {
            'post_list' : posts,
            'form' : form,
        }
        return render (request, 'social/postlist.html',context)
        
    def post(self,request,*args,**kwargs):
        posts = Post.objects.all().order_by('-posted_on')
        form = PostForm(request.POST)
        if form.is_valid():
            new_post= form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
        
        context = {
            'post_list' : posts,
            'form' : form,           
        }
        return render (request, 'social/postlist.html',context)    
        
class PostAddView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            creator__profile__followers__in =[logged_in_user.id]
        ).order_by('-posted_on')
        form = PostForm()

        context = {
            'post_list' : posts,
            'form' : form,
        }
        return render (request, 'social/postadd.html',context)

    def post(self,request,*args,**kwargs):
        posts = Post.objects.all().order_by('-posted_on')
        form = PostForm(request.POST)
        if form.is_valid():
            new_post= form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
        
        context = {
            'post_list' : posts,
            'form' : form,           
        }
        return render (request, 'social/postadd.html',context)  

class PostDetailView(LoginRequiredMixin,View):
    def get(self, request , pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter( post= post).order_by('-created_on')
        context = {
            'post':post,
            'form':form,
            'comments': comments,
        }
        return render(request, 'social/post_detail.html',context)

    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk = pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter( post= post).order_by('-created_on')
        context = {
            'post' : post,
            'form' : form,         
            'comments': comments,  
        }
        return render (request, 'social/post_detail.html',context)

class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['caption']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail',kwargs = {'pk' : pk}) 
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    fields = '__all__'
    template_name= 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    fields = '__all__'
    template_name= 'social/comment_delete.html'
    
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail',kwargs = {'pk' : pk})  
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author    


class ProfileView(View):
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk = pk)
        user = profile.user
        posts = Post.objects.filter(creator = user).order_by('-posted_on')
        followers = profile.followers.all()
        pfp = ""
        try:
            pfp = profile.profile_pic.url
        except ValueError:
            pfp =""

        if len(followers)== 0:
            is_following=False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False 


        no_of_followers = len(followers)

        context = {
            'user': user,
            'profile' : profile,
            'posts' : posts,
            'no_of_followers' : no_of_followers,
            'is_following': is_following,
            'pfp': pfp,
        }
        return render(request,'social/profile.html',context)

class ProfileEditView(UpdateView):
    model = UserProfile
    fields = '__all__'
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile',kwargs= {'pk':pk})

    def test_func(self):
        profile =self.get_object()
        return self.request.user == profile.user

class AddFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile',pk = profile.pk)

class RemoveFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile',pk = profile.pk)

class AddLike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk = pk)

        is_dislike =False

        for dislike in post.dislikes.all():
            if dislike == request.user :
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
        
        if is_dislike:
            post.dislikes.remove(request.user)
            print("Like removed")

        is_like =False

        for like in post.likes.all():
            if like == request.user :
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)
            print("Liked added")
            
        if is_like:
            post.likes.remove(request.user)
            print("Like rmeoved")

        next= request.POST.get('next','/')
        print("Bakchodi")
        return HttpResponseRedirect(next)

class DisLike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk = pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user :
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
        
        if is_like:
            post.likes.remove(request.user)
            print("Like removed")

        is_dislike =False

        for dislike in post.dislikes.all():
            if dislike == request.user :
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
            print("Disliked")
        if is_dislike:
            post.dislikes.remove(request.user)
            print("Liked")

        next= request.POST.get('next','/')
        print("Hey")
        return  HttpResponseRedirect(next)