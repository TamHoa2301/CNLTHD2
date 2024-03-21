from django.contrib import admin
from course.models import Category, Course, Tag, Lesson, Comment
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from cloudinary.models import CloudinaryField


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date', 'active']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name', 'created_date']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, course):
        if course.image:
            return mark_safe(f"<img width='200' src='{course.image.url}' />")

    class Media:
        css = {
            'all': ['/static/css/style.css']
        }


admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tag)
admin.site.register(Lesson)
admin.site.register(Comment)

# Register your models here.
