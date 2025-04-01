from django import template

register = template.Library()

@register.filter
def japanese_weekday(value):
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    if hasattr(value, 'weekday'):
        return weekdays[value.weekday()]
    return ''
