from django.forms import ModelForm
from django.forms import Textarea, NumberInput, CheckboxInput
from books.models import Review


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.fields["text"].label = "Text"
        self.fields["rating"].label = "Rating"
        self.fields["will_recommend"].label = "Will Recommend"

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        # Special case for checkbox input
        self.fields["will_recommend"].widget.attrs.update({"class": "form-check-input"})

    class Meta:
        model = Review
        fields = ["text", "rating", "will_recommend"]

        # Widgets to apply Bootstrap classes and customize form fields.
        widgets = {
            "text": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your review...",
                    "rows": 4,
                }
            ),
            "rating": NumberInput(attrs={"class": "form-control", "min": 0, "max": 5}),
            "will_recommend": CheckboxInput(attrs={"class": "form-check-input"}),
        }
