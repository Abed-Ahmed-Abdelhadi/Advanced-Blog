from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

def blog_list(request, tag_slug=None):
    blog_list = Post.POSPublished.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        blog_list = blog_list.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(blog_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        blog_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        blog_list = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        blog_list = paginator.page(paginator.num_pages)

    context = {'blog_list':blog_list, 'tag': tag}
    return render(request,'blog/blog_list.html', context)


def blog_detail(request, slug, year, month, day):
    blog_detail = get_object_or_404(Post,
                                    POSSlug=slug,
                                    POSStatus=Post.Status.PUBLISHED,
                                    POSPublish__year=year,
                                    POSPublish__month=month,
                                    POSPublish__day=day)
    # List of active comments for this post
    comments = blog_detail.comments.filter(COMActive=True)
    # Form for users to comment
    form = CommentForm()
    # List of similar posts
    post_tags_ids = blog_detail.tags.values_list('id', flat=True)
    similar_posts = Post.POSPublished.filter(tags__in=post_tags_ids).exclude(id=blog_detail.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-POSPublish')[:4]

    context = {'blog_detail':blog_detail, 'comments': comments, 'form': form,'similar_posts': similar_posts}
    return render(request, 'blog/blog_detail.html', context)

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, POSStatus=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.POSTitle}"
            message = f"Read {post.POSTitle} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'abed.ahmed.abdelhadi@gmail.com',[cd['to']])
            sent = True
            # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, POSStatus=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.COMPost = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/comment.html',{'post': post,'form': form,'comment': comment})

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # 1 - Stemming and ranking results
            search_vector = SearchVector('POSTitle', 'POSBody')
            search_query = SearchQuery(query)

            # 2 - Stemming and removing stop words in different languages
            # search_vector = SearchVector('title', 'body', config='spanish')
            # search_query = SearchQuery(query, config='spanish')

            # 3 - Weighting queries
            #search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            #search_query = SearchQuery(query)
            #results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
            
            results = Post.POSPublished.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            # 4 - Searching with trigram similarity
            #results = Post.published.annotate(similarity=TrigramSimilarity('POSTitle', query),).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(request, 'blog/search.html', {'form': form, 'query': query, 'results': results})