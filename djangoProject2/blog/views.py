# اینجا فایل تمپلیت که html هست رو رندر میکنیم و میفرستیم
# یعنی طبق اون دیکشنری کانتکس هر جا تو html یه کلید ارز دیکشنری باشه مقدار اون که یه متغر هست رو جاش میزاره
# و در جواب ریکوست میفرسته


from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse
from .models import *
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import *
from django.views.decorators.http import require_POST
from django.utils.safestring import mark_safe


# def posts_list(request):
#     posts = Post.published.all()  # از منیجری که خودمون ساختیم استفاده میکنیم تا فقط پستهای پابلیش شده بده
#     paginator = Paginator(posts, 4)  # کل پست ها و اینکه میخای تو هر صفحه چند تا باشه بهش میدی
#     page_number = request.GET.get('page', 1)  # متد گت دومی روی دیکشنری زدیم تا اگه نبود دیفالت داشته باشه
#     try:
#         posts = paginator.page(page_number)  # یه صفحه شامل تعدادپست مورد نظر
#     except EmptyPage: #     __________  تعداد صفحه
#         posts = paginator.page(paginator.num_pages)  # عدد خارج رنج بزنه
#     except PageNotAnInteger:
#         posts = paginator.page(1)  # رشته و... بزنه
#
#     context = {
#         'posts': posts
#     }
#     return render(request, "blog/list.html", context=context)
# جایگزین _____________
class posts_list(ListView):
    # model = Post # اینجوری خودش با منیجر آبجکت همه رو میفرسته
    queryset = Post.published.all() # اینجوری از منیجر شخصی استفاده میکنیم
    context_object_name = "posts" # اسم متغیر پست ها هست که میفرسته تو html تا رندر بشه (دیفالت object_list هست)
    paginate_by = 3 # تو هر صفحه چند باشه
    template_name = "blog/list.html" # آدرس فایل تمپلیت مه باید برداره (دیفالت postlist هست)

def posts_detail(request, id):
    # post = Post.published.get(id = id)  # این بر اساس ایدی پست اون رو برمیگردونه که اگه نباشه ارور میده
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISH)  # برخلاف بالایی ترای و اکسپت نمیخواد
    comments = post.comments.filter(active=True)
    #              _____^____     related_name که نوی مودل کامنت تعریف کردیم
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, "blog/detils.html", context=context)
# جایگزین _____________
# class posts_detail(DetailView):
#     model = Post
#     template_name = "blog/detils.html"



def ticket(request):
    if request.method == "POST": # متد پست برای ارسال اطلاعات وارد شده تو فرم هست
        form = TicketForm(request.POST) # با اون اطلاعات یه فرم میسازیم
        if form.is_valid() : # طبق چیزایی که تو کلاس تیکت فرم نوشتی اطلاعات وارد شده معتبر هست اگه
            cd = form.cleaned_data # اطلاعات به صورت دیکشنری
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject']) # تو دیتا بیس زخیره میشه با این مودل و خودش سیو میکنه
            #                نیم و نیم اسپس اون________
            return redirect("blog:ticket") # به این url هدایت میشه
        else:
            print("faule")
    else: # تازه میخواد فرم رو ببینه و پر کنه (متد GET)
        form = TicketForm() # یه فرم خالی میسازی
    return render(request, "forms/ticket.html", {'form': form})
    # اچ تی ام ال رو رندر میکنی و میفرستی براش



@require_POST # کاری میکنه که فقط برای متد پست کار کنه
def post_comment(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISH)
    comment = None
    form = CommentForm(data=request.POST) # با دیتای دریافت شده آبجکت فرم رو میسازه
    if form.is_valid(): # اگه مشکل داشت خودش خطا میده و میگه و کامنت برابر نان میمونه
        comment = form.save(commit=False) # از اون فرم یه رکورد کامنت ساخته میشه ولی تو دتابیس سیو نمیشه
        comment.post = post # فیلد پست رو هم خودمون پر میکنیم
        comment.save() # ذر آخر اون رو توی دیتا بیس سیو میکنیم
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, "forms/comment.html", context)


def index(request):
    return render(request, "blog/index.html")

def add_post(request):
    error = ''
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            po_fo = form.save(commit=False)
            try:
                po_fo.author = request.user
                po_fo.save()
            except ValueError:
                error = mark_safe("<a href='http://localhost:8000/admin/login/?next=/admin/' target='_blank'>لاگین کنید</a>")

    else: # تازه میخواد فرم رو ببینه و پر کنه (متد GET)
        form = PostForm() # یه فرم خالی میسازی
    return render(request, "forms/post.html", {'form': form ,"error":error})
    # اچ تی ام ال رو رندر میکنی و میفرستی براش
