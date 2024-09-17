from .import views
from django.urls import path
# ای فایل رو خودت ایجاد کن وurl  های مربوط به این اپ رو توش بنویس بعد تو url های اصلی پروژه معرفیش کن
#  موقع استفاده باید اول url اونجا بنویسی بعد از اون به مال این url هایی که اینجا آدرسش رو نوشتی برسی


app_name = 'blog' # اون نیم اسپس که تو urls.py اصلی پروژه نوشتی
urlpatterns = [
    # اگه این url استفاده بشخ تابع پست لیست که توی ویو هست صدا زده میشه
    # path('posts/', views.posts_list, name='posts_list'),
    path('posts/', views.posts_list.as_view(), name="post_list"), #برای کلای بیس ویو ها اینجوریه

    # ای دی رو از url ورودی میگیره و به تابع میفرسته (برای صفحه ای مه مخصوص هر پست هست)
    path("post/<int:id>", views.posts_detail, name='posts_detail'),
    # path('post/<pk>', views.posts_detail.as_view(), name="posts_detail"),#برای کلای بیس ویو ها اینجوریه

    path('ticket',views.ticket, name="ticket"),
    path("post/<int:id>/comment", views.post_comment, name='post_comment'),
    path('',views.index, name="index"),
    path('add_post',views.add_post,name="add_post")

]
