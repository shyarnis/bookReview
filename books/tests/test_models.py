import os
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from books.models import Book, Review


class BookTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="1984",
            author="George Orwell",
            summary="This is a sample summary of the book.",
            category="Classic",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
            book_url="https://www.google.com/",
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "1984")
        self.assertEqual(self.book.author, "George Orwell")
        self.assertEqual(self.book.summary, "This is a sample summary of the book.")
        self.assertEqual(self.book.category, "Classic")
        self.assertTrue(self.book.image.name.startswith("books/test_image"))
        self.assertTrue(self.book.image.name.endswith(".jpg"))
        self.assertEqual(self.book.book_url, "https://www.google.com/")

    def test_book_str_method(self):
        self.assertEqual(str(self.book), self.book.title)

    # Delete the image file created during the setUp()
    def tearDown(self):
        if self.book.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.book.image.name)

            if os.path.exists(image_path):
                os.remove(image_path)


class ReviewTestCase(TestCase):

    def setUp(self):
        # "Review" model has ForeignKey with "User" model.
        self.user = User.objects.create(username="testuser", password="Password#123")

        # "Review" model has ForeignKey with "Book" model.
        self.book = Book.objects.create(
            title="Animal Farm",
            author="George Orwell",
            summary="This is a sample summary of the book.",
            category="Classic",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
            book_url="https://www.google.com/",
        )

        self.review = Review.objects.create(
            text="Great Book!!",
            user=self.user,
            book=self.book,
            rating=5,
            will_recommend=True,
        )

    def test_review_creation(self):
        self.assertEqual(self.review.text, "Great Book!!")
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.will_recommend, True)

    def test_review_str_method(self):
        self.assertEqual(str(self.review), self.review.text)

    # Delete the image file created during the setUp()
    def tearDown(self):
        if self.book.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.book.image.name)

            if os.path.exists(image_path):
                os.remove(image_path)
