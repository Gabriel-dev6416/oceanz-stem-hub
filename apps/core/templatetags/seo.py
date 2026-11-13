import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# JSON unicode escapes for <, > and &, as in Django's json_script. Built from chr(92), the
# backslash, so the mapping cannot be altered by tools that rewrite escape sequences.
_BACKSLASH = chr(92)
_ESCAPES = {ord(char): f"{_BACKSLASH}u{ord(char):04X}" for char in "<>&"}


@register.simple_tag
def jsonld(data):
    """schema.org structured data. Escaped like Django's json_script, so values entered in the
    admin cannot close the script element."""
    payload = json.dumps(data, ensure_ascii=False).translate(_ESCAPES)
    # Reviewed: <, > and & are escaped above, as Django's json_script does before its own
    # mark_safe; test_structured_data_cannot_break_out_of_the_script proves it.
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')  # nosec B308 B703
