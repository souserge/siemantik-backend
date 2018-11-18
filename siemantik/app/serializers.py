from rest_framework import serializers

from django.contrib.auth.models import User
from siemantik.app.models import Project, Label, Document, Classifier


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'project_set')


class ProjectSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'language')


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'classname', 'display_name')


class ProjectSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'language', 'description', 'labels')


class DocumentSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'label', 'is_set_manually')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'text', 'label', 'is_set_manually')

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'language')
    

class ProjectDocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=1000)
    text = serializers.CharField()
    label_id = serializers.IntegerField(allow_null=True)