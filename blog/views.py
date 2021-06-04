from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from django.utils import timezone
from django.http import Http404
from .forms import PostForm


def post_list(request):
  qs = Post.objects.all()
  qs = qs.filter(published_date__lte=timezone.now())
  qs = qs.order_by('published_date')

  return render(request, 'blog/post_list.html', {
    'post_list': qs,
  } )

def post_detail(request, pk):
  #try:
  #  post = Post.objects.get(pk=pk)
  #except Post.DoesNotExist:
  #  raise Http404

  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/post_detail.html', {
    'post': post,
  } )  

# @login_required
def post_new(request):
  # request.POST, request.FILES
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      #post.published_date = timezone.now()
      post.save()
      return redirect('post_detail', pk=post.pk)

  # GET
  else:
    form = PostForm()

  return render(request, 'blog/post_edit.html', {
      'form': form,
  } ) 


def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)

  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      #post.published_date = timezone.now()
      post.save()
      return redirect('post_detail', pk=post.pk)

  # GET
  else:
    form = PostForm(instance=post)

  return render(request, 'blog/post_edit.html', {
    'form': form,
  } )  


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
