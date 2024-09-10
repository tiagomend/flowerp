from django.utils.safestring import mark_safe


def badge(value, color):
    html = f"""
        <span class="badge {color}">{value}</span>
    """

    return mark_safe(html)
