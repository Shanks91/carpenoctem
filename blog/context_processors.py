from .models import Article


def drafts_processor(request):
    if request.user.is_authenticated():
        drafts = Article.objects.filter(publish=False).filter(author=request.user).count()
        return {'drafts': drafts}
    else:
        return {'drafts': None}
