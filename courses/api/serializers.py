from rest_framework import serializers

from courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    """ Serializer for the Subject model """
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']
