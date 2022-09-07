from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, PostsForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from .models import Posts, Group, User, Comment, Follow


def index(request):
    post_list = Posts.objects.get_queryset().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/group_slug.html', {'page': page, 'paginator': paginator})


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect('/thank-you/')
        return render(request, 'posts/contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'posts/contact.html', {'form': form})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostsForm(request.POST, files=request.FILES or None)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')

        return render(request, 'posts/create_or_update_posts.html', {'form': form})
    form = PostsForm()
    return render(request, 'posts/create_or_update_posts.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    edit_post = get_object_or_404(Posts, pk=post_id)
    if edit_post.author == request.user:
        if request.method == "POST":
            form = PostsForm(request.POST, files=request.FILES or None, instance=edit_post)
            if form.is_valid():
                form.save()
                return redirect("post", username, post_id)
        form = PostsForm(instance=edit_post)
        return render(
            request,
            "posts/create_or_update_posts.html",
            {
                "form": form,
                "username": username,
                "post_id": post_id,
                "edit_post": edit_post
            }
        )
    return redirect("post", username, post_id)


# def post_edit(request, username, post_id):
#    profile = get_object_or_404(User, username=username)
#    post = get_object_or_404(Posts, pk=post_id, author=profile)
#    if request.user != profile:
#        return redirect('post', username=username, post_id=post_id)
#    # добавим в form свойство files
#    form = PostsForm(request.POST or None, files=request.FILES , instance=post)
#
#    if request.method == 'POST':
#        if form.is_valid():
#            form.save()
#            return redirect("post", username=request.user.username, post_id=post_id)
#
#    return render(
#        request, 'posts/create_or_update_posts.html', {'form': form, 'post': post},
#    )

def profile(request, username):
    user_req = get_object_or_404(User, username=username)
    post_list = user_req.posts.get_queryset().order_by('id')
    followers_author = user_req.following.all()
    check_follower = []
    follow = False
    for aut in followers_author:
        author = aut.user
        check_follower.append(author)
    if request.user in check_follower:
        follow = True
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    follower = Follow.objects.filter(author=user_req).count()
    following = Follow.objects.filter(user=user_req).count()
    return render(request, 'posts/profile.html',
                  {'user_req': user_req, 'page': page, 'paginator': paginator,
                   'follower': follower, 'following': following, 'follow': follow})


def post_view(request, username, post_id):
    user_req = get_object_or_404(User, username=username)
    post = get_object_or_404(Posts, pk=post_id)
    context = {'user_req': user_req, 'post': post}
    return render(request, 'posts/post.html', context)


@login_required
def add_comment(request, username, post_id):
    user_req = get_object_or_404(User, username=username)
    post = get_object_or_404(Posts, pk=post_id)
    comments = post.comments.all()
    paginator = Paginator(comments, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            form.save()
            return redirect('post', username, post_id)
        return render(
            request,
            'posts/post.html',
            {
                'user_req': user_req,
                'post': post,
                'form': form,
                # 'comments': comments,
                'page': page,
                'paginator': paginator,
            }
        )
    form = CommentForm()
    return render(
        request,
        "posts/post.html",
        {
            "user_req": user_req,
            "post": post,
            "form": form,
            # "comments": comments,
            'page': page,
            'paginator': paginator,

        }
    )


# def add_comment(request, username, post_id ):
#    post = get_object_or_404(Posts, author=username, pk=post_id)
#    form = CommentForm(request.POST or None)
#    comments = post.comments.all()
#    print(comments)
#    if form.is_valid():
#        form.save()
#        return redirect ('post', username=username, post_id=post_id,)
#    return render(request, 'posts/post.html', {'form': form, 'comments': comments})


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def follow_index(request):
    fav_posts = Posts.objects.filter(author__following__user=request.user)
    context = {'posts': fav_posts, 'title': 'Избранные авторы'}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    if user == author:
        return redirect('profile', username)
    follow = Follow.objects.filter(author=author, user=user)
    if len(follow) > 0:
        return redirect('profile', username)
    Follow.objects.create(user=user, author=author)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(author=author, user=user)
    follow.delete()
    return redirect('profile', username)
