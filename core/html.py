from django.utils.safestring import mark_safe


def badge(value, color):
    html = f"""
        <span class="badge {color}">{value}</span>
    """

    return mark_safe(html)

def badge_icon(value, color, icon):
    html = f"""
        <span class="badge {color}">
            <i class="icon_{icon}"></i>
            {value}
        </span>
    """

    return mark_safe(html)
