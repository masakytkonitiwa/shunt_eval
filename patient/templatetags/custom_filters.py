from django import template
import datetime

register = template.Library()

@register.filter
def japanese_weekday(value):
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    
    if isinstance(value, datetime.datetime):
        value = value.date()  # datetime → date に変換
    
    if hasattr(value, 'weekday'):
        return weekdays[value.weekday()]
    
    return ''
