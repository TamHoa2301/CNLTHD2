from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    name = models.CharField(max_length=200)
    description = RichTextField(null=True)
    image = CloudinaryField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=250, unique=True)


class Lesson(BaseModel):
    name = models.CharField(max_length=200)
    content = RichTextField(null=True)
    image = CloudinaryField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')

