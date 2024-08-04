from django.urls import path
from books import views


urlpatterns = [
    path("<int:book_id>", views.detail, name="detail"),
    path("<int:book_id>/create", views.create_review, name="create_review"),
    path("review/<int:review_id>", views.update_review, name="update_review"),
    path("review/<int:review_id>/delete", views.delete_review, name="delete_review"),
]
