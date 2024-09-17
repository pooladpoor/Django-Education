from django import forms
from .models import *


class TicketForm(forms.Form):  # ازاین چیز آماده جنگو ارث بری کن
    SUBJECT_CHOICES = (
        #(ذخیره ,نمایشی)
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    # وارد کردن اجباری____________   ____________________________به جای تکست فیلد
    message = forms.CharField(widget=forms.Textarea, required=True, label='message:')
    #  لیبل رو اگه نویسی نام متغیر رو دیفالت برمیداره ^
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    # به جای html میشه این کار ها رو اینجا هم انجام داد برای وقتی که اونجا راه نداره
    # email = forms.EmailField(widget=forms.EmailInput({"plaseholder": 'pwladpwr@gmail.com',
    #                                                     # "style": '...', # هر چیز css ای که خواستی
    #                                                     "class": 'name'}))

    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)  # گزینه انتخابی

    # خود جنگو همچین چیزی برای ایمیل تعریف کرده دیگه تو نمیخاد زحمت بکشی
    # اینجوری هر کدوم از موارد بالا رو برسی برسی میکنی و اگه اشتباه زده ارور میدی
    def clean_phone(self):  # اسم تابع به همین فرمت باشه
        phone = self.cleaned_data['phone']  # مقدار اون رو میگیری
        if phone:  # اگه یه چیزی زده بود یعنی خالی نبود
            if not phone.isnumeric():
                # این ارور تو html دردسترس هست و هر جور خواستی میتونی نمایشش بدی
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            else:
                return phone  # اگه اوکی بود


class CommentForm(forms.ModelForm):  # اینجوری مودل و فیلدی که میخای رو میدی و خودش برات فرم رومیسازه
    class Meta:
        model = Comment
        fields = ['name', 'body']  # این فیلد ها او فقط باید کاربر بزنه تا فرم ایجاد بشه

    # # وقتی تو htnl اینجوری مینویسی {{ form.as_p }} دیگه نمیشه اونجا کاریش کرد
    # widgets = {  # اینجوری براش چیزی که قرار بوده تو htnl بزاریم رو مشخص میکنیم
    #     'body': forms.TextInput(attrs={
    #         'placeholder': 'متن',  #کمرنگ تو باکس مینویسه
    #         'class': 'cm-body'  # تو css با این کلاس بهش استایل میدی
    #     }),
    #     'name': forms.TextInput(attrs={
    #         'placeholder': 'نام',
    #         'class': 'cm-name'
    #     })
    # }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه است")
            else:
                return name


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description','reading_time']

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if len(title) < 3:
                raise forms.ValidationError("موضوع کوتاه است")
            elif len(title) > 20:
                raise forms.ValidationError("موضوع بلند است")
            else:
                return title

    def clean_description(self):
        description = self.cleaned_data['description']
        # title = self.cleaned_data['title']
        if description:
            if len(description) < 20:
                raise forms.ValidationError("توضیحات نمبتواند از موضوع کوتاه تر باشد")
            else:
                return description
