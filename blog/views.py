from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list (request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail (request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True).order_by('-created_at')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_at = timezone.now() # w/o this line, post will be saved as draft, not published
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_at = timezone.now() # w/o this line, post will be saved as draft, not published
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    post.save() # not in tutorial
    return redirect('post_detail', pk=pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def comment_list (request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'post': post, 'comment': comment})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def approved_comments(self):
    approved = post.comments.filter(approved_comment=True)
    comments_count = 0
    for i in approved:
        comments_count +=1
    return comments_count



