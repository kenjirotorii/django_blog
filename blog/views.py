from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse

import markdown

from .forms import FileUploadForm
from .models import Post

published_post = Post.objects.filter(is_public=True)
most_popular = published_post.order_by('-view_count')[0:3]
latest_post = published_post.order_by('-created_at')[0:3]


def get_object_count(object):
    object_name = object + '__name'
    queryset = published_post.values(object_name).annotate(Count(object_name))
    return queryset


popular_tag = get_object_count(
    object='tags').order_by('-tags__name__count')[0:10]


def get_paginatior(request, query_list, per_page):
    paginator = Paginator(query_list, per_page)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginatored_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginatored_queryset = paginator.page(1)
    except EmptyPage:
        paginatored_queryset = paginator.page(paginator.num_pages)

    return paginatored_queryset, page_request_var


def blog(request):

    queryset, page_request_var = get_paginatior(request, published_post, 8)

    context = {
        'queryset': queryset,
        'most_popular': most_popular,
        'latest_post': latest_post,
        'page_request_var': page_request_var,
        'popular_tag': popular_tag,
        'meta_discription': None,
    }

    return render(request, 'index.html', context)


def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.view_count += 1
    post.save()

    # previous post
    try:
        previous_post = post.get_previous_by_created_at()
    except Post.DoesNotExist:
        previous_post = None

    # next post
    try:
        next_post = post.get_next_by_created_at()
    except Post.DoesNotExist:
        next_post = None

    # markdown
    md = markdown.Markdown(
        extensions=[
            'extra',
            'toc',
        ],
    )
    md_content = md.convert(post.content)


    context = {
        'post': post,
        'most_popular': most_popular,
        'latest_post': latest_post,
        'popular_tag': popular_tag,
        'previous_post': previous_post,
        'next_post': next_post,
        'md_content': md_content,
        'meta_discription': post.overview,
    }

    return render(request, 'post.html', context)


def search(request):
    query = request.GET.get('q')
    if query:
        query_list = published_post.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    queryset, page_request_var = get_paginatior(request, query_list, 8)

    context = {
        'queryset': queryset,
        'popular_tag': popular_tag,
        'query': query,
        'most_popular': most_popular,
        'latest_post': latest_post,
        'search': True,
        'meta_discription': None,
    }

    return render(request, 'index.html', context)


def tag_search(request, name):

    post_list = published_post.filter(tags__name=name)
    queryset, page_request_var = get_paginatior(request, post_list, 8)

    context = {
        'queryset': queryset,
        'most_popular': most_popular,
        'latest_post': latest_post,
        'page_request_var': page_request_var,
        'popular_tag': popular_tag,
        'tag_name': name,
        'tag': True,
        'meta_discription': None,
    }

    return render(request, 'index.html', context)


def category_search(request, name):

    post_list = published_post.filter(categories__name=name)
    queryset, page_request_var = get_paginatior(request, post_list, 8)

    context = {
        'queryset': queryset,
        'most_popular': most_popular,
        'latest_post': latest_post,
        'page_request_var': page_request_var,
        'popular_tag': popular_tag,
        'cat_name': name,
        'category': True,
        'meta_discription': None,
    }

    return render(request, 'index.html', context)


def upload(request):
    """ファイルのアップロード用ビュー"""
    form = FileUploadForm(files=request.FILES)
    if form.is_valid():
        url = form.save()
        return JsonResponse({'url': url})
    return HttpResponseBadRequest()
