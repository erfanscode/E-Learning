from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
  # The Subject model represents a subject that students can study
  title = models.CharField(max_length=200, verbose_name='عنوان')
  slug = models.SlugField(max_length=225, unique=True, verbose_name='اسلاگ')

  class Meta:
    ordering = ['title']

  def __str__(self):
    return self.title
  

class Course(models.Model):
  # The Course model represents a course that students can take
  owner = models.ForeignKey(
    User, related_name='courses_created',
    on_delete=models.CASCADE,
    verbose_name='سازنده'
  )
  subject = models.ForeignKey(
    Subject,
    related_name='courses',
    on_delete=models.CASCADE,
    verbose_name='موضوع'
  )
  
  title = models.CharField(max_length=200, verbose_name='عنوان')
  slug = models.SlugField(max_length=225, unique=True, verbose_name='اسلاگ')

  overview = models.TextField(verbose_name='توضیح')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created']

  def __str__(self):
    return self.title


class Module(models.Model):
  # The Module model represents a module that belongs to a course
  course = models.ForeignKey(
    Course,
    related_name='modules',
    on_delete=models.CASCADE,
    verbose_name='دوره'
  )
  title = models.CharField(max_length=200, verbose_name='عنوان')
  description = models.TextField(blank=True, verbose_name='توضیح')

  def __str__(self):
    return self.title