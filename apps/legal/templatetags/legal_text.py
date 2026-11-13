from django import template
from django.utils.html import format_html, format_html_join
from django.utils.safestring import SafeString

register = template.Library()


@register.filter
def legal_body(text):
    """Plain text to HTML: '## ' headings, '- ' lists, blank-line paragraphs. Built only from
    format_html pieces, so every part of the stored text is escaped."""
    html = SafeString("")
    for block in text.replace("\r\n", "\n").split("\n\n"):
        lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):
            html += format_html("<h2>{}</h2>", lines[0][3:])
            lines = lines[1:]
        if lines and all(line.startswith("- ") for line in lines):
            items = format_html_join("", "<li>{}</li>", ((line[2:],) for line in lines))
            html += format_html("<ul>{}</ul>", items)
        elif lines:
            html += format_html("<p>{}</p>", " ".join(lines))
    return html
