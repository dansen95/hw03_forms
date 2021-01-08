from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .forms import PostForm, EditPostForm
from .models import Group, Post

User = get_user_model()

def index(request):
    post_list = Post.objects.select_related('group').order_by('-pub_date')
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10) 

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page') 

    # Получаем набор записей для страницы с запрошенным номером
    page = paginator.get_page(page_number) 
    return render(
         request,
         'posts/index.html',
         {'page': page,}
     ) 


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group).select_related('group').order_by('-pub_date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(request, 'group.html', {'group': group, 'page': page})



def profile(request, username): 
    author = User.objects.get(username=username)
    post_list = author.posts.all()
    #author = get_object_or_404(Post, username=author)
    #post_list = author.objects.select_related('author').order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'author': author,
        'paginator': paginator.count,
    }
    return render(request, 'profile.html', context)
        #return render(request, 'profile.html', {})
 
 
def post_view(request, username, post_id):
        author = User.objects.get(username=username)
        post = get_object_or_404(Post, id=post_id, author=author)
        #post = Post.objects.filter(author=author).filter(id=post_id).order_by('-pub_date')
        #post = Post.objects.get(id=post_id)
        count = Post.objects.filter(author=author).select_related('author').count()
        return render(request, 'post.html', {'post': post, 'author': author, 'count': count})


@login_required
def post_edit(request, username, post_id):    
    user = User.objects.filter(username=username)[0]
    #post = Post.objects.filter(id=post_id).filter(author=user)[0]
    post = get_object_or_404(Post, id=post_id, author=user)
    if user != request.user:
        return redirect('post', username=user, post_id=post_id)
    form = PostForm(request.POST or None, 
        initial={
            'text': post.text,
            'group': post.group,
        }
    )
    if form  == request.GET or not form.is_valid():
        return render(
            request, 
            'posts/new_post.html',
            {                
                'form': form,
                'button': 'Редактировать',
                'group': post,
            }
        )           
    form = PostForm(request.POST, instance=post)
    form.save()
    return redirect('post', username=user, post_id=post_id)


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('index')

        return render(request, 'posts/new_post.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/new_post.html', {'form': form})
