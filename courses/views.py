from django.views.generic.list import ListView
from .models import Course


class ManageCourseListView(ListView):
    ''' List view for the owner's courses '''
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        ''' Show only the courses created by the current user '''
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
