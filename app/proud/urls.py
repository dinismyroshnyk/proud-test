from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="proud/index.html"), name="index"),
    path("admin/", views.index, name="index"),
    path("users/", views.users, name="users"),
    path("user/<uuid:user_id>/", views.user, name="user"),
    path("user/<uuid:user_id>/cancel/", views.user_cancel, name="user_cancel"),
    path("auth/login/", views.login, name="login"),
    path("members/", views.members, name="members"),
    path("member/<uuid:user_id>/", views.member, name="member"),
    path("member/<uuid:user_id>/reject/", views.member_reject, name="member_reject"),
    path("products/", views.products, name="products"),
    path("products/<int:product_id>/", views.product, name="product"),
    path('create-newsletter/', views.create_newsletter, name='create_newsletter'),

]


