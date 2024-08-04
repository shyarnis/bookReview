import os
from django.conf import settings
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import Book, Review
from books.forms import ReviewForm


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="pass#1933")

        self.book = Book.objects.create(
            title="Karnali Blues",
            author="Buddhi Sagar",
            summary="The novel depicts the father-son relationship in a family from the Mid-western region of Nepal.",
            category="Fiction",
            image=SimpleUploadedFile(
                name="karnali_blues.jpg", content=b"", content_type="image/jpeg"
            ),
            book_url="https://www.goodreads.com/author/show/6997657.Buddhisagar",
        )

        self.review = Review.objects.create(
            text="Amazing Book!",
            user=self.user,
            book=self.book,
            rating=5,
            will_recommend=True,
        )

    def test_home_view(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home_page.html")
        self.assertContains(
            response, "Karnali Blues"
        )  # response should contain book title

    def test_detail_view(self):
        response = self.client.get(reverse("detail", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "detail.html")
        self.assertContains(response, "Karnali Blues")
        self.assertContains(response, "Amazing Book!")

    def test_create_review_GET(self):
        # @login_required for create_review
        self.client.login(username="testuser", password="pass#1933")

        response = self.client.get(reverse("create_review", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_review.html")
        self.assertIsInstance(response.context["form"], ReviewForm)

    def test_create_review_POST_success(self):
        self.client.login(username="testuser", password="pass#1933")
        review_data = {"text": "Good to read", "rating": 4, "will_recommend": True}

        response = self.client.get(
            reverse("create_review", args=[self.book.id]), review_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_review.html")

    def test_create_review_POST_error(self):
        self.client.login(username="testuser", password="pass#1933")
        review_data = {"text": "", "rating": 8, "will_recommend": True}

        response = self.client.get(
            reverse("create_review", args=[self.book.id]), review_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_review.html")

    def test_update_review_GET(self):
        self.client.login(username="testuser", password="pass#1933")
        response = self.client.get(reverse("update_review", args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_review.html")
        self.assertIsInstance(response.context["form"], ReviewForm)

    def test_update_review_POST_success(self):
        self.client.login(username="testuser", password="pass#1933")
        updated_review = {"text": "Amazing", "rating": 5, "will_recommend": True}

        response = self.client.get(
            reverse("create_review", args=[self.book.id]), updated_review
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_review.html")
        self.review.refresh_from_db()
        self.assertEqual(self.review.text, "Amazing Book!")

    def test_update_review_POST_error(self):
        self.client.login(username="testuser", password="12345")
        updated_review = {"text": "", "rating": 8, "will_recommend": "True"}
        response = self.client.post(
            reverse("update_review", args=[self.review.id]), updated_review
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_review(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("delete_review", args=[self.review.id]))
        self.assertEqual(response.status_code, 302)

    def test_login_required(self):
        # Test that login is required for create_review, update_review, and delete_review
        create_url = reverse("create_review", args=[self.book.id])
        update_url = reverse("update_review", args=[self.review.id])
        delete_url = reverse("delete_review", args=[self.review.id])

        for url in [create_url, update_url, delete_url]:
            response = self.client.get(url)
            self.assertRedirects(response, f"/account/login/?next={url}")

    def test_user_can_only_edit_own_review(self):
        other_user = User.objects.create_user(username="otheruser", password="12345")
        self.client.login(username="otheruser", password="12345")

        response = self.client.get(reverse("update_review", args=[self.review.id]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse("delete_review", args=[self.review.id]))
        self.assertEqual(response.status_code, 404)

    # Delete the image file created during the setUp()
    def tearDown(self):
        if self.book.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.book.image.name)

            if os.path.exists(image_path):
                os.remove(image_path)
