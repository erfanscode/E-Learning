from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import Course


# Mixins
class OwnerMixin:
    def get_queryset(self):
        ''' Show only the courses created by the current user '''
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    '''
        Automatically set the current user in the owner attribute
        of the object being saved
    '''
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    '''
        For managing the Course model, ensuring that only
        courses owned by the logged-in user are processed
    '''
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    '''
        For editing courses that restricts data to the owner
        and automatically assigns the logged-in user as the owner when saving
    '''
    template_name = 'courses/manage/course/form.html'


# Views
class ManageCourseListView(OwnerCourseMixin, ListView):
    ''' List view for the owner's courses '''
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    '''
        Creating a new course, ensuring that the course
        is associated with the logged-in user
    '''
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    '''
        Updating an existing course, ensuring that only
        the owner can make changes
    '''
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    ''' Deleting a course, restricted to the owner of the course '''
    template_name = 'courses/manage/course/delete.html'
