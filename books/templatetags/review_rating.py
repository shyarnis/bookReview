from django import template

register = template.Library()


@register.filter
def star_rating(rating):
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        rating = 0

    full_star = '<i class="fas fa-star"></i>'
    empty_star = '<i class="far fa-star"></i>'
    return (full_star * rating) + (empty_star * (5 - rating))
