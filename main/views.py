from main import models
from . import forms
from django.contrib import messages
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate
import logging
logger = logging.getLogger(__name__)


class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(models.ProductTag, slug=tag)
        if self.tag:
            print(self.tag)
            products = models.Product.objects.active().filter(tags=self.tag)
            print(products)
        else:
            products = models.Product.objects.active()
        return products.order_by("name")

class SignupView(FormView):
    template_name = 'main/signup.html'
    form_class = forms.UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        logger.info(
            "New signup for email=%s through SignupView", email
        )
        logger.debug(
            "New signup for email=%s through SignupView", email
        )
        print(logger)
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)

        messages.info(
            self.request, "You signed up successfully."
        )
        return response

