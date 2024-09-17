from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


class PublishManager(models.Manager):  # این منیجر دست ساز هست که فقط پابلیش شده ها رو میده
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


class Post(models.Model):
    def __str__(self):
        return f"{self.title} (by {self.author})"

    class Status(models.TextChoices):
        PUBLISH = 'PU', 'publish'
        REJECT = 'RE', 'Reject'
        DRAFT = 'DR', 'Draft'

    title = models.CharField(max_length=250,verbose_name='موضوع')
    description = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(max_length=250,default="")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default='DR')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_Post')
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    #                      اینتیجر مثبت   ^^^^^^^^^^^^^^^^^^

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ["publish"]
        indexes = [models.Index(fields=["publish"])]

    # این متد رو میشه مثل اتریبیوت استفاده کرد و هرجایی خواستی این url رو برات تولید میکنه (تو پنل امین هم خودش میزاره)
    def get_absolute_url(self):
        return reverse("blog:posts_detail", args=[self.id])
        #                    namespase:name      توی فایل url مشخص کردی



class Ticket(models.Model):
    #                           این رو توی پنل ادمین نشون میده  ___________
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(max_length=250, verbose_name="موضوع")

    class Meta:
        #این رو توی پنل ادمین نشون میده
        verbose_name = "تیکت"  # خودش
        verbose_name_plural = "تیکت ها" # جمعش

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت") # یه چک باکس میزاره که میشه تیک برنی

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}: {self.post}"
