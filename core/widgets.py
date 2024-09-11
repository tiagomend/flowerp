from django.forms import widgets
from django.utils.safestring import mark_safe


class Awesomplete(widgets.Select):
    def render(self, name, value, attrs=None, renderer=None):
        select_html = super().render(name, value, attrs, renderer)
        html = f"""
            <div class='awesomplete'>
                {select_html}
            </div>
        """
        return mark_safe(html)
