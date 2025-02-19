from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse_lazy

from .models import Course
from .forms import ModuleFormSet


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


class OwnerCourseMixin(LoginRequiredMixin,
                       PermissionRequiredMixin, OwnerMixin):
    '''
        For managing the Course model, ensuring that only
        courses owned by the logged-in user are processed
    '''
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')


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
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    '''
        Creating a new course, ensuring that the course
        is associated with the logged-in user
    '''
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    '''
        Updating an existing course, ensuring that only
        the owner can make changes
    '''
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    ''' Deleting a course, restricted to the owner of the course '''
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    ''' Managing course modules using a formset '''
    template_name = 'courses/manage/module/formset.html'
    course = 0

    def get_formset(self, data=None):
        ''' Create and return a formset for the course mudules '''
        return ModuleFormSet(
            instance=self.course,
            data=data
        )

    def dispatch(self, request, pk):
        ''' Ensure the course exists and is owned by the current user '''
        self.course = get_object_or_404(
            Course,
            id=pk,
            owner=request.user
        )
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        '''
            Handle GET request:
            display the formset for editing modules
        '''
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

    def post(self, request, *args, **kwargs):
        '''
            Handle POST request:
            validate and save the formset
        '''
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })
