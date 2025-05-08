from django import template

register = template.Library()

@register.filter
def int_value(value):
    try:
        return int(round(float(value)))
    except (ValueError, TypeError):
        return 0

@register.filter
def star_list(value):
    """
    Returns a list of 'full', 'half', or 'empty' for 5 stars, based on the rating.
    Shows a half star if the decimal part is >= 0.25 and < 0.75, and a full star if >= 0.75.
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        value = 0
    stars = []
    for i in range(1, 6):
        if value >= i:
            stars.append('full')
        elif (i - value) <= 0.75 and (i - value) > 0.25:
            stars.append('half')
        else:
            stars.append('empty')
    return stars

@register.filter
def star_percentage(value):
    """Converts a 0-5 rating to a percentage for star fill."""
    try:
        return float(value) / 5 * 100
    except (ValueError, TypeError):
        return 0
