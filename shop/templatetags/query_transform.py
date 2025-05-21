from django import template

register = template.Library()

@register.simple_tag
def query_transform(request_get, exclude_key):
    updated = request_get.copy()
    if exclude_key in updated:
        updated.pop(exclude_key)
    return updated.urlencode()
