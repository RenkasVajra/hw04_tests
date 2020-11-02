from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.checks.messages import Error
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import PostForm
from .models import Group, Post


User = get_user_model()

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'posts':posts,
                                          'group': group,
                                          'page': page, 
                                          'paginator': paginator
    })

def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number)
    return render(
         request,
         'index.html',
         {'page': page, 
          'paginator': paginator}
    )

@login_required
def new_post(request):

    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'new.html',
                     {'form': form,
                     'is_new':True
    }) 

    post = form.save(commit=False)
    post.author = request.user
    post.save()
      
    return redirect('index')

def profile(request, username):

    author = get_object_or_404(User, username=username)
    if author is None:
        return redirect('signup')
 
    post_list = author.posts.all()
    post_count = post_list.count()
    paginator = Paginator(post_list, 10)
    post_latest = post_list.latest('pub_date')
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number)
    context = {"author": author,
                 "post_latest":post_latest,
                 "post_count":post_count,
                 "page":page,
                 "paginator":paginator}
    return render(request, 
                  'profile.html',
                   context
    )
def profile(request, username):
    author = get_object_or_404(User, username=username)
    authors_posts = author.posts.all()
    paginator = Paginator(authors_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'posts': authors_posts, "page": page,
                   "paginator": paginator, "author": author})
    
def post_view(request, username, post_id):
    post = get_object_or_404(Post,author__username=username,pk=post_id,)
    author = post.author
    return render(request, 'post.html', {'post': post,
                                        'author': author   
    })

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return render(request,'post.html',{'username':username,
                                           'post_id':post.pk,
                                           'post': post,
    })
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            
            form.save()
            return redirect(reverse('post', 
                                    kwargs={
                                    'username':username,
                                    'post_id':post.pk,
                                    
    }))
    else:
        form = PostForm(instance=post)
    return render(request, "new.html", {'form': form, 
                                        'instance':post,
                                        'is_new':False,
    })
