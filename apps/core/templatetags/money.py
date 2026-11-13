from decimal import Decimal

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def naira(amount):
    """Decimal('1000') -> '₦1,000'; Decimal('1500.50') -> '₦1,500.50'."""
    amount = Decimal(amount)
    if amount == amount.to_integral_value():
        return f"₦{intcomma(int(amount))}"
    return f"₦{intcomma(f'{amount:.2f}')}"
