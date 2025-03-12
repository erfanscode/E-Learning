from rest_framework import serializers

from courses.models import Subject, Course, Module


class SubjectSerializer(serializers.ModelSerializer):
    """ Serializer for the Subject model """
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """ Serializer for the Module model """
    class Meta:
        model = Module
        fields = ['id', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """ Serializer for the Course model """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']
