from django import template
import json
# import datetime
# import nepali_datetime
from django.template.defaulttags import register

register = template.Library()

@register.filter
def json_to_dict(value):
    try:
        json_value = json.loads(value)
        if isinstance(json_value, dict):
            return json_value.items()
    except (ValueError, TypeError):
        pass
    return {}

# @register.filter
# def get_NepaliDate(date):
#     try:
#         dt = datetime.date(date.year,date.month,date.day)
#         nepali_date = nepali_datetime.date.from_datetime_date(dt)
#         return nepali_date
#         # return nepali_date.strftime('%K-%n-%D (%k %N %G)')   
#     except:
#         return date

