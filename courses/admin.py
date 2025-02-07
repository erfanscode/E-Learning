from django.contrib import admin
from .models import Subject, Course, Module


# ---------- Inline Classes ---------- #
class ModuleInline(admin.StackedInline):
    ''' The ModuleInline class is a stacked inline for the Module model '''
    model = Module
    extra = 1


# ---------- Admin Classes ---------- #
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    '''
      The SubjectAdmin class customizes
      the admin interface for the Subject model
    '''
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    '''
      The CourseAdmin class customizes
      the admin interface for the Course model
    '''
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
