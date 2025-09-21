from django import template
from django.utils.safestring import mark_safe
import markdown
import re

register = template.Library()

@register.filter(name='get_yt_id')
def get_yt_id(url):
    if not isinstance(url, str):
        return ""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = re.search(youtube_regex, url)
    if match:
        return match.group(6)
    return ""

@register.filter(name='markdownify')
def markdownify(text):
    """
    Converts markdown text to HTML and marks it as safe for rendering.
    """
    return mark_safe(markdown.markdown(text))