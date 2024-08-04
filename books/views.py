from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from books.models import Book, Review
from books.forms import ReviewForm


# Create your views here.
def home(request):
    books = Book.objects.all()
    return render(request, "home_page.html", {"books": books})


# Read a book in detail
# /book/<int:book_id>
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book)

    return render(request, "detail.html", {"book": book, "reviews": reviews})


# Create a review for a book
# /book/<int:book_id>/create
@login_required
def create_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "GET":
        return render(
            request, "create_review.html", {"form": ReviewForm(), "book": book}
        )

    if request.method == "POST":
        try:
            form = ReviewForm(request.POST)
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.book = book
            new_review.save()
            return redirect("detail", new_review.book.id)

        except ValueError:
            return render(
                request,
                "create_review.html",
                {"form": ReviewForm(), "error": "bad data passed in"},
            )


# Update a review for a book
# /book/review/<int:review_id>
@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == "GET":
        form = ReviewForm(instance=review)
        return render(request, "update_review.html", {"review": review, "form": form})

    if request.method == "POST":
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect("detail", review.book.id)

        except ValueError:
            return render(
                request,
                "update_review.html",
                {"review": review, "form": form, "error": "bad data in form"},
            )


# Delete a review for a book
# /book/review/<int:review_id>/delete
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect("detail", review.book.id)
