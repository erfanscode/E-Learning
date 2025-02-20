from django.shortcuts import redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.apps import apps
from django.urls import reverse_lazy

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

from .models import Course, Module, Content
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
            return redirect('courses:manage_course_list')
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })


class ContentCreateUpdateView(TemplateResponseMixin, View):
    ''' create or update content for a specific course module '''
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        '''
            Dynamically fetch the model based
            on the content type (e.g., text, file, image, video)
        '''
        if model_name in ['text', 'file', 'image', 'video']:
            return apps.get_model(
                app_label='courses',
                model_name=model_name
            )
        return None

    def get_form(self, model, *args, **kwargs):
        '''
            Generate a modelform for the given model
            excluding owner, order, created, and updated fields
        '''
        Form = modelform_factory(
            model,
            exclude=[
                'owner',
                'order',
                'created',
                'updated'
            ]
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        '''
            Ensure that the module exists and belongs to the
            logged-in user, and retrieve the corresponding content model
        '''
        self.module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        self.model = self.get_model(model_name)

        if id:
            # Fetch existing content if an ID is provided
            self.obj = get_object_or_404(
                self.model,
                id=id,
                owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        '''
            Handle GET request:
            Display the content form for editing or creating content
        '''
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })

    def post(self, request, module_id, model_name, id=None):
        '''
            Handle POST request:
            Validate and save the form, create new content if necessary
        '''
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # New content
                Content.objects.create(
                    module=self.module,
                    item=obj
                )
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })


class ContentDeleteView(View):
    ''' Deleting a specific content item '''
    def post(self, request, id):
        '''
            Handle POST request:
            Delete the content item and redirect to the module content list
        '''
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)
