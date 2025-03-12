from rest_framework import generics

from courses.models import Subject
from courses.api.serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
    """ List all subjects """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """ Retrieve a subject by its slug """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
