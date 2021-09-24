from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.views.generic.detail import DetailView
from . import models

urlpatterns = [
     path('product/<slug:slug>/', DetailView.as_view(model=models.Product), name="product"),
     path("about-us/", TemplateView.as_view(template_name="about_us.html")),
     path("", TemplateView.as_view(template_name="Home.html")),
     path('products/<slug:tag>/', views.ProductListView.as_view(), name="products"),
     path('signup/', views.SignupView.as_view(), name="signup")

]