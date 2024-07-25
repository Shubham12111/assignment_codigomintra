from django.shortcuts import render
from .models import Blog
from nltk.stem import SnowballStemmer
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from .forms import EmailPostForm

# Create your views here.
def blog_list(request):
    tag = request.GET.get('tag', None)
    if tag:
        blogs = Blog.objects.filter(tags__name__in=[tag])
    else:
        blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def blog_search_rank(request):
    query = request.GET.get('query')
    stemmer = SnowballStemmer('english')
    if query:
        stemmed_query = ' '.join([stemmer.stem(word) for word in query.split()])
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(stemmed_query)
        blogs = Blog.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
    else:
        blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def blog_search_similarity(request):
    query = request.GET.get('query')
    stemmer = SnowballStemmer('english')
    if query:
        stemmed_query = ' '.join([stemmer.stem(word) for word in query.split()])
        blogs = Blog.objects.annotate(
            similarity=TrigramSimilarity('title', stemmed_query) + TrigramSimilarity('body', stemmed_query)
        ).filter(similarity__gt=0.3).order_by('-similarity')
    else:
        blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})



def share_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            blog_url = request.build_absolute_uri(blog.get_absolute_url())
            subject = f"{cd['name']} recommends you read {blog.title}"
            message = f"Read {blog.title} at {blog_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_email@example.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share_blog.html', {'blog': blog, 'form': form, 'sent': sent})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})  