from django import template
from django.utils.safestring import mark_safe
import markdown
import re

register = template.Library()

@register.filter(name='markdownify')
def markdownify(text):
    """
    Converts a Markdown string to HTML, including tables.
    """
    html = markdown.markdown(text, extensions=['tables'])
    return mark_safe(html)

@register.filter(name='get_yt_id')
def get_yt_id(url):
    """
    Extracts the YouTube video ID from various URL formats using regex.
    """
    if not isinstance(url, str):
        return ""
    # --- THIS IS THE FIX: Using a raw string (r'...') to avoid warnings ---
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = re.search(youtube_regex, url)
    if match:
        return match.group(6)
    return ""