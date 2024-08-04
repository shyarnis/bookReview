from django.test import TestCase
from books.forms import ReviewForm


class ReviewFormTestCase(TestCase):

    def test_form_labels(self):
        form = ReviewForm()
        self.assertEqual(form.fields["text"].label, "Text")
        self.assertEqual(form.fields["rating"].label, "Rating")
        self.assertEqual(form.fields["will_recommend"].label, "Will Recommend")

    def test_form_widgets(self):
        form = ReviewForm()
        # Check widget attributes for 'text' field.
        self.assertEqual(form.fields["text"].widget.attrs["class"], "form-control")
        self.assertEqual(
            form.fields["text"].widget.attrs["placeholder"], "Write your review..."
        )
        self.assertEqual(form.fields["text"].widget.attrs["rows"], 4)

        # Check widget attributes for 'rating' field.
        self.assertEqual(form.fields["rating"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["rating"].widget.attrs["min"], 0)
        self.assertEqual(form.fields["rating"].widget.attrs["max"], 5)

        # Check widget attributes for 'will_recommend' field
        self.assertEqual(
            form.fields["will_recommend"].widget.attrs["class"], "form-check-input"
        )

    # Fill the form with valid data.
    def test_form_valid_data(self):
        form_data = {"text": "Awesome Book!!!", "rating": 5, "will_recommend": True}
        form = ReviewForm(data=form_data)
        review = form.save(commit=False)

        self.assertTrue(form.is_valid())
        self.assertEqual(review.text, "Awesome Book!!!")
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.will_recommend)

    # Fill the form with invalid data.
    def test_form_invalid_data_1(self):
        form_data = {
            "text": "",  # invalid text
            "rating": 1,
            "will_recommend": False,
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_data_2(self):
        form_data = {
            "text": "Great",
            "rating": 6,  # invalid rating
            "will_recommend": True,
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
