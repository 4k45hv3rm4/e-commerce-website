from django.test import TestCase
from decimal import Decimal

from django.urls import reverse

from main import models

# Create your tests here.
class Testpage(TestCase):
    def test_home_page_works(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Home.html")
        print(response)
        self.assertContains(response, 'BookTime')
    def test_about_us_page_works(self):
        response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_us.html")
        print(response)
        self.assertContains(response, 'About us')


class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Product.objects.create(name="The Cathedral and the bazaar", price=Decimal("10.00"))
        models.Product.objects.create(name="Pride and Prejudice", price = Decimal("2.00"))
        models.Product.objects.create(name="A Tale of Two Cities", price=Decimal("2.00"), active=False)
        self.assertEqual(len(models.Product.objects.active()), 2)



class TestPage(TestCase):

    def test_products_page_returns_active(self):
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.0"),
        )
        models.Product.objects.create(
            name="A Tale of Two Cities",
            slug='tale-two-cities',
            price=Decimal("2.00"),
            active=False
        )
        response = self.client.get(reverse('products', kwargs={'tag':'all'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")
        product_list = models.Product.objects.active().order_by("name")
        self.assertEqual(list(response.context["object_list"]),
                         list(product_list),
        )
    def test_products_page_filters_by_tags_and_active(self):
        cb = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00")
        )
        cb.tags.create(name="Open source", slug="opensource")
        models.Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00")
        )
        response = self.client.get(
            reverse("products", kwargs={"tag": "opensource"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")
        product_list = (
            models.Product.objects.active()
            .filter(tags__slug='opensource')
            .order_by("name")
        )
        self.assertEqual(list(response.context['object_list']),
                         list(product_list),)