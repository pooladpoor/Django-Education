# اینجا تمپلیت تگ سفارشی خودمون رو مینویسیم

from django import template
from django.db.models import Count, Max, Min
from ..models import *
from django.urls import reverse
from django.utils.safestring import mark_safe
from markdown import markdown
import json

register = template.Library()


@register.simple_tag()  # آرگوملن name رو میشه بهش بدی ولی دیفالت اسم تابع هست
def total_posts():
    return Post.published.count()


#                         کوری ست رو میشماره ^^^^^^

@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish
    # تاریخ آخرین پست منتشر شده^^^^^^


@register.simple_tag()
def last_post_url():
    return reverse("blog:posts_detail", args=[Post.published.last().id])


# این برخلاف قبلی ها که رشته میدادن یه html برمیگردونه
@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context  # با این کانتکس اون html بالا رندر میشه


@register.simple_tag
def most_popular_posts(count=5):
    # این فیلد ریلیتد نیم کامنت که به _____  پست وصل کردیم هست و شامل همه کانت های این پست میشه
    p = Post.published.annotate(comments_count=Count('comments'))  # یه کوری ست شامل پست ها برمیگردونه
    #                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #  اینجوری یه فیلد موقت ایجاد مینیم که توی دیتا بیس ٍثبت نمیشه و فقط اینجا ازش استفاده میکنیم و تموم
    return p.order_by('-comments_count')[:count]
    #  حالا براساس همین فیلد موقتی که ساختیم مرتبش میکنیم و بعدش 5 تای اولش رو برمیداریم


# اینجوری تمپلیت فیلتر سفارشی میسازیم
@register.filter(name="markdown")
#  یه ورودی که همون چیزی که روش فیلتر میزنی رو میگیره خاستی ورودی دوم هم با : جلوش میدی و اینجا میگیری مثل فیلتر add
def to_markdown(text):
    # مارک سیف به جنگو میگه که این html امن هست
    # اگه نویسی html رو متن فرض میکنه و همون رو نشون میده
    #      _________
    return mark_safe(markdown(text))
#                    ^^^^^^^^
# مارک دون کاری میکنه که کاربر عادی بتونه
# منت بنویسه و خودکار به اچ تی ام ال تبدیل بشه
# مثل واتساپ و تلگرام واینا که متن بلد و کج و لینک دار مینویسی
#خیلی کار میشه کرد داکیومنت خودش بخون اگه لازم شد


@register.simple_tag()
def ext_reading_time(cuont=1):
    li1 = list(Post.published.order_by("-reading_time")[:cuont])
    li2 = ["..."]
    li3 = (list(reversed(Post.published.order_by("reading_time")[:cuont])))
    return li1 + li2 + li3


@register.simple_tag()
def activat_users(cuont=1):
    all_user = User.objects.annotate(posts_count=Count('user_Post'))
    return all_user.order_by("-posts_count")[:cuont]


@register.filter()
def cuss_filter(text: str):
    folsh_li = json.load(open("D:\\PycharmProjects\\djangoProject2\\blog\\static\\json\\fohsh.json",encoding='utf-8'))["farsiWords"]

    for word in folsh_li:
        text = text.replace(word, len(word) * "*")
    return mark_safe(text)
