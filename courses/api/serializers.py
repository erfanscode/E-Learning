from rest_framework import serializers

from courses.models import (
  Subject,
  Course,
  Module,
  Content
)


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


class ItemRelatedField(serializers.RelatedField):
    """ A custom field to return the URL of the item """
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """ Serializer for the Content model """
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """ Serializer for the Module model with its contents """
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """ Serializer for the Course model with its contents """
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules']
