"""Markdown processing utilities."""

import re
import markdown
from bleach import clean
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES

# Add additional HTML tags that we want to allow
EXTENDED_ALLOWED_TAGS = list(ALLOWED_TAGS) + [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'div', 'span', 'hr', 'br',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'blockquote', 'code', 'pre', 'em', 'strong', 'i', 'b', 'u', 'strike',
    'a', 'img'
]

# Add additional attributes 
EXTENDED_ALLOWED_ATTRIBUTES = {
    **ALLOWED_ATTRIBUTES,
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'td': ['colspan', 'rowspan', 'align'],
    'th': ['colspan', 'rowspan', 'align'],
    'code': ['class'],
    'pre': ['class'],
    '*': ['class', 'id']  # Allow class and id on all elements
}


def markdown_to_html(text: str) -> str:
    """Convert markdown text to safe HTML.
    
    Args:
        text: Markdown text to convert
        
    Returns:
        Sanitized HTML string
    """
    if not text:
        return ""
    
    # Convert Markdown to HTML
    html = markdown.markdown(
        text,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.attr_list',
            'markdown.extensions.smarty',
            'markdown.extensions.nl2br'
        ]
    )
    
    # Sanitize HTML to prevent XSS
    cleaned_html = clean(
        html,
        tags=EXTENDED_ALLOWED_TAGS,
        attributes=EXTENDED_ALLOWED_ATTRIBUTES,
        strip=True
    )
    
    # Apply additional styling for better readability
    
    # Add classes to headings
    cleaned_html = re.sub(r'<h1>', r'<h1 class="heading-1">', cleaned_html)
    cleaned_html = re.sub(r'<h2>', r'<h2 class="heading-2">', cleaned_html)
    cleaned_html = re.sub(r'<h3>', r'<h3 class="heading-3">', cleaned_html)
    
    # Style lists
    cleaned_html = re.sub(r'<ul>', r'<ul class="md-list">', cleaned_html)
    cleaned_html = re.sub(r'<ol>', r'<ol class="md-list">', cleaned_html)
    
    # Style code blocks
    cleaned_html = re.sub(r'<pre><code>', r'<pre class="code-block"><code>', cleaned_html)
    
    # Style blockquotes
    cleaned_html = re.sub(r'<blockquote>', r'<blockquote class="md-quote">', cleaned_html)
    
    return cleaned_html