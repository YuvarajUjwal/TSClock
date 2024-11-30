from django import template
import math

from tango.models import *
register = template.Library()

# 100 -> 10% --> mrp  - ( mrp * discount * 0.01 ) = selprice
@register.simple_tag
def cal_sellprice(price , discount):
    if discount is None or discount == 0:
        return price
    # print(price)
    sellprice = price
    # print(price)
    sellprice = price - discount
    return sellprice


@register.filter
def rupee(price):
    return f'₹{price}'

@register.simple_tag
def is_enrolled(request , course):
   
    user = None
    if not request.user.is_authenticated:
        return False
        # i you are enrooled in this course you can watch every video
    user = request.user
    try:
        user_course = UserCourse.objects.get(user = user  , course = course)
        return True
    except:
        return False