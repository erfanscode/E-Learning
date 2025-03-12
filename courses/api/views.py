from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from courses.models import Subject, Course
from courses.api.serializers import (
  SubjectSerializer,
  CourseSerializer
)


class SubjectListView(generics.ListAPIView):
    """ List all subjects """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """ Retrieve a subject by its slug """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(APIView):
    """ Enroll a user in a course """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ List all courses, or retrieve one by its slug """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
