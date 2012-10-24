from django import template
import md5

register = template.Library()

@register.filter
def gravatar(value, size):
    """Return gravatar url for the given email address"""
    default = "mm"  # default to mystery man
    gravatar_url = "http://www.gravatar.com/avatar/"
    gravatar_url += md5.new(value).hexdigest()
    gravatar_url += "?s=" + size
    gravatar_url += "&d=" + default
    
    return gravatar_url

