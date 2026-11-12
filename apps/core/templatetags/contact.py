import re
from urllib.parse import quote

from django import template

register = template.Library()


def _digits(number):
    return re.sub(r"\D", "", number or "")


@register.filter
def tel_link(number):
    """'+234 706 457 9661' -> 'tel:+2347064579661'."""
    return f"tel:+{_digits(number)}"


@register.simple_tag
def whatsapp_link(number, page_name=""):
    """WhatsApp click-to-chat link with a message naming the page (FR-WEB-10)."""
    message = "Hello OCEANZ STEM HUB, I would like to know more"
    if page_name:
        message += f" (from your {page_name} page)"
    return f"https://wa.me/{_digits(number)}?text={quote(message + '.')}"
