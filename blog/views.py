from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, BlogComment
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required()
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
        else:
            return render(request, 'blog/articlecreate.html', {'form': form})
    else:
        form = ArticleForm()
        return render(request, 'blog/articlecreate.html', {'form': form})


def article_list(request):
    articles = Article.objects.filter(publish=True).order_by('-timestamp')
    return render(request, 'blog/articleslist.html', {'articles': articles})


@login_required()
def article_draft(request):
    articles = Article.objects.filter(publish=False)
    return render(request, 'blog/articledraft.html', {'articles': articles})


@login_required()
def article_publish(request, pk):
    article = get_object_or_404(Article, id=pk)
    article.publish_article()
    return redirect('article_draft')


@login_required()
def article_edit(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article2 = form.save(commit=False)
            article2.save()
            return redirect('article_detail', pk=pk)
        else:
            return render(request, 'blog/articlecreate.html', {'form': form})
    else:
        form = ArticleForm(instance=article)
        return render(request, 'blog/articlecreate.html', {'form': form})


def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    comments = BlogComment.objects.filter(comment_on=article)
    form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated():
            user = request.user
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = user
                comment.comment_on = article
                comment.save()
                return redirect('article_detail', pk=pk)
            else:
                return render(request, 'blog/articledetail.html', {'article': article, 'comments': comments, 'form': form})
        else:
            raise PermissionDenied
    return render(request, 'blog/articledetail.html', {'article': article, 'comments': comments, 'form': form})


def article_delete(request, pk):
    article = get_object_or_404(Article, id=pk)
    user = request.user
    if user == article.author:
        article.delete()
    else:
        raise PermissionDenied
    return redirect('article_list')
