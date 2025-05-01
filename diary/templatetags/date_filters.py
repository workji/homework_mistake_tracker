from django import template
from datetime import datetime, date
import math

register = template.Library()

@register.filter
def time_since(value):
    if not value:
        return ""

    today = date.today()
    delta = today - value

    if delta.days == 0:
        return "今天"
    elif delta.days < 30:
        return f"{delta.days} 天前"
    elif delta.days < 365:
        months = math.floor(delta.days / 30)
        return f"{months} 个月前"
    else:
        years = math.floor(delta.days / 365)
        return f"{years} 年前"