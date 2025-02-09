from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Subject(models.Model):
    ''' The Subject model represents a subject that students can study '''
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=225, unique=True, verbose_name='اسلاگ')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    ''' The Course model represents a course that students can take '''
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
    ''' The Module model represents a module that belongs to a course '''
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


class Content(models.Model):
    ''' The content model represents a content object '''
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE,
        verbose_name='ماژول'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='نوع محتوا',
        limit_choices_to={'model__in': (
                              'text',
                              'video',
                              'image',
                              'file'
                          )}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    ''' The ItemBase model represents a base class for content models '''
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE,
        verbose_name='سازنده'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    ''' The Text model represents a text content object '''
    content = models.TextField(verbose_name='متن')


class File(ItemBase):
    ''' The File model represents a file content object '''
    file = models.FileField(upload_to='files', verbose_name='فایل')


class Image(ItemBase):
    '''  The Image model represents an image content object '''
    file = models.FileField(upload_to='images', verbose_name='تصویر')


class Video(ItemBase):
    ''' The Video model represents a video content object '''
    url = models.URLField(verbose_name='ویدیو')
