from django.urls import path
from . import views


urlpatterns = [

    # Main page
    path('', views.index, name='index'),
    path('400/', views.page_not_found, name='page_400'),
    path('500/', views.server_error, name='page_500'),

    # Group page
    path('group/<slug>', views.group_posts, name='slug'),

    # Contact page
    path('contact/', views.user_contact, name='contact'),

    # New page
    path('new/', views.new_post, name='new_post'),

    # Follow, unfollow
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),

    # User profile
    path('<str:username>/', views.profile, name='profile'),

    # Comments
    path("<username>/<int:post_id>/", views.add_comment, name="add_comment"), # убрал comment

    # Viewing a Recording
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),

]
