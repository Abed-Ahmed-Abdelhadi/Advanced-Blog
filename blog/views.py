from django.shortcuts import render, get_object_or_404
from .models import Post

def blog_list(request):
    blog_list = Post.POSPublished.all()
    context = {'blog_list':blog_list}
    return render(request,'blog/blog_list.html', context)

def blog_detail(request, slug):
    blog_detail = get_object_or_404(Post,POSSlug=slug,POSStatus=Post.Status.PUBLISHED)
    context = {'blog_detail':blog_detail}
    return render(request, 'blog/blog_detail.html', context)